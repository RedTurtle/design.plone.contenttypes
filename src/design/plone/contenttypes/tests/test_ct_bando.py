# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from redturtle.bandi.interfaces.settings import IBandoSettings

import unittest


class TestBandoSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_bando(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Bando"].behaviors,
            (
                "plone.app.content.interfaces.INameFromTitle",
                "plone.app.dexterity.behaviors.discussion.IAllowDiscussion",
                "plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation",
                "plone.app.dexterity.behaviors.id.IShortName",
                "plone.app.dexterity.behaviors.metadata.IDublinCore",
                "plone.app.relationfield.behavior.IRelatedItems",
                "plone.app.versioningbehavior.behaviors.IVersionable",
                "plone.app.contenttypes.behaviors.tableofcontents.ITableOfContents",
                "plone.app.lockingbehavior.behaviors.ILocking",
                "Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes",
                "plone.versioning",
                "design.plone.contenttypes.behavior.argomenti_bando",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "design.plone.contenttypes.behavior.update_note",
                "volto.preview_image",
            ),
        )

    def test_bando_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(len(resp["fieldsets"]), 7)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "correlati",
                "settings",
                "categorization",
                "dates",
                "ownership",
                "seo",
            ],
        )

    def test_bando_required_fields(self):
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "tipologia_bando"]),
        )

    def test_bando_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "text",
                "tipologia_bando",
                "destinatari",
                "ente_bando",
                "apertura_bando",
                "scadenza_domande_bando",
                "scadenza_bando",
                "chiusura_procedimento_bando",
                "riferimenti_bando",
                "update_note",
                "preview_image",
                "preview_caption",
            ],
        )

    def test_bando_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "area_responsabile",
                "ufficio_responsabile",
                "tassonomia_argomenti",
                "correlato_in_evidenza",
            ],
        )

    def test_bando_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "table_of_contents",
                "changeNote",
            ],
        )

    def test_bando_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            ["subjects", "language", "relatedItems"],
        )

    def test_bando_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(resp["fieldsets"][4]["fields"], ["effective", "expires"])

    def test_bando_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"], ["creators", "contributors", "rights"]
        )

    def test_bando_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            [
                "seo_title",
                "seo_description",
                "seo_noindex",
                "seo_canonical_url",
                "opengraph_title",
                "opengraph_description",
                "opengraph_image",
            ],
        )


class TestBando(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_bando_folder_deepening_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("File", "Link", "Modulo"),
            portal_types["Bando Folder Deepening"].allowed_content_types,
        )

    def test_bando_view_base(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(portal_types["Bando"].default_view, "view")
        self.assertEqual(portal_types["Bando"].view_methods, ("view",))

    def test_disabled_default_ente(self):
        default_ente = api.portal.get_registry_record(
            "default_ente", interface=IBandoSettings
        )
        self.assertEqual(default_ente, ())

    def test_bando_substructure_created(self):
        bando = api.content.create(container=self.portal, type="Bando", title="Bando")

        self.assertIn("documenti", bando.keys())
        self.assertIn("comunicazioni", bando.keys())
        self.assertIn("esiti", bando.keys())
