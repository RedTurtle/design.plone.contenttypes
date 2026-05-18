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

    def test_scadenziario_day_returns_events_for_specific_day(self):
        """Test @scadenziario-day endpoint returns events for a specific day."""
        now = datetime.now()
        target_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Create events on different days
        api.content.create(
            container=self.portal,
            type="Event",
            title="Event Today Morning",
            start=target_day.replace(hour=9),
            end=target_day.replace(hour=11),
        )

        api.content.create(
            container=self.portal,
            type="Event",
            title="Event Today Afternoon",
            start=target_day.replace(hour=14),
            end=target_day.replace(hour=16),
        )

        api.content.create(
            container=self.portal,
            type="Event",
            title="Event Tomorrow",
            start=(target_day + timedelta(days=1)).replace(hour=9),
            end=(target_day + timedelta(days=1)).replace(hour=11),
        )

        commit()

        # Query for events on the target day
        response = self.api_session.post(
            f"{self.portal_url}/@scadenziario-day",
            json={
                "query": [
                    {
                        "i": "start",
                        "o": ("plone.app.querystring.operation." "date.afterToday"),
                        "v": "",
                    }
                ]
            },
        ).json()

        date_key = target_day.strftime("%Y/%m/%d")
        self.assertIn(date_key, response["items"])
        self.assertEqual(len(response["items"][date_key]), 2)

        titles = [item["title"] for item in response["items"][date_key]]
        self.assertIn("Event Today Morning", titles)
        self.assertIn("Event Today Afternoon", titles)

    def test_scadenziario_day_includes_related_places(self):
        """Test @scadenziario-day includes related places (luoghi_correlati)."""
        from z3c.relationfield import RelationValue
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds

        now = datetime.now()
        target_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Create a venue
        venue = api.content.create(
            container=self.portal,
            type="Venue",
            title="Test Venue",
        )

        # Create event with related places
        event = api.content.create(
            container=self.portal,
            type="Event",
            title="Event with Venue",
            start=target_day.replace(hour=9),
            end=target_day.replace(hour=11),
        )

        # Set the related places (luoghi_correlati) using the behavior
        intids = getUtility(IIntIds)
        venue_id = intids.getId(venue)
        event.luoghi_correlati = [RelationValue(venue_id)]

        event.reindexObject()
        commit()

        response = self.api_session.post(
            f"{self.portal_url}/@scadenziario-day",
            json={
                "query": [
                    {
                        "i": "start",
                        "o": ("plone.app.querystring.operation." "date.afterToday"),
                        "v": "",
                    }
                ]
            },
        ).json()

        date_key = target_day.strftime("%Y/%m/%d")
        event_data = response["items"][date_key][0]

        # Check that luoghi_correlati is present and correct
        self.assertIn("luoghi_correlati", event_data)
        self.assertEqual(len(event_data["luoghi_correlati"]), 1)
        self.assertEqual(
            event_data["luoghi_correlati"][0]["name"],
            "Test Venue",
        )
        self.assertIn(venue.id, event_data["luoghi_correlati"][0]["url"])

    def test_scadenziario_day_includes_parent_event(self):
        """Test @scadenziario-day includes parent event (rassegna) info."""
        now = datetime.now()
        target_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Create parent event (rassegna)
        parent_event = api.content.create(
            container=self.portal,
            type="Event",
            title="Rassegna Events",
            start=target_day.replace(hour=8),
            end=(target_day + timedelta(days=7)).replace(hour=18),
        )

        # Create child event inside parent event
        child_event = api.content.create(
            container=parent_event,
            type="Event",
            title="Child Event",
            start=target_day.replace(hour=9),
            end=target_day.replace(hour=11),
        )

        child_event.reindexObject()
        parent_event.reindexObject()
        commit()

        response = self.api_session.post(
            f"{self.portal_url}/@scadenziario-day",
            json={
                "query": [
                    {
                        "i": "start",
                        "o": "plone.app.querystring.operation.date.afterToday",
                        "v": "",
                    }
                ]
            },
        ).json()

        date_key = target_day.strftime("%Y/%m/%d")
        # Find the child event in the results
        event_data = None
        for item in response["items"].get(date_key, []):
            if item["title"] == "Child Event":
                event_data = item
                break

        self.assertIsNotNone(event_data)
        # Check that parent_event is present and correct
        self.assertIn("parent_event", event_data)
        self.assertEqual(event_data["parent_event"]["name"], "Rassegna Events")
        self.assertIn(parent_event.id, event_data["parent_event"]["url"])

    def test_scadenziario_day_without_related_places_or_parent(self):
        """Test @scadenziario-day event without related places or parent."""
        now = datetime.now()
        target_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Create standalone event
        event = api.content.create(
            container=self.portal,
            type="Event",
            title="Standalone Event",
            start=target_day.replace(hour=9),
            end=target_day.replace(hour=11),
        )

        event.reindexObject()
        commit()

        response = self.api_session.post(
            f"{self.portal_url}/@scadenziario-day",
            json={
                "query": [
                    {
                        "i": "start",
                        "o": "plone.app.querystring.operation.date.afterToday",
                        "v": "",
                    }
                ]
            },
        ).json()

        date_key = target_day.strftime("%Y/%m/%d")
        event_data = response["items"][date_key][0]

        # Check that luoghi_correlati and parent_event are NOT in the response
        # (or empty if present)
        self.assertFalse(event_data.get("luoghi_correlati"))
        self.assertFalse(event_data.get("parent_event"))
