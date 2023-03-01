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
                "plone.leadimage",
                "volto.preview_image",
            ),
        )
