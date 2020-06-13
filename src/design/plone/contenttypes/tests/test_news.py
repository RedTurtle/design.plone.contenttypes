# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api

import unittest


class TestNews(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_news(self):
        portal_types = api.portal.get_tool(name="portal_types")

        self.assertEqual(
            portal_types["News Item"].behaviors,
            (
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "volto.blocks",
                "design.plone.contenttypes.behavior.news",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.luoghi_correlati",
                "design.plone.contenttypes.behavior.dataset_correlati",
                "design.plone.contenttypes.behavior.servizi_correlati",
            ),
        )

    def test_news_item_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            "Notizie e comunicati stampa", portal_types["News Item"].title
        )

    def test_news_item_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Image", "File", "Link", "Document"),
            portal_types["News Item"].allowed_content_types,
        )
