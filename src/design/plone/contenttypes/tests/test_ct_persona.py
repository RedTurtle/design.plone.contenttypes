# -*- coding: utf-8 -*-

from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import helpers
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestPersonaSchema(unittest.TestCase):
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
        self.persona = api.content.create(
            container=self.portal, type="Persona", title="John Doe"
        )
        intids = getUtility(IIntIds)

        self.persona_ref = RelationValue(intids.getId(self.persona))
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_behaviors_enabled_for_persona(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Persona"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.relateditems",
                "plone.categorization",
                "plone.basic",
                "plone.locking",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.contatti_persona",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
            ),
        )

    def test_persona_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Persona pubblica", portal_types["Persona"].title)

    def test_persona_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(len(resp["fieldsets"]), 10)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "ruolo",
                "contatti",
                "documenti",
                "informazioni",
                # "correlati", questo non viene fuori nei test
                "categorization",
                "dates",
                "ownership",
                "settings",
                "seo",
            ],
        )

    def test_persona_required_fields(self):
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "contact_info",
                ]
            ),
        )

    def test_persona_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            ["title", "description", "foto_persona"],
        )

    def test_persona_fields_ruolo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            ["incarichi_persona", "competenze", "deleghe", "biografia"],
        )

    def test_persona_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][2]["fields"], ["contact_info"])

    def test_persona_fields_documenti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][3]["fields"], ["curriculum_vitae"])

    def test_persona_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["ulteriori_informazioni"],
        )

    def test_persona_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"], ["relatedItems", "subjects", "language"]
        )

    def test_persona_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["effective", "expires"])

    def test_persona_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"], ["creators", "contributors", "rights"]
        )

    def test_persona_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
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

    def test_persona_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
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

    def test_atto_di_nomina_incarico(self):
        incarico = api.content.create(
            container=self.persona.incarichi, type="Incarico", title="Sindaco"
        )
        commit()
        atto_nomina = api.content.create(
            container=incarico, type="Documento", title="Atto di nomina"
        )
        commit()
        intids = getUtility(IIntIds)
        self.persona.incarichi_persona = [RelationValue(intids.getId(incarico))]
        incarico.atto_nomina = [RelationValue(intids.getId(atto_nomina))]
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()
        self.assertEqual(len(res["incarichi_persona"]), 1)
        self.assertEqual(res["incarichi_persona"][0]["title"], incarico.title)
        self.assertIn("atto_di_nomina", list(res["incarichi_persona"][0].keys()))

    def test_delete_incarico_and_call_persona(self):
        """
        This test is to check that if an incarico is deleted,
        the persona endpoint respond correctly. Right now it breaks because of
        the relation to the deleted incarico in persona ct.
        """
        incarico = api.content.create(
            container=self.persona.incarichi, type="Incarico", title="Sindaco"
        )
        commit()
        intids = getUtility(IIntIds)
        self.persona.incarichi_persona = [RelationValue(intids.getId(incarico))]
        commit()

        summary = getMultiAdapter(
            (self.persona, self.request), ISerializeToJsonSummary
        )()
        self.assertTrue(len(summary["incarichi"]) > 0)

        self.persona.incarichi._delObject(incarico.getId())
        commit()
        summary = getMultiAdapter(
            (self.persona, self.request), ISerializeToJsonSummary
        )()
        # non ho incarichi, ma soprattutto non ho errori
        self.assertTrue(len(summary["incarichi"]) == 0)

    def test_unauthorized_on_subfolder(self):
        incarico = api.content.create(
            container=self.persona.incarichi, type="Incarico", title="Sindaco"
        )
        commit()
        intids = getUtility(IIntIds)
        self.persona.incarichi_persona = [RelationValue(intids.getId(incarico))]
        api.content.transition(obj=self.persona, transition="publish")
        commit()

        helpers.logout()
        # with previous bug this as anonymous user return
        # AccessControl.unauthorized.Unauthorized: You are not allowed to
        # access '_Access_inactive_portal_content_Permission' in this context
        persona_summary = getMultiAdapter(
            (self.persona, self.request), ISerializeToJsonSummary
        )()
        self.assertFalse(persona_summary["incarichi"])
        incarico_summary = getMultiAdapter(
            (self.persona.incarichi.sindaco, self.request), ISerializeToJsonSummary
        )()
        self.assertEqual(incarico_summary["compensi_file"], [])
        self.assertEqual(incarico_summary["importi_di_viaggio_e_o_servizi"], [])
