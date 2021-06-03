# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)

import unittest


class TestCorrelatoInEvidenza(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.argomento = api.content.create(
            container=self.portal,
            type="Pagina Argomento",
            title="Argomento",
            icona="test-icon",
        )
        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )
        commit()
        intids = getUtility(IIntIds)

        self.document.correlato_in_evidenza = [
            RelationValue(intids.getId(self.argomento))
        ]
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_correlato_in_evidenza_also_return_icona_info(self):
        """
        """
        response = self.api_session.get(self.document.absolute_url())
        res = response.json()
        self.assertIn(
            "icona", res["correlato_in_evidenza"][0],
        )
        self.assertEqual(res["correlato_in_evidenza"][0]["icona"], "test-icon")
