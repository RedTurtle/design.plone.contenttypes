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

import transaction
import unittest
import io
import os


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
                "collective.geolocationbehavior.geolocation.IGeolocatable",
                "design.plone.contenttypes.behaviors.luogo.ILuogo",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.servizi_correlati",
            ),
        )

    def test_luogo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Luogo", portal_types["Venue"].title)


class TestLuogoApi(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "image.jpg")
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    def test_newsitem_required_fields(self):

        response = self.api_session.post(
            self.portal_url, json={"@type": "Venue", "title": "Foo"}
        )

        self.assertEqual(400, response.status_code)
        message = response.json()["message"]
        self.assertIn("descrizione_breve", message)
        self.assertIn("modalita_accesso", message)
        self.assertIn("identificativo_mibac", message)
        self.assertIn("immagine", message)
        self.assertIn("indirizzo", message)
        self.assertIn("cap", message)

        with io.FileIO(self.file_path, "rb") as f:

            response = self.api_session.post(
                self.portal_url,
                json={
                    "@type": "Venue",
                    "title": "Foo",
                    "descrizione_breve": "xxx",
                    "modalita_accesso": "xxx",
                    "identificativo_mibac": "xxx",
                    "immagine": f,
                    "indirizzo": "xxx",
                    "cap": "xxx",
                },
            )
            self.assertEqual(201, response.status_code)

    def test_newsitem_substructure_created(self):
        with io.FileIO(self.file_path, "rb") as f:
            self.api_session.post(
                self.portal_url,
                json={
                    "@type": "Venue",
                    "title": "Foo",
                    "descrizione_breve": "xxx",
                    "modalita_accesso": "xxx",
                    "identificativo_mibac": "xxx",
                    "immagine": f,
                    "indirizzo": "xxx",
                    "cap": "xxx",
                },
            )

            transaction.commit()
            news = self.portal["foo"]

            self.assertEqual(["multimedia"], news.keys())

            self.assertEqual(news["multimedia"].portal_type, "Document")
            self.assertEqual(news["multimedia"].constrain_types_mode, 1)
            self.assertEqual(
                news["multimedia"].locally_allowed_types, ("Link", "Image")
            )

