# -*- coding: utf-8 -*-
from DateTime import DateTime
from datetime import datetime
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
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

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

        intids = getUtility(IIntIds)
        self.page = api.content.create(
            container=self.portal,
            type="Document",
            title="Page",
            relatedItems=[
                RelationValue(intids.getId(published_news)),
                RelationValue(intids.getId(private_news)),
                RelationValue(intids.getId(event)),
            ],
        )
        commit()

    def tearDown(self):
        self.api_session.close()

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
