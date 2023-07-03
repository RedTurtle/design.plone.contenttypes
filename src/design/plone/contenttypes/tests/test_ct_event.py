# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.contenttypes.schema_overrides import SchemaTweaks
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
from plone.autoform.interfaces import IFormFieldProvider
from plone.restapi.testing import RelativeSession
from zope.component import provideAdapter

import transaction
import unittest


class TestEvent(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING
    maxDiff = None

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

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
