# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from design.plone.contenttypes.restapi.services.types.get import (
    FIELDSETS_ORDER,
)
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone import api
from plone.restapi.testing import RelativeSession
from design.plone.contenttypes.controlpanels.vocabularies import (
    IVocabulariesControlPanel,
)
from transaction import commit
import unittest


class TestContentTypes(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        api.portal.set_registry_record(
            "lead_image_dimension",
            ["News Item|1920x600"],
            interface=IVocabulariesControlPanel,
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_persona_fieldset_order(self):
        response = self.api_session.get("/@types/Persona")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertEqual(ids, FIELDSETS_ORDER["Persona"])

    def test_news_item_fieldset_order(self):
        response = self.api_session.get("/@types/News%20Item")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertEqual(ids, FIELDSETS_ORDER["News Item"])

    def test_event_fieldset_order(self):
        response = self.api_session.get("/@types/Event")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertEqual(ids, FIELDSETS_ORDER["Event"])

    def test_servizio_fieldset_order(self):
        response = self.api_session.get("/@types/Servizio")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertEqual(ids, FIELDSETS_ORDER["Servizio"])

    def test_unitaorganizzativa_fieldset_order(self):
        response = self.api_session.get("/@types/UnitaOrganizzativa")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertEqual(ids, FIELDSETS_ORDER["UnitaOrganizzativa"])

    def test_venue_fieldset_order(self):
        response = self.api_session.get("/@types/Venue")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertEqual(ids, FIELDSETS_ORDER["Venue"])

    def test_image_field_description(self):
        response = self.api_session.get("/@types/News%20Item")
        res = response.json()
        self.assertEqual(
            res["properties"]["image"]["description"],
            "Image dimension should be 1920x600 px",
        )

    # schema overrides aggiunge correlati ma dai test non si vede
    # def test_testata_fieldset_order(self):
    #     response = self.api_session.get("/@types/Document")
    #     res = response.json()

    #     ids = [x["id"] for x in res["fieldsets"]]
    #     self.assertIn("testata", ids)
    #     self.assertEqual(ids, FIELDSETS_ORDER["Document"])
