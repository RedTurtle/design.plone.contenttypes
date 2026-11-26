# -*- coding: utf-8 -*-

from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from design.plone.contenttypes.tests.utils import fieldsets_ids
from design.plone.contenttypes.tests.utils import get_fieldset_fields
from design.plone.contenttypes.tests.utils import PLONE_61
from design.plone.contenttypes.tests.utils import PLONE_VOLTO_5
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession

import unittest


class TestDocumentSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_document(self):
        portal_types = api.portal.get_tool(name="portal_types")
        expected = [
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
        ]
        if PLONE_61:
            expected.remove("plone.allowdiscussion")
        if PLONE_VOLTO_5:
            idx = expected.index("volto.blocks")
            expected[idx:idx] = ["volto.preview_image_link", "volto.navtitle"]
        self.assertEqual(portal_types["Document"].behaviors, tuple(expected))

    def test_document_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            fieldsets_ids(
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
                ]
            ),
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
            get_fieldset_fields(resp, "default"),
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
            get_fieldset_fields(resp, "testata"),
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

    def test_document_preview_image_only_in_testata_fieldset(self):
        """
        preview_image is moved in "testata" and preview_caption is hidden:
        with plone.volto 5+ they are not in "default" but in "preview_image".
        """
        resp = self.api_session.get("@types/Document").json()
        fields = [x for fieldset in resp["fieldsets"] for x in fieldset["fields"]]
        self.assertEqual(fields.count("preview_image"), 1)
        self.assertNotIn("preview_caption", fields)
        if PLONE_VOLTO_5:
            self.assertEqual(
                get_fieldset_fields(resp, "preview_image"),
                ["preview_image_link", "preview_caption_link"],
            )

    def test_document_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        expected = [
            "allow_discussion",
            "exclude_from_nav",
            "id",
            "versioning_enabled",
            "show_modified",
            "exclude_from_search",
            "changeNote",
        ]
        if PLONE_61:
            expected.remove("allow_discussion")
        if PLONE_VOLTO_5:
            expected.insert(expected.index("id") + 1, "nav_title")
        self.assertEqual(get_fieldset_fields(resp, "settings"), expected)

    def test_document_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            get_fieldset_fields(resp, "correlati"),
            ["correlato_in_evidenza"],
        )

    def test_document_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            get_fieldset_fields(resp, "categorization"),
            ["subjects", "language", "relatedItems"],
        )

    def test_document_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(get_fieldset_fields(resp, "dates"), ["effective", "expires"])

    def test_document_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            get_fieldset_fields(resp, "ownership"),
            ["creators", "contributors", "rights"],
        )

    def test_document_fields_layout_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            get_fieldset_fields(resp, "layout"), ["blocks", "blocks_layout"]
        )

    def test_document_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            get_fieldset_fields(resp, "seo"),
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
