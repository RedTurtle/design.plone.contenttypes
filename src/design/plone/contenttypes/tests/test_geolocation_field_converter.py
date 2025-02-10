# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.formwidget.geolocation import Geolocation
from plone.restapi.testing import RelativeSession
from transaction import commit


import unittest


class TestGeolocationFieldConverter(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    def test_geolocation_null_if_not_set(self):
        api.content.create(container=self.portal, type="Venue", title="venue1")
        commit()

        response = self.api_session.get("/venue1").json()
        self.assertIsNone(response["geolocation"])

    def test_geolocation_null_if_set_to_zero(self):
        api.content.create(
            container=self.portal,
            type="Venue",
            title="venue1",
            geolocation=Geolocation(0.0, 0.0),
        )
        commit()

        response = self.api_session.get("/venue1").json()
        self.assertIsNone(response["geolocation"])

    def test_geolocation_with_value_if_set(self):
        api.content.create(
            container=self.portal,
            type="Venue",
            title="venue1",
            geolocation=Geolocation(2.0, 2.0),
        )
        commit()

        response = self.api_session.get("/venue1").json()
        self.assertEqual(response["geolocation"], {"latitude": 2.0, "longitude": 2.0})
