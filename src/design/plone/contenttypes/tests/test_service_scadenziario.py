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

        # multi-day events must produce one entry for every day they span,
        # from their start date up to (and including) their end date.
        expected_days = set()
        for event in (future_event_1, future_event_2):
            day = event.start.date()
            end_day = event.end.date()
            while day <= end_day:
                expected_days.add(day.strftime("%Y/%m/%d"))
                day += timedelta(days=1)

        self.assertEqual(set(response["items"]), expected_days)
        # results are in asc order
        self.assertEqual(response["items"], sorted(response["items"]))


class ScadenziarioDayTest(unittest.TestCase):
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

    def query_day(self, day):
        day_start = day.strftime("%Y/%m/%d 00:00")
        day_end = day.strftime("%Y/%m/%d 23:59")
        return self.api_session.post(
            f"{self.portal_url}/@scadenziario-day",
            json={
                "query": [
                    {
                        "i": "portal_type",
                        "o": "plone.app.querystring.operation.selection.any",
                        "v": ["Event"],
                    },
                    {
                        "i": "start",
                        "o": "plone.app.querystring.operation.date.between",
                        "v": [day_start, day_end],
                    },
                ],
                "sort_on": "start",
                "sort_order": "ascending",
            },
        ).json()

    def test_multi_day_event_is_returned_for_every_day_it_spans(self):
        now = datetime.now()
        start = now.replace(hour=13, minute=0, second=0, microsecond=0)
        end = (now + timedelta(days=23)).replace(
            hour=14, minute=0, second=0, microsecond=0
        )

        api.content.create(
            container=self.portal,
            type="Event",
            title="Multi-day event",
            start=start,
            end=end,
        )

        commit()

        # start day, an in-between day and the end day must all return the
        # event, not just the day it starts on.
        for offset in (0, 1, 10, 23):
            day = now + timedelta(days=offset)
            response = self.query_day(day)
            day_key = day.strftime("%Y/%m/%d")
            self.assertIn(day_key, response["items"])
            titles = [item["title"] for item in response["items"][day_key]]
            self.assertIn("Multi-day event", titles)

        # the day after the event ends must not return it.
        response = self.query_day(now + timedelta(days=24))
        day_key = (now + timedelta(days=24)).strftime("%Y/%m/%d")
        titles = [item["title"] for item in response["items"].get(day_key, [])]
        self.assertNotIn("Multi-day event", titles)

    def test_recurring_event_uses_occurrence_dates_not_master_span(self):
        # a recurring event whose own start-end spans two days: the
        # recurrence must take precedence over that raw interval, so each
        # occurrence must be found only on its own recurrence date, not on
        # every day between the master event's start and end.
        now = datetime.now()
        start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end = (now + timedelta(days=1)).replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        api.content.create(
            container=self.portal,
            type="Event",
            title="Recurring event",
            start=start,
            end=end,
            recurrence="RRULE:FREQ=WEEKLY;COUNT=3",
        )
        commit()

        occurrence_days = {
            (start + timedelta(weeks=week)).strftime("%Y/%m/%d") for week in range(3)
        }

        # day after the first occurrence: within the master event's raw
        # start-end span, but not an actual occurrence date, so must be
        # absent from the found event days.
        day_after_first_occurrence = (start + timedelta(days=1)).strftime("%Y/%m/%d")

        # @scadenziario
        response = self.api_session.post(
            f"{self.portal_url}/@scadenziario",
            json={
                "query": [
                    {
                        "i": "portal_type",
                        "o": "plone.app.querystring.operation.selection.any",
                        "v": ["Event"],
                    },
                    {
                        "i": "path",
                        "o": "plone.app.querystring.operation.string.relativePath",
                        "v": "./",
                    },
                ],
                "sort_on": "start",
                "sort_order": "ascending",
                "b_size": 100,
            },
        ).json()
        self.assertEqual(set(response["items"]), occurrence_days)
        self.assertNotIn(day_after_first_occurrence, response["items"])

        # @scadenziario-day: found on each occurrence date...
        for occurrence_day in occurrence_days:
            day_response = self.query_day(datetime.strptime(occurrence_day, "%Y/%m/%d"))
            self.assertIn(occurrence_day, day_response["items"])

        # ...but not on the day after the first occurrence, even though
        # it's still within the master event's own start-end interval.
        day_response = self.query_day(start + timedelta(days=1))
        titles = [
            item["title"]
            for item in day_response["items"].get(day_after_first_occurrence, [])
        ]
        self.assertNotIn("Recurring event", titles)
