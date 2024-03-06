# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)

from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing.helpers import logout
from plone.indexer.interfaces import IIndexableObject
from plone.restapi.interfaces import IZCatalogCompatibleQuery
from plone.restapi.testing import RelativeSession
from transaction import commit
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
import unittest


class ExcludeFromSearchFunctionalTest(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING
    maxDiff = None

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.catalog = api.portal.get_tool("portal_catalog")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret!!!",
        )

        self.news = api.content.create(
            container=self.portal,
            type="News Item",
            title="Test News",
        )

        self.document = api.content.create(
            container=self.portal,
            type="Document",
            title="Test Document",
        )

        api.content.transition(obj=self.news, transition="publish")
        api.content.transition(obj=self.news["multimedia"], transition="publish")
        api.content.transition(obj=self.document, transition="publish")

        commit()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.api_session_foo = RelativeSession(self.portal_url)
        self.api_session_foo.headers.update({"Accept": "application/json"})
        self.api_session_foo.auth = ("foo", "secret!!!")

        self.api_session_anon = RelativeSession(self.portal_url)
        self.api_session_anon.headers.update({"Accept": "application/json"})

    def tearDown(self):
        self.api_session.close()
        self.api_session_anon.close()

    def test_exclude_from_search_indexer_for_item_without_behavior(self):
        """
        news item does not have the behavior, so it has False by default
        """
        self.assertRaises(AttributeError, getattr, self.news, "exclude_from_search")
        adapter = queryMultiAdapter((self.news, self.catalog), IIndexableObject)
        self.assertFalse(adapter.exclude_from_search)

    def test_exclude_from_search_indexer_for_item_with_behavior_enabled(self):
        """ """
        self.assertFalse(self.document.exclude_from_search)
        adapter = queryMultiAdapter((self.document, self.catalog), IIndexableObject)
        self.assertFalse(adapter.exclude_from_search)

    def test_exclude_from_search_indexer_for_item_with_behavior_enabled_and_set(self):
        """ """
        self.assertTrue(self.news["multimedia"].exclude_from_search)
        adapter = queryMultiAdapter(
            (self.news["multimedia"], self.catalog), IIndexableObject
        )
        self.assertTrue(adapter.exclude_from_search)

    def test_adapter_do_not_append_anything_to_query_for_auth_users(self):
        catalog_compatible_query = getMultiAdapter(
            (self.portal, self.request), IZCatalogCompatibleQuery
        )({})
        self.assertEqual({}, catalog_compatible_query)

    def test_adapter_append_exclude_from_search_to_query_for_anon_users(self):
        logout()
        catalog_compatible_query = getMultiAdapter(
            (self.portal, self.request), IZCatalogCompatibleQuery
        )({})
        self.assertEqual(catalog_compatible_query, {"exclude_from_search": False})

    def test_search_return_excluded_contents_for_logged_users(self):
        """ """
        resp = self.api_session.get(
            "/@search", params={"SearchableText": "multimedia"}
        ).json()
        self.assertEqual(resp["items_total"], 1)

        resp = self.api_session_foo.get(
            "/@search", params={"SearchableText": "multimedia"}
        ).json()
        self.assertEqual(resp["items_total"], 1)

    def test_search_do_not_return_excluded_contents_for_anon_users(self):
        """ """
        resp = self.api_session_anon.get(
            "/@search", params={"SearchableText": "multimedia"}
        ).json()
        self.assertEqual(resp["items_total"], 0)
