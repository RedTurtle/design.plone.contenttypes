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
from plone.restapi.testing import RelativeSession

import unittest

WIDGET_PROPERTY_CHECKS = {
    "tassonomia_argomenti": {"selectableTypes": ["Pagina Argomento"]},
    "ufficio_responsabile": {
        "maximumSelectionSize": 1,
        "selectableTypes": ["UnitaOrganizzativa"],
    },
    "area": {
        "maximumSelectionSize": 1,
        "selectableTypes": ["UnitaOrganizzativa"],
    },
    "altri_documenti": {
        "maximumSelectionSize": 10,
        "selectableTypes": ["Documento"],
    },
    "servizi_collegati": {
        "maximumSelectionSize": 10,
        "selectableTypes": ["Servizio"],
    },
    "sedi_e_luoghi": {
        "maximumSelectionSize": 10,
        "selectableTypes": ["Venue"],
    },
}

FIELDS_IN_CORRELATI_TAB = [
    "servizi_collegati",
    "ufficio_responsabile",
    "area",
    "altri_documenti",
]


class TestServizio(unittest.TestCase):
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

    def tearDown(self):
        self.api_session.close()

    def test_related_widgets(self):
        response = self.api_session.get("/@types/Servizio")
        res = response.json()
        properties = res["properties"]
        for field in WIDGET_PROPERTY_CHECKS:
            self.assertTrue(
                properties[field]["widgetOptions"]["pattern_options"]
                == WIDGET_PROPERTY_CHECKS[field]
            )
            self.assertTrue(properties[field]["type"] == "array")

    def test_related_widgets_are_in_related_tab(self):
        response = self.api_session.get("/@types/Servizio")
        res = response.json()
        for fieldset in res["fieldsets"]:
            if fieldset["id"] == "correlati":
                for field in FIELDS_IN_CORRELATI_TAB:
                    self.assertTrue(field in fieldset["fields"])
