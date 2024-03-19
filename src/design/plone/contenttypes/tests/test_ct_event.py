# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.contenttypes.schema_overrides import SchemaTweaks
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.autoform.interfaces import IFormFieldProvider
from plone.restapi.testing import RelativeSession
from zope.component import provideAdapter

import transaction
import unittest


class TestEventSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_event(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Event"].behaviors,
            (
                "plone.eventbasic",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.argomenti_evento",
                "plone.eventrecurrence",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.evento",
                "design.plone.contenttypes.behavior.luoghi_correlati_evento",
                "design.plone.contenttypes.behavior.address_event",
                "design.plone.contenttypes.behavior.geolocation_event",
                "design.plone.contenttypes.behavior.strutture_correlate",
                "design.plone.contenttypes.behavior.contatti_event",
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.relateditems",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "collective.taxonomy.generated.tipologia_evento",
            ),
        )

    def test_event_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            sorted(("Image", "File", "Link", "Event", "Document")),
            sorted(portal_types["Event"].allowed_content_types),
        )

    def test_event_provide_design_pct_marker_interface(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        event = api.content.create(container=self.portal, type="Event", title="Evento")
        self.assertTrue(IDesignPloneContentType.providedBy(event))

    def test_event_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(len(resp["fieldsets"]), 12)
        # should be 13 but SchemaTweaks does not work in tests
        # self.assertEqual(len(resp["fieldsets"]), 13)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cose",
                "luogo",
                "date_e_orari",
                "costi",
                "contatti",
                "informazioni",
                # "correlati", see SchemaTweaks problem in tests
                "categorization",
                "dates",
                "settings",
                "ownership",
                "seo",
            ],
        )

    def test_event_required_fields(self):
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "tassonomia_argomenti",
                    "tipologia_evento",
                    "start",
                    "prezzo",
                    "end",
                    "descrizione_estesa",
                    "descrizione_destinatari",
                    "contact_info",
                    "description",
                ]
            ),
        )

    def test_event_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "start",
                "end",
                "whole_day",
                "open_end",
                "sync_uid",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "correlato_in_evidenza",
                "tassonomia_argomenti",
                "recurrence",
                "sottotitolo",
                "tipologia_evento",
            ],
            # should be like this with SchemaTweaks
            # [
            #     "title",
            #     "description",
            #     "image",
            #     "image_caption",
            #     "preview_image",
            #     "preview_caption",
            #     "correlato_in_evidenza",
            #     "tassonomia_argomenti",
            #     "sottotitolo",
            #     "tipologia_evento",
            # ],
        )

    def test_event_fields_cose_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "descrizione_estesa",
                "descrizione_destinatari",
                "persone_amministrazione",
            ],
        )

    def test_event_fields_luogo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            [
                "luoghi_correlati",
                "nome_sede",
                "street",
                "zip_code",
                "city",
                "quartiere",
                "circoscrizione",
                "country",
                "geolocation",
            ],
        )

    def test_event_fields_date_e_orari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "orari",
            ],
            # with SchemaTweaks should be like this
            # [
            #     "start",
            #     "end",
            #     "whole_day",
            #     "open_end",
            #     "sync_uid",
            #     "recurrence",
            #     "orari",
            # ],
        )

    def test_event_fields_costi_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            [
                "prezzo",
            ],
            # should be like this with SchemaTweaks
            # [
            #     "costi",
            # ],
        )

    def test_event_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "organizzato_da_interno",
                "organizzato_da_esterno",
                "supportato_da",
                "patrocinato_da",
                "contact_info",
            ],
        )

    def test_event_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["ulteriori_informazioni", "strutture_politiche"],
        )

    # def test_event_fields_correlati_fieldset(self):
    #     """
    #     Get the list from restapi
    #     """
    #     resp = self.api_session.get("@types/Event").json()
    #     self.assertEqual(
    #         resp["fieldsets"][7]["fields"],
    #         ["relatedItems"],
    #     )

    def test_event_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
            ["subjects", "language", "relatedItems"],
            # should be like this with SchemaTweaks
            # ["subjects", "language"],
        )

    def test_event_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][8]["fields"], ["effective", "expires"])

    def test_event_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_event_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][10]["fields"], ["creators", "contributors", "rights"]
        )

    def test_event_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
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


class TestEventApi(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        self.event = api.content.create(
            container=self.portal, type="Event", title="Evento"
        )
        provideAdapter(SchemaTweaks, (IFormFieldProvider,), name="schema.tweaks")
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_event_substructure_created(self):
        event = self.portal["evento"]

        self.assertEqual(
            sorted(["documenti", "immagini", "sponsor_evento", "video"]),
            sorted(event.keys()),
        )

        self.assertEqual(event["immagini"].portal_type, "Document")
        self.assertEqual(event["immagini"].constrain_types_mode, 1)
        self.assertEqual(event["immagini"].locally_allowed_types, ("Image", "Link"))

        self.assertEqual(event["sponsor_evento"].portal_type, "Document")
        self.assertEqual(event["sponsor_evento"].constrain_types_mode, 1)
        self.assertEqual(event["sponsor_evento"].locally_allowed_types, ("Link",))

        self.assertEqual(event["documenti"].portal_type, "Document")
        self.assertEqual(event["documenti"].constrain_types_mode, 1)
        self.assertEqual(event["documenti"].locally_allowed_types, ("File",))

        self.assertEqual(event["video"].portal_type, "Document")
        self.assertEqual(event["video"].constrain_types_mode, 1)
        self.assertEqual(event["video"].locally_allowed_types, ("Link",))

        self.assertEqual(api.content.get_state(obj=event["immagini"]), "published")
        self.assertEqual(api.content.get_state(obj=event["video"]), "published")
        self.assertEqual(
            api.content.get_state(obj=event["sponsor_evento"]), "published"
        )
        self.assertEqual(api.content.get_state(obj=event["documenti"]), "published")
