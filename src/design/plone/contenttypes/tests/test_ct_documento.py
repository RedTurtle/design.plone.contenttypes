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

    def test_behaviors_enabled_for_documento(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Documento"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.dublincore",
                "plone.relateditems",
                "plone.locking",
                "plone.constraintypes",
                "plone.leadimage",
                "design.plone.contenttypes.behavior.argomenti_documento",
                "design.plone.contenttypes.behavior.descrizione_estesa_documento",
                "design.plone.contenttypes.behavior.additional_help_infos",
            ),
        )

    def test_event_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Document", "Modulo", "Link"),
            portal_types["Documento"].allowed_content_types,
        )
