# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
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


class ScadenziarioTest(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        commit()

    def tearDown(self):
        self.api_session.close()

    def test_return_future_events_if_query_is_end_after_today(self):
        now = datetime.now()

        # past event
        api.content.create(
            container=self.portal,
            type="Event",
            title="Past event",
            start=now.replace(hour=8) + timedelta(days=-2),
            end=now.replace(hour=18) + timedelta(days=-2),
        )

        future_event_1 = api.content.create(
            container=self.portal,
            type="Event",
            title="Future event",
            start=now.replace(hour=8) + timedelta(days=2),
            end=now.replace(hour=18) + timedelta(days=4),
        )
        future_event_2 = api.content.create(
            container=self.portal,
            type="Event",
            title="Future event that starts in the past",
            start=now.replace(hour=8) + timedelta(days=-4),
            end=now.replace(hour=18) + timedelta(days=4),
        )

        commit()

        response = self.api_session.post(
            f"{self.portal_url}/@scadenziario",
            json={
                "query": [
                    {
                        "i": "end",
                        "o": "plone.app.querystring.operation.date.afterToday",
                        "v": "",
                    }
                ]
            },
        ).json()
        self.assertEqual(len(response["items"]), 2)

        # results are in asc order
        self.assertEqual(
            response["items"][0],
            future_event_2.start.strftime("%Y/%m/%d"),
        )
        self.assertEqual(
            response["items"][1],
            future_event_1.start.strftime("%Y/%m/%d"),
        )
