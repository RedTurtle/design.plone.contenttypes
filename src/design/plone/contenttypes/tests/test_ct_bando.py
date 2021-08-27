# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from redturtle.bandi.interfaces.settings import IBandoSettings
from plone import api

import unittest


class TestBando(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

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
