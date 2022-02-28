# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.bandi.interfaces.settings import IBandoSettings

import unittest


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
