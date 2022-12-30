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

import unittest


class TestDescrizioneEstesaBehavior(unittest.TestCase):

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

    def test_descrizione_estesa_indexed(self):

        # Servizio have design.plone.contenttypes.behavior.descrizione_estesa
        # behavior
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            descrizione_estesa={"blocks": {"12345": {"searchableText": "foo"}}},
        )

        res = api.content.find(SearchableText="foo")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())
