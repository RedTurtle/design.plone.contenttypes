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

import transaction
import unittest


class TestUpdateNoteBehavior(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    def test_is_enabled_in_bando(self):

        portal_types = api.portal.get_tool(name="portal_types")
        self.assertIn(
            "design.plone.contenttypes.behavior.update_note",
            portal_types["Bando"].behaviors,
        )

    def test_if_compiled_is_stored_in_metadata(self):
        bando = api.content.create(
            container=self.portal, type="Bando", title="Test Bando", update_note="Foo"
        )
        transaction.commit()
        resp = self.api_session.get(
            "/@search", params={"UID": bando.UID(), "metadata_fields": "update_note"}
        )

        res = resp.json()

        self.assertEqual(res["items"][0]["update_note"], bando.update_note)
