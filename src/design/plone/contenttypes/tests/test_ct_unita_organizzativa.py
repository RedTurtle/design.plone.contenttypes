# -*- coding: utf-8 -*-

"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone.restapi.testing import RelativeSession
from Products.CMFPlone.utils import getToolByName
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestUO(unittest.TestCase):
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

        self.intids = getUtility(IIntIds)
        self.news = api.content.create(
            container=self.portal, type="News Item", title="TestNews"
        )
        self.luogo = api.content.create(
            container=self.portal, type="Venue", title="Luogo",
        )
        sede = RelationValue(self.intids.getId(self.luogo))

        self.uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="TestUO",
            sede=[sede],
        )

        self.service = api.content.create(
            container=self.portal,
            type="Servizio",
            title="TestService",
            ufficio_responsabile=[RelationValue(self.intids.getId(self.uo))],
        )

        self.bando = api.content.create(
            container=self.portal,
            type="Bando",
            title="TestBando",
            ufficio_responsabile=[RelationValue(self.intids.getId(self.uo))],
        )

        self.news.a_cura_di = [RelationValue(self.intids.getId(self.uo))]
        pcatalog = getToolByName(self.portal, "portal_catalog")
        pcatalog.manage_reindexIndex(ids=["ufficio_responsabile", "news_uo"])
        commit()

    def tearDown(self):
        self.api_session.close()

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
                "plone.leadimage",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.address_uo",
                "design.plone.contenttypes.behavior.geolocation_uo",
                "design.plone.contenttypes.behavior.contatti_uo",
                "design.plone.contenttypes.behavior.argomenti",
                "collective.dexteritytextindexer",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.translatable",
                "kitconcept.seo",
            ),
        )

    def test_uo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            "Unita Organizzativa", portal_types["UnitaOrganizzativa"].title
        )

    def test_uo_service_related_news(self):
        response = self.api_session.get(self.uo.absolute_url() + "?fullobjects")
        self.assertTrue(
            response.json()["related_news"][0]["@id"], self.news.absolute_url()
        )

    def test_uo_service_related_service_show_only_services(self):
        response = self.api_session.get(self.uo.absolute_url() + "?fullobjects")
        self.assertEqual(
            len(response.json()["servizi_offerti"]), 1,
        )
        self.assertTrue(
            response.json()["servizi_offerti"][0]["@id"], self.service.absolute_url(),
        )

    def test_uo_sede_data(self):
        response = self.api_session.get(self.uo.absolute_url() + "?fullobjects")
        sede = response.json()["sede"][0]
        fields = [
            "street",
            "zip_code",
            "city",
            "country",
            "orario_pubblico",
            "telefono",
            "email",
            "pec",
            "web",
            "riferimento_telefonico_struttura",
            "riferimento_mail_struttura",
            "riferimento_pec_struttura",
        ]
        for field in fields:
            self.assertEqual(sede[field], getattr(self.luogo, field, ""))

    def test_uo_location_indexer_populated(self):
        pc = api.portal.get_tool(name="portal_catalog")
        self.assertEqual((self.luogo.UID(),), pc.uniqueValuesFor("uo_location"))

        # create another uo and a venue
        luogo_bis = api.content.create(
            container=self.portal, type="Venue", title="Luogo bis",
        )
        api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="Second UO",
            sede=[RelationValue(self.intids.getId(self.luogo))],
            sedi_secondarie=[RelationValue(self.intids.getId(luogo_bis))],
        )

        self.assertEqual(
            tuple(sorted([self.luogo.UID(), luogo_bis.UID()])),
            pc.uniqueValuesFor("uo_location"),
        )

    def test_uo_locations_vocabulary_populated(self):
        # create another uo and a venue
        luogo_bis = api.content.create(
            container=self.portal, type="Venue", title="Luogo bis",
        )
        api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="Second UO",
            sede=[RelationValue(self.intids.getId(self.luogo))],
            sedi_secondarie=[RelationValue(self.intids.getId(luogo_bis))],
        )

        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.uo_locations"
        )
        vocabulary = factory(self.portal)

        self.assertIn(self.luogo.UID(), vocabulary)
        self.assertIn(luogo_bis.UID(), vocabulary)
        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(vocabulary.getTerm(self.luogo.UID()).title, self.luogo.Title())
        self.assertEqual(vocabulary.getTerm(luogo_bis.UID()).title, luogo_bis.Title())
