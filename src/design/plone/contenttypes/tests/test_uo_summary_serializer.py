# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.formwidget.geolocation import Geolocation
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import getMultiAdapter

import unittest


class UOSummarySerializerTest(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]

    def test_geolocation_injected(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
            geolocation=Geolocation(25, 25),
        )

        summary = getMultiAdapter(
            (uo, self.layer["request"]), ISerializeToJsonSummary
        )()

        self.assertDictEqual(
            {
                "longitude": uo.geolocation.longitude,
                "latitude": uo.geolocation.latitude,
            },
            summary["geolocation"],
        )
