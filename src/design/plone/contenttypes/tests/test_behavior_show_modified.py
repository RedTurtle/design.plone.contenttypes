# -*- coding: utf-8 -*-

"""Setup tests for this package."""
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
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


class TestShowModifiedBehavior(unittest.TestCase):

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
        # reset do default
        api.portal.set_registry_record(
            "show_modified_default",
            False,
            interface=IDesignPloneSettings,
        )
        transaction.commit()

    def test_if_not_set_return_site_default(self):

        page = api.content.create(
            container=self.portal,
            type="Document",
            title="Test document",
        )
        transaction.commit()
        resp = self.api_session.get(page.absolute_url())

        self.assertTrue(getattr(page, "show_modified", None))
        self.assertTrue(resp.json().get("show_modified", None))

        api.portal.set_registry_record(
            "show_modified_default",
            False,
            interface=IDesignPloneSettings,
        )
        transaction.commit()

        resp = self.api_session.get(page.absolute_url())
        self.assertFalse(getattr(page, "show_modified", None))
        self.assertFalse(resp.json().get("show_modified", None))

    def test_if_set_will_override_default(self):

        page = api.content.create(
            container=self.portal,
            type="Document",
            title="Test document",
            show_modified=False,
        )
        transaction.commit()
        resp = self.api_session.get(page.absolute_url())

        self.assertFalse(getattr(page, "show_modified", None))
        self.assertFalse(resp.json().get("show_modified", None))
