# -*- coding: utf-8 -*-

"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
    # DESIGN_PLONE_CONTENTTYPES_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
# from plone.app.textfield.value import RichTextValue
from plone.restapi.testing import RelativeSession
from Products.CMFPlone.utils import getToolByName
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

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

        intids = getUtility(IIntIds)
        self.news = api.content.create(
            container=self.portal, type="News Item", title="TestNews"
        )
        self.luogo = api.content.create(
            container=self.portal, type="Venue", title="Luogo",
            street="Street Foo",
            zip_code="1234",
            city="Rome",
            country="Italy",
            orario_pubblico="",
            telefono="123456",
            email="foo@foo.com",
            pec="foo@pec.com",
            riferimento_telefonico_struttura="9876",
            riferimento_mail_struttura="bar@bar.com",
            riferimento_pec_struttura="bar@pec.com",
            web="http://www.plone.org",
        )
        luogo = RelationValue(intids.getId(self.luogo))

        self.uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="TestUO",
            sede=[luogo]
        )
        uo = RelationValue(intids.getId(self.uo))

        self.service = api.content.create(
            container=self.portal,
            type="Servizio",
            title="TestService",
            ufficio_responsabile=[uo]
        )

        self.news.a_cura_di = [uo]
        pcatalog = getToolByName(self.portal, "portal_catalog")
        pcatalog.manage_reindexIndex(ids=["ufficio_responsabile", "news_uo"])
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_uo_service_related_news(self):
        response = self.api_session.get(self.uo.absolute_url() + "?fullobjects")
        self.assertTrue(
            response.json()["related_news"][0]["@id"], self.news.absolute_url()
        )

    def test_uo_service_related_service(self):
        response = self.api_session.get(self.uo.absolute_url() + "?fullobjects")
        self.assertTrue(
            response.json()["servizi_offerti"][0]["@id"],
            self.service.absolute_url()
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
            self.assertEqual(
                sede[field],
                getattr(self.luogo, field, '')
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
                "plone.leadimage",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.address_uo",
                "design.plone.contenttypes.behavior.geolocation_uo",
                "design.plone.contenttypes.behavior.contatti_uo",
                "design.plone.contenttypes.behavior.argomenti",
                "collective.dexteritytextindexer",
                "design.plone.contenttypes.behavior.additional_help_infos",
            ),
        )

    def test_uo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            "Unita Organizzativa", portal_types["UnitaOrganizzativa"].title
        )


#  DISABILITATO perchè nei test non indicizza niente nel searchabletext, non so perché
# class TestUOSearchableText(unittest.TestCase):
#     layer = DESIGN_PLONE_CONTENTTYPES_FUNCTIONAL_TESTING

#     def setUp(self):
#         """Custom shared utility setup for tests."""
#         self.portal = self.layer["portal"]
#         self.catalog = api.portal.get_tool(name="portal_catalog")
#         setRoles(self.portal, TEST_USER_ID, ["Manager"])

#         self.person = api.content.create(
#             container=self.portal, type="Persona", title="John Doe"
#         )

# def test_competenze_indexed(self):
#     uo = api.content.create(
#         container=self.portal,
#         type="UnitaOrganizzativa",
#         title="UO",
#         # competenze=RichTextValue(
#         #     raw="destinatari",
#         #     mimeType="text/html",
#         #     outputMimeType="text/html",
#         #     encoding="utf-8",
#         # ),
#     )
#     res = api.content.find(UID=uo.UID())
#     rid = res[0].getRID()
#     index_data = self.catalog.getIndexDataForRID(rid)

#     import pdb

#     pdb.set_trace()
#     res = api.content.find(SearchableText="destinatari")

#     self.assertEqual(len(res), 1)
#     self.assertEqual(res[0].UID, servizio.UID())
