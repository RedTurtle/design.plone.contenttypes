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
