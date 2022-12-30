# -*- coding: utf-8 -*-
from datetime import datetime
from DateTime import DateTime
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
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class VocabulariesControlpanelTest(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session_anon = RelativeSession(self.portal_url)
        self.api_session_anon.headers.update({"Accept": "application/json"})

        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.intids = getUtility(IIntIds)

        published_news = api.content.create(
            container=self.portal, type="News Item", title="Published news"
        )
        published_news.setEffectiveDate(DateTime())
        api.content.transition(obj=published_news, transition="publish")

        private_news = api.content.create(
            container=self.portal, type="News Item", title="Private news"
        )

        event = api.content.create(
            container=self.portal,
            type="Event",
            title="Event",
            start=datetime.now(),
            end=datetime.now(),
        )

        self.page = api.content.create(
            container=self.portal,
            type="Document",
            title="Page",
            relatedItems=[
                RelationValue(self.intids.getId(published_news)),
                RelationValue(self.intids.getId(private_news)),
                RelationValue(self.intids.getId(event)),
            ],
        )
        commit()

    def tearDown(self):
        self.api_session.close()
        self.api_session_anon.close()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_api_do_not_return_effective_on_private_items(self):
        response = self.api_session.get(self.page.absolute_url())

        result = response.json()
        relatedItems = result.get("relatedItems", [])
        self.assertEqual(len(relatedItems), 3)

        # published news
        self.assertIn("effective", relatedItems[0])
        self.assertIsNotNone(relatedItems[0]["effective"])

        # other contents
        self.assertIn("effective", relatedItems[1])
        self.assertIsNone(relatedItems[1]["effective"])
        self.assertIn("effective", relatedItems[2])
        self.assertIsNone(relatedItems[2]["effective"])

    def test_api_do_return_start_end_on_events(self):
        response = self.api_session.get(self.page.absolute_url())

        result = response.json()
        relatedItems = result.get("relatedItems", [])
        self.assertEqual(len(relatedItems), 3)

        # news
        self.assertNotIn("start", relatedItems[0])
        self.assertNotIn("end", relatedItems[0])
        self.assertNotIn("start", relatedItems[1])
        self.assertNotIn("end", relatedItems[1])

        # event
        self.assertIn("start", relatedItems[2])
        self.assertIn("end", relatedItems[2])

    def test_api_do_not_return_related_items_with_effective_date_in_future_for_anon(
        self,
    ):

        present = api.content.create(
            container=self.portal, type="Document", title="present"
        )
        future = api.content.create(
            container=self.portal, type="Document", title="future"
        )
        present.setEffectiveDate(DateTime())
        future.setEffectiveDate(DateTime() + 1)
        api.content.transition(obj=present, transition="publish")
        api.content.transition(obj=future, transition="publish")
        page = api.content.create(
            container=self.portal,
            type="Document",
            title="Page",
            relatedItems=[
                RelationValue(self.intids.getId(present)),
                RelationValue(self.intids.getId(future)),
            ],
        )
        api.content.transition(obj=page, transition="publish")
        commit()

        res = self.api_session.get(page.absolute_url()).json()

        relatedItems = res.get("relatedItems", [])
        self.assertEqual(len(relatedItems), 2)

        res_anon = self.api_session_anon.get(page.absolute_url()).json()
        self.assertEqual(len(res_anon["relatedItems"]), 1)

    def test_api_do_not_return_related_items_with_effective_date_in_future_for_users_that_cant_edit_context(  # noqa
        self,
    ):
        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret",
        )

        api_session = RelativeSession(self.portal_url)
        api_session.headers.update({"Accept": "application/json"})
        api_session.auth = ("foo", "secret")

        present = api.content.create(
            container=self.portal, type="Document", title="present"
        )
        future = api.content.create(
            container=self.portal, type="Document", title="future"
        )
        present.setEffectiveDate(DateTime())
        future.setEffectiveDate(DateTime() + 1)
        api.content.transition(obj=present, transition="publish")
        api.content.transition(obj=future, transition="publish")
        page = api.content.create(
            container=self.portal,
            type="Document",
            title="Page",
            relatedItems=[
                RelationValue(self.intids.getId(present)),
                RelationValue(self.intids.getId(future)),
            ],
        )
        api.content.transition(obj=page, transition="publish")
        commit()

        setRoles(self.portal, "foo", ["Reader"])
        commit()
        res = api_session.get(page.absolute_url()).json()

        relatedItems = res.get("relatedItems", [])
        self.assertEqual(len(relatedItems), 1)

        setRoles(self.portal, "foo", ["Editor"])
        commit()
        res = api_session.get(page.absolute_url()).json()

        relatedItems = res.get("relatedItems", [])
        self.assertEqual(len(relatedItems), 2)
