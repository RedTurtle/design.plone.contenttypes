# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.utils import createContentInContainer
from plone.restapi.testing import RelativeSession
from transaction import commit
from unittest import mock

import unittest


class CustomNavigationTest(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.folder = createContentInContainer(
            self.portal, "Folder", id="folder", title="Some Folder"
        )
        self.folder2 = createContentInContainer(
            self.portal, "Folder", id="folder2", title="Some Folder 2"
        )
        self.subfolder1 = createContentInContainer(
            self.folder, "Folder", id="subfolder1", title="SubFolder 1"
        )
        self.subfolder2 = createContentInContainer(
            self.folder, "Folder", id="subfolder2", title="SubFolder 2"
        )
        self.thirdlevelfolder = createContentInContainer(
            self.subfolder1,
            "Folder",
            id="thirdlevelfolder",
            title="Third Level Folder",
        )
        self.fourthlevelfolder = createContentInContainer(
            self.thirdlevelfolder,
            "Folder",
            id="fourthlevelfolder",
            title="Fourth Level Folder",
        )
        createContentInContainer(self.folder, "Document", id="doc1", title="A document")
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_return_show_in_footer_info_based_on_registry(self):
        # by default is True
        response = self.api_session.get(
            "/@navigation", params={"expand.navigation.depth": 2}
        ).json()

        self.assertIn("show_in_footer", response)
        self.assertTrue(response["show_in_footer"])

        # change it
        api.portal.set_registry_record(
            "show_dynamic_folders_in_footer",
            False,
            interface=IDesignPloneSettings,
        )
        commit()

        response = self.api_session.get(
            "/@navigation", params={"expand.navigation.depth": 2}
        ).json()

        self.assertIn("show_in_footer", response)
        self.assertFalse(response["show_in_footer"])

    def test_navigation_extends_redturtle_volto_navigation(self):
        from design.plone.contenttypes.restapi.services.navigation.get import (
            Navigation,
        )
        from redturtle.volto.restapi.services.navigation.navigation import (
            Navigation as RTNavigation,
        )

        self.assertTrue(issubclass(Navigation, RTNavigation))

    def test_navigation_depth_is_limited(self):
        # registry plone.navigation_depth default is 3, fixture has 4 levels
        response = self.api_session.get(
            "/@navigation", params={"expand.navigation.depth": 70}
        ).json()

        self.assertEqual(tree_depth(response["items"]), 3)
        self.assertIn("show_in_footer", response)

    def test_navigation_expander_depth_is_limited(self):
        response = self.api_session.get(
            "/", params={"expand": "navigation", "expand.navigation.depth": 70}
        ).json()
        navigation = response["@components"]["navigation"]

        self.assertEqual(tree_depth(navigation["items"]), 3)
        self.assertIn("show_in_footer", navigation)

    def test_navigation_depth_within_limit_is_unchanged(self):
        response = self.api_session.get(
            "/@navigation", params={"expand.navigation.depth": 2}
        ).json()

        self.assertEqual(tree_depth(response["items"]), 2)

    def test_navigation_invalid_depth_returns_400(self):
        response = self.api_session.get(
            "/@navigation", params={"expand.navigation.depth": "foo"}
        )

        self.assertEqual(response.status_code, 400)

    def test_navigation_items_are_capped_by_whole_levels(self):
        with mock.patch("redturtle.volto.config.MAX_NAVIGATION_ITEMS", 4):
            response = self.api_session.get(
                "/@navigation", params={"expand.navigation.depth": 3}
            ).json()

        self.assertIn("show_in_footer", response)
        # level 1 is always kept, deeper levels that do not fit are cut
        self.assertEqual(tree_depth(response["items"]), 1)
        for item in response["items"]:
            self.assertEqual(item["items"], [])


def tree_depth(items):
    """Number of nested levels in a navigation tree."""
    if not items:
        return 0
    return 1 + max(tree_depth(item.get("items") or []) for item in items)
