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
from Products.CMFPlone.utils import getToolByName
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IVocabularyFactory

import transaction
import unittest


class TestUOSchema(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

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
                "volto.preview_image",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.contatti_uo",
                "design.plone.contenttypes.behavior.argomenti",
                "plone.textindexer",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "collective.taxonomy.generated.tipologia_organizzazione",
            ),
        )

    def test_uo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            "Unita Organizzativa", portal_types["UnitaOrganizzativa"].title
        )

    def test_uo_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(len(resp["fieldsets"]), 12)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cosa_fa",
                "struttura",
                "persone",
                "contatti",
                "correlati",
                "categorization",
                "informazioni",
                "settings",
                "ownership",
                "dates",
                "seo",
            ],
        )

    def test_uo_required_fields(self):
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "competenze",
                    "tipologia_organizzazione",
                    "sede",
                    "contact_info",
                    "description",
                ]
            ),
        )

    def test_uo_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tassonomia_argomenti",
            ],
        )

    def test_uo_fields_cosa_fa_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(resp["fieldsets"][1]["fields"], ["competenze"])

    def test_uo_fields_struttura_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            [
                "legami_con_altre_strutture",
                "responsabile",
                "assessore_riferimento",
                "tipologia_organizzazione",
            ],
        )

    def test_uo_fields_persone_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            ["persone_struttura"],
        )

    def test_uo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["contact_info", "sede", "sedi_secondarie", "orario_pubblico"],
        )

    def test_uo_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            # ["documenti_pubblici", "correlato_in_evidenza"], # BBB dovrebbe essere così
            # ma viene fuori così nei test perché non viene vista la patch SchemaTweaks
            ["correlato_in_evidenza"],
        )

    def test_uo_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            # ["subjects", "language"] BBB dovrebbe essere così
            # ma nei test esce così perché non viene vista la patch di SchemaTweaks
            ["subjects", "language", "relatedItems", "documenti_pubblici"],
        )

    def test_uo_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["ulteriori_informazioni"])

    def test_uo_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_uo_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"], ["creators", "contributors", "rights"]
        )

    def test_uo_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(resp["fieldsets"][10]["fields"], ["effective", "expires"])

    def test_uo_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][11]["fields"],
            [
                "seo_title",
                "seo_description",
                "seo_noindex",
                "seo_canonical_url",
                "opengraph_title",
                "opengraph_description",
                "opengraph_image",
            ],
        )


class TestUO(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING
    maxDiff = None

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
            container=self.portal,
            type="Venue",
            title="Luogo",
        )
        sede = RelationValue(self.intids.getId(self.luogo))

        self.uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="TestUO",
            sede=[sede],
            city="Metropolis",
            zip_code="1234",
            street="whatever",
            contact_info={"blocks": {"xxx": {"foo": "bar"}}},
        )

        self.uo_child = api.content.create(
            container=self.uo,
            type="UnitaOrganizzativa",
            title="Child uo",
            city="Gotham City",
            zip_code="5678",
            street="somewhere",
            contact_info={"blocks": {"yyy": {"foo": "bar"}}},
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

    def test_uo_service_related_service_show_only_services(self):
        response = self.api_session.get(self.uo.absolute_url() + "?fullobjects")
        self.assertEqual(
            len(response.json()["servizi_offerti"]),
            1,
        )
        self.assertTrue(
            response.json()["servizi_offerti"][0]["@id"],
            self.service.absolute_url(),
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
            self.assertEqual(sede[field], getattr(self.luogo, field, None))

    def test_uo_location_indexer_populated(self):
        pc = api.portal.get_tool(name="portal_catalog")
        self.assertEqual((self.luogo.UID(),), pc.uniqueValuesFor("uo_location"))

        # create another uo and a venue
        luogo_bis = api.content.create(
            container=self.portal,
            type="Venue",
            title="Luogo bis",
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
            container=self.portal,
            type="Venue",
            title="Luogo bis",
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

    def test_do_not_show_parent_uo_if_not_present(self):
        response = self.api_session.get(self.uo.absolute_url())
        self.assertEqual(response.status_code, 200)
        uo_parent = response.json()["uo_parent"]

        self.assertIsNone(uo_parent)

    def test_show_parent_uo_if_present(self):
        response = self.api_session.get(self.uo_child.absolute_url())
        self.assertEqual(response.status_code, 200)
        uo_parent = response.json()["uo_parent"]

        self.assertIsNotNone(uo_parent)
        self.assertEqual(uo_parent["id"], self.uo.getId())
        self.assertEqual(uo_parent["zip_code"], self.uo.zip_code)
        self.assertEqual(uo_parent["city"], self.uo.city)
        self.assertEqual(uo_parent["contact_info"], self.uo.contact_info)
        self.assertEqual(uo_parent["street"], self.uo.street)

    def test_do_not_show_children_uo_if_not_present(self):
        response = self.api_session.get(self.uo_child.absolute_url())
        self.assertEqual(response.status_code, 200)
        uo_children = response.json()["uo_children"]

        self.assertEqual(uo_children, [])

    def test_show_children_uo_if_present(self):
        response = self.api_session.get(self.uo.absolute_url())
        self.assertEqual(response.status_code, 200)
        uo_children = response.json()["uo_children"]

        self.assertEqual(len(uo_children), 1)
        self.assertEqual(uo_children[0]["id"], self.uo_child.getId())
        self.assertEqual(uo_children[0]["zip_code"], self.uo_child.zip_code)
        self.assertEqual(uo_children[0]["city"], self.uo_child.city)
        self.assertEqual(uo_children[0]["contact_info"], self.uo_child.contact_info)
        self.assertEqual(uo_children[0]["street"], self.uo_child.street)

    def test_backref_to_servizio_dove_rivolgersi(self):
        """Check backref to servizio in
        dove rivolgersi field"""

        self.service.dove_rivolgersi = [RelationValue(self.intids.getId(self.uo))]

        self.service.reindexObject()
        transaction.commit()

        response = self.api_session.get(self.uo.absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.service.absolute_url(),
            [i["@id"] for i in response.json()["prestazioni"]],
        )

    def test_cant_patch_uo_that_has_no_required_fields(self):
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="Foo"
        )
        commit()
        resp = self.api_session.patch(
            uo.absolute_url(),
            json={
                "title": "Foo modified",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("La descrizione è obbligatoria", resp.json()["message"])

    def test_can_sort_uo_that_has_no_required_fields(self):
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="Foo"
        )
        commit()
        self.assertEqual(self.bando, self.portal.listFolderContents()[-2])
        self.assertEqual(uo, self.portal.listFolderContents()[-1])

        resp = self.api_session.patch(
            self.portal_url,
            json={"ordering": {"delta": -1, "obj_id": uo.getId()}},
        )
        commit()

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.bando, self.portal.listFolderContents()[-1])
        self.assertEqual(uo, self.portal.listFolderContents()[-2])
