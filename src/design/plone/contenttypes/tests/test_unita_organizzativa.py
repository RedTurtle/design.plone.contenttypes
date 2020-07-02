# -*- coding: utf-8 -*-

"""Setup tests for this package."""
from plone import api
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone.restapi.testing import RelativeSession
from transaction import commit
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from Products.CMFPlone.utils import getToolByName
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
import unittest


class TestServizio(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

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
        self.service = api.content.create(
            container=self.portal, type="Servizio", title="TestService"
        )
        self.uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="TestUO"
        )
        intids = getUtility(IIntIds)
        uo = RelationValue(intids.getId(self.uo))
        self.news.a_cura_di = [uo]
        self.service.ufficio_responsabile = [uo]
        pcatalog = getToolByName(self.portal, "portal_catalog")
        pcatalog.manage_reindexIndex(ids=["ufficio_responsabile", "news_uo"])
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_uo_service_related_news(self):
        response = self.api_session.get(
            self.uo.absolute_url() + "?fullobjects",
        )
        self.assertTrue(
            response.json()["related_news"][0]["@id"], self.news.absolute_url()
        )

    def test_uo_service_related_service(self):
        response = self.api_session.get(
            self.uo.absolute_url() + "?fullobjects",
        )
        self.assertTrue(
            response.json()["servizi_offerti"][0]["@id"],
            self.service.absolute_url(),
        )


class TestUO(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_uo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["UnitaOrganizzativa"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "plone.locking",
                "collective.geolocationbehavior.geolocation.IGeolocatable",
                "plone.leadimage",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.additional_help_infos",
            ),
        )

    def test_uo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            "Unita Organizzativa", portal_types["UnitaOrganizzativa"].title
        )
