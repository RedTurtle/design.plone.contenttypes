# -*- coding: utf-8 -*-

from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
import unittest


class TestDocument(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_document(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Document"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.dublincore",
                "plone.relateditems",
                "plone.locking",
                "volto.blocks",
                "plone.versioning",
                "design.plone.contenttypes.behavior.info_testata",
                "design.plone.contenttypes.behavior.argomenti_document",
                "plone.translatable",
                "design.plone.contenttypes.behavior.show_modified",
                "kitconcept.seo",
                "plone.constraintypes",
                "design.plone.contenttypes.behavior.exclude_from_search",
                "plone.leadimage",
                "volto.preview_image",
            ),
        )

    def test_document_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(len(resp["fieldsets"]), 9)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "testata",
                "settings",
                "correlati",
                "categorization",
                "dates",
                "ownership",
                "layout",
                "seo",
            ],
        )

    def test_document_required_fields(self):
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title"]),
        )

    def test_document_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
            ],
        )

    def test_document_fields_testata_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "image",
                "image_caption",
                "preview_image",
                "ricerca_in_testata",
                "mostra_bottoni_condivisione",
                "info_testata",
                "mostra_navigazione",
                "tassonomia_argomenti",
            ],
        )

    def test_document_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "show_modified",
                "exclude_from_search",
                "changeNote",
            ],
        )

    def test_document_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            ["correlato_in_evidenza"],
        )

    def test_document_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"], ["subjects", "language", "relatedItems"]
        )

    def test_document_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["effective", "expires"])

    def test_document_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"], ["creators", "contributors", "rights"]
        )

    def test_document_fields_layout_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["blocks", "blocks_layout"])

    def test_document_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
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
