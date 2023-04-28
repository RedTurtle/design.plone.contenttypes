# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.formwidget.geolocation import Geolocation
from plone.namedfile.file import NamedBlobImage
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import os
import unittest


class UOSummarySerializerTest(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

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

    def test_pdc_and_location(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
        )
        uo2 = api.content.create(
            container=uo,
            type="UnitaOrganizzativa",
            title="UO",
        )
        pdc = api.content.create(
            container=self.portal,
            type="PuntoDiContatto",
            title="PDC",
        )
        venue = api.content.create(
            container=self.portal,
            type="Venue",
            title="Venue",
        )
        commit()
        intids = getUtility(IIntIds)
        uo2.sede = [RelationValue(intids.getId(venue))]
        uo2.contact_info = [RelationValue(intids.getId(pdc))]
        commit()
        response = self.api_session.get(uo.absolute_url())
        res = response.json()
        contact_info = res["uo_children"][0]["contact_info"]
        sede = res["uo_children"][0]["sede"]
        self.assertEqual(contact_info[0]["@type"], "PuntoDiContatto")
        self.assertEqual(sede[0]["@type"], "Venue")

    def test_image_in_uo_serializer(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
        )
        uo2 = api.content.create(
            container=uo,
            type="UnitaOrganizzativa",
            title="UO",
        )
        commit()
        response = self.api_session.get(uo.absolute_url())
        res = response.json()
        uo_children = res["uo_children"][0]
        self.assertEqual(uo_children["image_field"], None)
        self.assertEqual(uo_children["image_scales"], None)

        # now, add a preview image
        filename = os.path.join(os.path.dirname(__file__), "example.png")
        uo2.preview_image = NamedBlobImage(
            data=open(filename, "rb").read(),
            filename="example.png",
            contentType="image/png",
        )
        commit()
        response = self.api_session.get(uo.absolute_url())
        res = response.json()
        uo_children = res["uo_children"][0]
        self.assertEqual(uo_children["image_field"], "preview_image")
        self.assertEqual("preview_image" in res["uo_children"][0]["image_scales"], True)

        # let's try with both image
        uo2.image = NamedBlobImage(
            data=open(filename, "rb").read(),
            filename="example.png",
            contentType="image/png",
        )
        commit()
        response = self.api_session.get(uo.absolute_url())
        res = response.json()
        image_scales = list(res["uo_children"][0]["image_scales"].keys())
        self.assertIn("preview_image", image_scales)
        self.assertIn("image", image_scales)
