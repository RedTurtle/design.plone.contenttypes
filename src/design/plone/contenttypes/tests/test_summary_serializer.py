# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit


import unittest


class SummarySerializerTest(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_get_content_return_right_has_children_info(self):

        api.content.create(
            container=self.document, type="Document", title="empty"
        )
        api.content.create(
            container=self.document, type="Document", title="filled"
        )

        api.content.create(
            container=self.document["filled"], type="Document", title="Example"
        )
        commit()

        response = self.api_session.get(self.document.absolute_url())

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "empty")
        self.assertFalse(items[0]["has_children"])
        self.assertEqual(items[1]["title"], "filled")
        self.assertTrue(items[1]["has_children"])

    def test_get_content_return_id_value(self):

        news = api.content.create(
            container=self.portal, type="News Item", title="news"
        )
        commit()

        response = self.api_session.get(news.absolute_url())

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["id"], "multimedia")
        self.assertEqual(items[1]["id"], "documenti-allegati")
