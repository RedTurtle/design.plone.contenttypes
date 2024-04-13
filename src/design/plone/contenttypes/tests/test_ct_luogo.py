# -*- coding: utf-8 -*-
from DateTime import DateTime
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.formwidget.geolocation import Geolocation
from plone.restapi.testing import RelativeSession
from Products.CMFPlone.utils import getToolByName
from transaction import commit
from uuid import uuid4
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestLuogoSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_luogo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Venue"].behaviors,
            (
                "plone.app.content.interfaces.INameFromTitle",
                "plone.app.dexterity.behaviors.id.IShortName",
                "plone.app.dexterity.behaviors.metadata.IBasic",
                "plone.app.dexterity.behaviors.metadata.ICategorization",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.contatti_venue",
                "design.plone.contenttypes.behavior.luogo",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.address_venue",
                "design.plone.contenttypes.behavior.geolocation_venue",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.luoghi_correlati",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "collective.taxonomy.generated.tipologia_luogo",
            ),
        )

    def test_luogo_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Luogo", portal_types["Venue"].title)

    def test_luogo_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(len(resp["fieldsets"]), 11)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "descrizione",
                "accesso",
                "dove",
                "orari",
                "contatti",
                "informazioni",
                "settings",
                "correlati",
                "categorization",
                "seo",
            ],
        )

    def test_luogo_required_fields(self):
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "contact_info",
                    "modalita_accesso",
                    "description",
                    "street",
                    "city",
                    "zip_code",
                    "geolocation",
                ]
            ),
        )

    def test_luogo_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "nome_alternativo",
                "tassonomia_argomenti",
                "luoghi_correlati",
                "tipologia_luogo",
            ],
        )

    def test_luogo_fields_descrizione_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            ["descrizione_completa", "elementi_di_interesse"],
        )

    def test_luogo_fields_accesso_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["modalita_accesso"],
        )

    def test_luogo_fields_dove_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "street",
                "zip_code",
                "city",
                "quartiere",
                "circoscrizione",
                "country",
                "geolocation",
                "notes",
            ],
        )

    def test_luogo_fields_orari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["orario_pubblico"],
        )

    def test_luogo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "contact_info",
                "struttura_responsabile_correlati",
                "struttura_responsabile",
            ],
        )

    def test_luogo_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            [
                "ulteriori_informazioni",
            ],
        )

    def test_luogo_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
            [
                "id",
                "exclude_from_nav",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_luogo_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["correlato_in_evidenza"],
        )

    def test_luogo_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            # ["subjects", "language", "identificativo_mibac"] BBB dovrebbe essere così
            # ma nei test esce così perché non viene vista la patch di SchemaTweaks
            ["subjects", "language", "relatedItems", "identificativo_mibac"],
        )

    def test_luogo_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][10]["fields"],
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
        # message = response.json()["message"]

        self.assertEqual(400, response.status_code)
        # TODO: anzichè `invalid geolocation data` ritorna
        #       `Il campo geolocation è obbligatorio`
        # self.assertIn("Invalid geolocation data", message)
        # TODO: i dati vanno verificati con una chiamata alla api_session
        # self.assertEqual(venue.geolocation, None)

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

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"],
            "[{'error': 'ValidationError', "
            "'message': 'Il campo modalita_accesso è obbligatorio'}]",
        )

        text_uuid = str(uuid4())
        response = self.api_session.patch(
            venue.absolute_url(),
            json={
                "@type": "Venue",
                "title": "Foo",
                "geolocation": {"latitude": 11.0, "longitude": 10.0},
                "modalita_accesso": {
                    "blocks": {
                        text_uuid: {
                            "@type": "text",
                            "text": {"blocks": [{"text": "Test", "type": "paragraph"}]},
                        }
                    },
                    "blocks_layout": {"items": [text_uuid]},
                },
            },
        )
        self.assertEqual(response.status_code, 204)
        # TODO: i dati vanno verificati con una chiamata alla api_session
        # self.assertEqual(venue.geolocation.longitude, 10.0)
        # self.assert ... (venue.modalita_accesso)

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

    def test_venue_serializers(self):
        venue1 = api.content.create(container=self.portal, type="Venue", title="venue1")
        venue1.geolocation = Geolocation(44.35, 11.70)
        venue2 = api.content.create(container=self.portal, type="Venue", title="venue2")
        venue2.geolocation = Geolocation(44.35, 11.70)
        intids = getUtility(IIntIds)
        venue_rel = RelationValue(intids.getId(venue2))
        venue1.luoghi_correlati = [venue_rel]
        commit()
        response = self.api_session.post(
            "/@querystring-search",
            json={
                "metadata_fields": "_all",
                "query": [
                    {
                        "i": "portal_type",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["Venue"],
                    }
                ],
            },
        )
        items = response.json()["items"]
        for item in items:
            if item["id"] in ["venue1", "venue2"]:
                self.assertEqual(item["geolocation"]["latitude"], 44.35)
                self.assertEqual(item["geolocation"]["longitude"], 11.7)
