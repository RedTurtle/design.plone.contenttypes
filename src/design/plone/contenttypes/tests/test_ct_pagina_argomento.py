# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import unittest


class TestPaginaArgomentoSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_pagina_argomento(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Pagina Argomento"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.relateditems",
                "plone.categorization",
                "plone.basic",
                "plone.locking",
                "plone.leadimage",
                "volto.preview_image",
                "plone.textindexer",
                "volto.blocks",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
            ),
        )

    def test_pagina_argomento_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(len(resp["fieldsets"]), 8)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "informazioni",
                # "correlati", questo non viene fuori nei test
                "categorization",
                "dates",
                "settings",
                "layout",
                "ownership",
                "seo",
            ],
        )

    def test_pagina_argomento_required_fields(self):
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                ]
            ),
        )

    def test_pagina_argomento_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "icona",
                "unita_amministrative_responsabili",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
            ],
        )

    def test_pagina_argomento_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][1]["fields"], ["ulteriori_informazioni"])

    def test_pagina_argomento_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"], ["relatedItems", "subjects", "language"]
        )

    def test_pagina_argomento_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][3]["fields"], ["effective", "expires"])

    def test_pagina_argomento_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_pagina_argomento_fields_layout_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["blocks", "blocks_layout"])

    def test_pagina_argomento_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"], ["creators", "contributors", "rights"]
        )

    def test_pagina_argomento_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
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
