# -*- coding: utf-8 -*-
from DateTime import DateTime
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from Products.CMFPlone.utils import getToolByName
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestLuogo(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_luogo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Venue"].behaviors,
            (
                "plone.app.content.interfaces.INameFromTitle",
                "plone.app.dexterity.behaviors.id.IShortName",
                "plone.app.dexterity.behaviors.metadata.IBasic",
                "plone.app.dexterity.behaviors.metadata.ICategorization",
                "plone.relateditems",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.contatti_venue",
                "design.plone.contenttypes.behavior.luogo",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.address_venue",
                "design.plone.contenttypes.behavior.geolocation_venue",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
            ),
        )

    def test_luogo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Luogo", portal_types["Venue"].title)


class TestLuogoApi(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.news = api.content.create(
            container=self.portal, type="News Item", title="TestNews"
        )
        self.news_published = api.content.create(
            container=self.portal, type="News Item", title="TestNews published"
        )
        self.service = api.content.create(
            container=self.portal, type="Servizio", title="TestService"
        )
        self.uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="TestUO"
        )

        self.venue = api.content.create(
            container=self.portal, type="Venue", title="TestVenue"
        )

        api.content.transition(obj=self.news_published, transition="publish")
        self.news_published.setEffectiveDate(DateTime())
        self.news_published.reindexObject()

        intids = getUtility(IIntIds)

        venue = RelationValue(intids.getId(self.venue))
        self.news.luoghi_correlati = [venue]
        self.news_published.luoghi_correlati = [venue]
        self.service.dove_rivolgersi = [venue]
        self.uo.luoghi_correlati = [venue]
        pcatalog = getToolByName(self.portal, "portal_catalog")
        pcatalog.manage_reindexIndex(ids=["service_venue", "uo_location", "news_venue"])
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_venus_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Folder", "Link", "Image", "File"),
            portal_types["Venue"].allowed_content_types,
        )

    def test_venue_geolocation_deserializer_wrong_structure(self):
        venue = api.content.create(
            container=self.portal, type="Venue", title="Example venue"
        )

        commit()
        self.assertEqual(venue.geolocation, None)

        response = self.api_session.patch(
            venue.absolute_url(),
            json={"@type": "Venue", "title": "Foo", "geolocation": {"foo": "bar"}},
        )
        message = response.json()["message"]

        self.assertEqual(400, response.status_code)
        self.assertIn("Invalid geolocation data", message)
        self.assertEqual(venue.geolocation, None)

    def test_venue_geolocation_deserializer_right_structure(self):
        venue = api.content.create(
            container=self.portal, type="Venue", title="Example venue"
        )

        commit()
        self.assertEqual(venue.geolocation, None)

        response = self.api_session.patch(
            venue.absolute_url(),
            json={
                "@type": "Venue",
                "title": "Foo",
                "geolocation": {"latitude": 11.0, "longitude": 10.0},
            },
        )
        commit()

        self.assertEqual(204, response.status_code)
        self.assertEqual(venue.geolocation.latitude, 11.0)
        self.assertEqual(venue.geolocation.longitude, 10.0)

    def test_venue_services(self):
        response = self.api_session.get(self.venue.absolute_url() + "?fullobjects")
        self.assertTrue(
            response.json()["venue_services"][0]["@id"],
            self.service.absolute_url(),
        )

    def test_venue_news(self):
        response = self.api_session.get(self.venue.absolute_url() + "?fullobjects")
        res = response.json()

        self.assertEqual(len(res["related_news"]), 2)
        self.assertEqual(
            res["related_news"][0]["@id"], self.news_published.absolute_url()
        )
        self.assertEqual(
            res["related_news"][1]["@id"],
            self.news.absolute_url(),
        )
