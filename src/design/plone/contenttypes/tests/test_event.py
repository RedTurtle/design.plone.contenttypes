# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import transaction
import unittest


class TestEvent(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_event(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Event"].behaviors,
            (
                "plone.eventbasic",
                "plone.eventrecurrence",
                "plone.eventcontact",
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.relateditems",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "volto.blocks",
                "design.plone.contenttypes.behavior.evento",
                "design.plone.contenttypes.behavior.argomenti",
                "plone.leadimage",
            ),
        )

    def test_event_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Evento", portal_types["Event"].title)

    def test_event_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Image", "File", "Link",),
            portal_types["Event"].allowed_content_types,
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

        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_event_required_fields(self):
        response = self.api_session.post(
            self.portal_url, json={"@type": "Event", "title": "Bar"}
        )

        self.assertEqual(400, response.status_code)
        message = response.json()["message"]
        self.assertIn("date_significative", message)
        self.assertIn("descrizione_destinatari", message)
        self.assertIn("indirizzo", message)
        self.assertIn("cap", message)
        self.assertIn("orari", message)
        self.assertIn("prezzo", message)
        self.assertIn("cap", message)
        self.assertIn("box_aiuto", message)

        response = self.api_session.post(
            self.portal_url,
            json={
                "@type": "Event",
                "title": "Bar",
                "descrizione_destinatari": "pippo,pluto,paperino",
                "date_significative": "xxx",
                "indirizzo": "xxx",
                "cap": "11111",
                "orari": "lorem ipsum",
                "prezzo": "lorem ipsum",
                "box_aiuto": "lorem ipsum",
            },
        )

        self.assertEqual(201, response.status_code)

    def test_event_substructure_created(self):
        self.api_session.post(
            self.portal_url,
            json={
                "@type": "Event",
                "title": "Bar",
                "indirizzo": "xxx",
                "descrizione_destinatari": "pippo,pluto,paperino",
                "date_significative": "xxx",
                "cap": "11111",
                "orari": "lorem ipsum",
                "prezzo": "lorem ipsum",
                "box_aiuto": "lorem ipsum",
            },
        )

        transaction.commit()

        event = self.portal["bar"]

        self.assertEqual(["multimedia", "documenti"], event.keys())

        self.assertEqual(event["multimedia"].portal_type, "Folder")
        self.assertEqual(event["multimedia"].constrain_types_mode, 1)
        self.assertEqual(
            event["multimedia"].locally_allowed_types, ("Image", "Link")
        )

        self.assertEqual(event["documenti"].portal_type, "Folder")
        self.assertEqual(event["documenti"].constrain_types_mode, 1)
        self.assertEqual(
            event["documenti"].locally_allowed_types, ("File",),
        )
