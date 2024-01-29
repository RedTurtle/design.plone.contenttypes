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
from transaction import commit

import unittest


WIDGET_PROPERTY_CHECKS = {
    "tassonomia_argomenti": {
        "selectableTypes": ["Pagina Argomento"],
    },
    "ufficio_responsabile": {
        "selectableTypes": ["UnitaOrganizzativa"],
    },
    "area": {
        "maximumSelectionSize": 1,
        "selectableTypes": ["UnitaOrganizzativa"],
    },
    "altri_documenti": {
        "selectableTypes": ["Documento", "CartellaModulistica"],
    },
    "servizi_collegati": {
        "selectableTypes": ["Servizio"],
    },
    "dove_rivolgersi": {
        "selectableTypes": ["Venue", "UnitaOrganizzativa"],
    },
}


class TestServizioSchema(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING
    maxDiff = None

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

    def test_behaviors_enabled_for_servizio(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Servizio"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "design.plone.contenttypes.behavior.descrizione_estesa_servizio",
                "plone.locking",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.argomenti_servizio",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.contatti_servizio",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "collective.taxonomy.generated.person_life_events",
                "collective.taxonomy.generated.business_events",
            ),
        )

    def test_servizio_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(len(resp["fieldsets"]), 18)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cose",
                "a_chi_si_rivolge",
                "accedi_al_servizio",
                "cosa_serve",
                "costi_e_vincoli",
                "tempi_e_scadenze",
                "casi_particolari",
                "contatti",
                "documenti",
                "link_utili",
                "informazioni",
                "correlati",
                "categorization",
                "settings",
                "ownership",
                "dates",
                "seo",
            ],
        )

    def test_servizio_required_fields(self):
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "tassonomia_argomenti",
                    "a_chi_si_rivolge",
                    "come_si_fa",
                    "cosa_si_ottiene",
                    "cosa_serve",
                    "tempi_e_scadenze",
                    "ufficio_responsabile",
                    "contact_info",
                    "description",
                ]
            ),
        )

    def test_servizio_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "sottotitolo",
                "stato_servizio",
                "motivo_stato_servizio",
                "condizioni_di_servizio",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "correlato_in_evidenza",
                "tassonomia_argomenti",
                "person_life_events",
                "business_events",
            ],
        )

    def test_servizio_fields_cose_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            ["descrizione_estesa"],
        )

    def test_servizio_fields_a_chi_si_rivolge_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["a_chi_si_rivolge", "chi_puo_presentare", "copertura_geografica"],
        )

    def test_servizio_fields_accedi_al_servizio_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "come_si_fa",
                "cosa_si_ottiene",
                "procedure_collegate",
                "canale_digitale",
                "canale_digitale_link",
                "canale_fisico",
                "dove_rivolgersi",
                "dove_rivolgersi_extra",
                "prenota_appuntamento",
            ],
        )

    def test_servizio_fields_cosa_serve_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["cosa_serve"],
        )

    def test_servizio_fields_costi_e_vincoli_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["costi", "vincoli"])

    def test_servizio_fields_tempi_e_scadenze_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["tempi_e_scadenze", "timeline_tempi_scadenze"],
        )

    def test_servizio_fields_casi_particolari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["casi_particolari"])

    def test_servizio_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["ufficio_responsabile", "area", "contact_info"],
        )

    def test_servizio_fields_documenti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][9]["fields"], ["altri_documenti"])

    def test_servizio_fields_link_utili_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][10]["fields"], ["link_siti_esterni"])

    def test_servizio_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][11]["fields"],
            ["codice_ipa", "settore_merceologico", "ulteriori_informazioni"],
        )

    def test_servizio_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][12]["fields"],
            ["servizi_collegati"],
        )

    def test_servizio_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][13]["fields"],
            ["identificativo", "subjects", "language", "relatedItems"],
        )

    def test_servizio_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][14]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_servizio_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][15]["fields"], ["creators", "contributors", "rights"]
        )

    def test_servizio_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][16]["fields"], ["effective", "expires"])

    def test_servizio_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][17]["fields"],
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


