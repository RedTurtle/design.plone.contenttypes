# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)  # noqa
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.restapi.testing import RelativeSession

import unittest

WIDGET_PROPERTY_CHECKS = {
    "tassonomia_argomenti": {
        "maximumSelectionSize": 20,
        "selectableTypes": ["Pagina Argomento"],
    },
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
    "dove_rivolgersi": {
        "maximumSelectionSize": 10,
        "selectableTypes": ["Venue", "UnitaOrganizzativa"],
    },
}


class TestServizio(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behaviors_enabled_for_servizio(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Servizio"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "design.plone.contenttypes.behavior.descrizione_estesa_servizio",
                "plone.locking",
                "plone.leadimage",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "collective.dexteritytextindexer",
            ),
        )


class TestServizioApi(unittest.TestCase):
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

    def test_sottotitolo_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            sottotitolo="sotto1",
        )

        res = api.content.find(SearchableText="sotto1")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_a_chi_si_rivolge_indexed_in_searchabletext(self):

        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            a_chi_si_rivolge=RichTextValue(
                raw="destinatari",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
        )

        res = api.content.find(SearchableText="destinatari")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_chi_puo_presentare_indexed_in_searchabletext(self):

        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            chi_puo_presentare=RichTextValue(
                raw="chi",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
        )

        res = api.content.find(SearchableText="chi")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_come_si_fa_indexed_in_searchabletext(self):

        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            come_si_fa=RichTextValue(
                raw="come",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
        )

        res = api.content.find(SearchableText="come")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_cosa_si_ottiene_indexed_in_searchabletext(self):

        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            cosa_si_ottiene=RichTextValue(
                raw="ottenere",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
        )

        res = api.content.find(SearchableText="ottenere")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_cosa_serve_indexed_in_searchabletext(self):

        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            cosa_serve=RichTextValue(
                raw="serve",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
        )

        res = api.content.find(SearchableText="serve")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_ulteriori_informazioni_indexed_in_searchabletext(self):

        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            ulteriori_informazioni=RichTextValue(
                raw="aiuto",
                mimeType="text/html",
                outputMimeType="text/html",
                encoding="utf-8",
            ),
        )

        res = api.content.find(SearchableText="aiuto")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())
