# -*- coding: utf-8 -*-

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
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestPersona(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

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


class TestPersonaEndpoint(unittest.TestCase):
    """"""

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
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

    def test_persona_strutture_correlate(self):
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 1",
            persone_struttura=[self.persona_ref],
        )
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()

        self.assertIn("strutture_correlate", list(res.keys()))
        self.assertEqual(len(res["strutture_correlate"]), 1)
        self.assertEqual(res["strutture_correlate"][0]["title"], uo.title)

    def test_persona_responsabile_di(self):
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 1",
            responsabile=[self.persona_ref],
        )
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()

        self.assertIn("responsabile_di", list(res.keys()))
        self.assertEqual(len(res["responsabile_di"]), 1)
        self.assertEqual(res["responsabile_di"][0]["title"], uo.title)

    def test_persona_assessore_di(self):
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 1",
            assessore_riferimento=[self.persona_ref],
        )
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()

        self.assertIn("assessore_di", list(res.keys()))
        self.assertEqual(len(res["assessore_di"]), 1)
        self.assertEqual(res["assessore_di"][0]["title"], uo.title)

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