class TestServizioApi(unittest.TestCase):
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

    def tearDown(self):
        self.api_session.close()

    def test_related_widgets(self):
        response = self.api_session.get("/@types/Servizio")
        res = response.json()
        properties = res["properties"]

        for field in WIDGET_PROPERTY_CHECKS:
            self.assertTrue(
                properties[field]["widgetOptions"]["pattern_options"]
                == WIDGET_PROPERTY_CHECKS[field]
            )
            self.assertTrue(properties[field]["type"] == "array")

    def test_canale_digitale_link_widget_set_in_schema(self):
        response = self.api_session.get("/@types/Servizio")
        res = response.json()
        self.assertEqual(res["properties"]["canale_digitale_link"]["widget"], "url")

    def test_sottotitolo_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            sottotitolo="sotto1",
        )

        res = api.content.find(SearchableText="sotto1")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_a_chi_si_rivolge_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            a_chi_si_rivolge={"blocks": {"foo": {"searchableText": "destinatari"}}},
        )

        res = api.content.find(SearchableText="destinatari")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_chi_puo_presentare_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            chi_puo_presentare={"blocks": {"foo": {"searchableText": "chi"}}},
        )

        res = api.content.find(SearchableText="chi")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_come_si_fa_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            come_si_fa={"blocks": {"foo": {"searchableText": "come"}}},
        )

        res = api.content.find(SearchableText="come")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_cosa_si_ottiene_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            cosa_si_ottiene={"blocks": {"foo": {"searchableText": "ottenere"}}},
        )

        res = api.content.find(SearchableText="ottenere")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_cosa_serve_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            cosa_serve={"blocks": {"foo": {"searchableText": "serve"}}},
        )

        res = api.content.find(SearchableText="serve")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_ulteriori_informazioni_indexed_in_searchabletext(self):
        #  Servizio is the only ct with this field
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            ulteriori_informazioni={"blocks": {"123456": {"searchableText": "aiuto"}}},
        )

        res = api.content.find(SearchableText="aiuto")

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, servizio.UID())

    def test_canale_digitale_link_serialized_as_url(self):
        page = api.content.create(
            container=self.portal, type="Document", title="Document"
        )
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            canale_digitale_link="/plone/resolveuid/{}".format(page.UID()),
        )

        commit()
        res = self.api_session.get(servizio.absolute_url()).json()
        self.assertEqual(res["canale_digitale_link"], page.absolute_url())

    def test_canale_digitale_link_deserialized_as_plone_internal_url(self):
        page = api.content.create(
            container=self.portal, type="Document", title="Document"
        )

        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test servizio",
            description="xxx",
            a_chi_si_rivolge={
                "blocks": {"xxx": {"@type": "foo", "searchableText": "aiuto"}},
                "blocks_layout": {"items": ["xxx"]},
            },
            canale_digitale={
                "blocks": {"xxx": {"@type": "foo", "searchableText": "aiuto"}},
                "blocks_layout": {"items": ["xxx"]},
            },
            come_si_fa={
                "blocks": {"xxx": {"@type": "foo", "searchableText": "aiuto"}},
                "blocks_layout": {"items": ["xxx"]},
            },
            cosa_serve={
                "blocks": {"xxx": {"@type": "foo", "searchableText": "aiuto"}},
                "blocks_layout": {"items": ["xxx"]},
            },
            cosa_si_ottiene={
                "blocks": {"xxx": {"@type": "foo", "searchableText": "aiuto"}},
                "blocks_layout": {"items": ["xxx"]},
            },
            tempi_e_scadenze={
                "blocks": {"xxx": {"@type": "foo", "searchableText": "aiuto"}},
                "blocks_layout": {"items": ["xxx"]},
            },
        )

        commit()

        self.api_session.patch(
            servizio.absolute_url(),
            json={"canale_digitale_link": page.absolute_url()},
        )

        commit()
        self.assertEqual(
            servizio.canale_digitale_link,
            "${{portal_url}}/resolveuid/{}".format(page.UID()),
        )

    def test_cant_patch_servizio_that_has_no_required_fields(self):
        service = api.content.create(
            container=self.portal, type="Servizio", title="Foo"
        )
        commit()
        resp = self.api_session.patch(
            service.absolute_url(),
            json={
                "title": "Foo modified",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("La descrizione è obbligatoria", resp.json()["message"])

    def test_can_sort_service_that_has_no_required_fields(self):
        document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )
        service = api.content.create(
            container=self.portal, type="Servizio", title="Foo"
        )
        commit()

        self.assertEqual(document, self.portal.listFolderContents()[0])
        self.assertEqual(service, self.portal.listFolderContents()[1])

        resp = self.api_session.patch(
            self.portal_url,
            json={"ordering": {"delta": -1, "obj_id": service.getId()}},
        )
        commit()

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(document, self.portal.listFolderContents()[1])
        self.assertEqual(service, self.portal.listFolderContents()[0])
