# -*- coding: utf-8 -*-

from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
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


class TestLuogo(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_luogo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Venue"].behaviors,
            (
                "plone.app.content.interfaces.INameFromTitle",
                "plone.app.dexterity.behaviors.metadata.IBasic",
                "plone.app.dexterity.behaviors.metadata.ICategorization",
                "collective.address.behaviors.IAddress",
                "collective.geolocationbehavior.geolocation.IGeolocatable",
                "design.plone.contenttypes.behaviors.luogo.ILuogo",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.servizi_correlati",
                "design.plone.contenttypes.behavior.argomenti",
                "plone.leadimage",
            ),
        )

    def test_luogo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Luogo", portal_types["Venue"].title)


class TestLuogoApi(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    def test_venue_required_fields(self):

        response = self.api_session.post(
            self.portal_url, json={"@type": "Venue", "title": "Foo"}
        )

        self.assertEqual(400, response.status_code)
        message = response.json()["message"]
        self.assertIn("descrizione_breve", message)
        self.assertIn("modalita_accesso", message)
        self.assertIn("identificativo_mibac", message)

    def test_venue_geolocation_deserializer_wrong_structure(self):
        venue = api.content.create(
            container=self.portal, type="Venue", title="Example venue"
        )

        commit()
        self.assertEqual(venue.geolocation, None)

        response = self.api_session.patch(
            venue.absolute_url(),
            json={"@type": "Venue", "title": "Foo", "geolocation": {"foo": "bar"}},
        )
        message = response.json()["message"]

        self.assertEqual(400, response.status_code)
        self.assertIn("Invalid geolocation data", message)
        self.assertEqual(venue.geolocation, None)

    def test_venue_geolocation_deserializer_right_structure(self):
        venue = api.content.create(
            container=self.portal, type="Venue", title="Example venue"
        )

        commit()
        self.assertEqual(venue.geolocation, None)

        response = self.api_session.patch(
            venue.absolute_url(),
            json={
                "@type": "Venue",
                "title": "Foo",
                "geolocation": {"latitude": 11.0, "longitude": 10.0},
            },
        )
        commit()

        self.assertEqual(204, response.status_code)
        self.assertEqual(venue.geolocation.latitude, 11.0)
        self.assertEqual(venue.geolocation.longitude, 10.0)

    def test_venue_default_values_for_location(self):
        response = self.api_session.get("/@types/Venue")
        schema = response.json()["properties"]
        self.assertEqual(
            schema["country"]["default"], {"title": "Italia", "token": "380"}
        )
        self.assertEqual(schema["city"]["default"], "Roma")
        self.assertEqual(schema["street"]["default"], "Via Liszt, 21")
        self.assertEqual(
            schema["geolocation"]["default"],
            {"latitude": 41.8337833, "longitude": 12.4677863},
        )
