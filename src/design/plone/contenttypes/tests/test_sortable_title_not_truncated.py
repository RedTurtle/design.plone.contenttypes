# -*- coding: utf-8 -*-

"""Setup tests for this package."""
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone.indexer.interfaces import IIndexableObject
from zope.component import queryMultiAdapter

import unittest


class TestSortableTitle(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_sortable_title_not_truncated(self):
        title = (
            "Super loooooooong title that is more than fourty characters and counting"
        )
        doc = api.content.create(type="Document", title=title, container=self.portal)

        catalog = api.portal.get_tool(name="portal_catalog")
        adapter = queryMultiAdapter((doc, catalog), IIndexableObject)

        self.assertEqual(len(adapter.sortable_title), len(title))
