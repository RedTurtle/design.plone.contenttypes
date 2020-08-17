# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
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

    def test_persona_correlati_fieldset_order(self):
        response = self.api_session.get("/@types/Persona")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertIn("correlati", ids)
        self.assertEqual(
            ids,
            [
                "default",
                "correlati",
                "categorization",
                "settings",
                "ownership",
                "dates",
            ],
        )

    def test_news_correlati_fieldset_order(self):
        response = self.api_session.get("/@types/News%20Item")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]

        self.assertIn("correlati", ids)
        self.assertEqual(
            ids,
            [
                "default",
                "correlati",
                "categorization",
                "dates",
                "ownership",
                "settings",
                "layout",
            ],
        )

    def test_image_field_description(self):
        response = self.api_session.get("/@types/News%20Item")
        res = response.json()
        self.assertEqual(
            res["properties"]["image"]["description"],
            "Image dimension should be 1920x600 px",
        )

    def test_testata_fieldset_order(self):
        response = self.api_session.get("/@types/Document")
        res = response.json()

        ids = [x["id"] for x in res["fieldsets"]]
        self.assertIn("testata", ids)
        self.assertEqual(
            ids,
            [
                "default",
                "testata",
                "settings",
                "categorization",
                "dates",
                "ownership",
                "layout",
            ],
        )
