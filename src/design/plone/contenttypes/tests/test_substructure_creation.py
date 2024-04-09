# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestEventCreation(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_bando_substructure_created(self):
        """
        Should have:
        - documenti
        - comunicazioni
        - esiti
        """
        item = api.content.create(
            container=self.portal,
            type="Bando",
            title="Test Bando",
        )

        self.assertEqual(
            list(item.keys()),
            ["documenti", "comunicazioni", "esiti"],
        )

        self.assertEqual(item["documenti"].portal_type, "Bando Folder Deepening")
        self.assertEqual(api.content.get_state(item["documenti"]), "private")

        self.assertEqual(item["comunicazioni"].portal_type, "Bando Folder Deepening")
        self.assertEqual(api.content.get_state(item["comunicazioni"]), "private")

        self.assertEqual(item["esiti"].portal_type, "Bando Folder Deepening")
        self.assertEqual(api.content.get_state(item["esiti"]), "private")

    def test_documento_substructure_created(self):
        """
        Should have:
        - multimedia
        """
        item = api.content.create(
            container=self.portal,
            type="Documento",
            title="Test",
        )

        self.assertEqual(
            list(item.keys()),
            ["multimedia"],
        )

        self.assertEqual(item["multimedia"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["multimedia"]), "private")
        self.assertEqual(item["multimedia"].constrain_types_mode, 1)
        self.assertEqual(
            item["multimedia"].locally_allowed_types,
            ("Image",),
        )
        self.assertTrue(item["multimedia"].exclude_from_search)

    def test_event_substructure_created(self):
        """
        Should have:
        - multimedia
        - sponsor_evento
        - documenti
        """
        item = api.content.create(
            container=self.portal,
            type="Event",
            title="Test",
        )

        self.assertEqual(
            list(item.keys()),
            ["multimedia", "sponsor_evento", "documenti"],
        )

        self.assertEqual(item["multimedia"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["multimedia"]), "published")
        self.assertEqual(item["multimedia"].constrain_types_mode, 1)
        self.assertEqual(
            set(item["multimedia"].locally_allowed_types),
            set(["Image", "Link"]),
        )
        self.assertTrue(item["multimedia"].exclude_from_search)

        self.assertEqual(item["sponsor_evento"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["sponsor_evento"]), "published")
        self.assertEqual(item["sponsor_evento"].constrain_types_mode, 1)
        self.assertEqual(
            item["sponsor_evento"].locally_allowed_types,
            ("Link",),
        )
        self.assertTrue(item["sponsor_evento"].exclude_from_search)

        self.assertEqual(item["documenti"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["documenti"]), "published")
        self.assertEqual(item["documenti"].constrain_types_mode, 1)
        self.assertEqual(item["documenti"].locally_allowed_types, ("File",))
        self.assertTrue(item["documenti"].exclude_from_search)

    def test_news_substructure_created(self):
        """
        Should have:
        - multimedia
        - documenti allegati
        """
        item = api.content.create(
            container=self.portal,
            type="News Item",
            title="Test News",
        )

        self.assertEqual(
            list(item.keys()),
            ["multimedia", "documenti-allegati"],
        )

        self.assertEqual(item["multimedia"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["multimedia"]), "private")
        self.assertEqual(item["multimedia"].constrain_types_mode, 1)
        self.assertEqual(
            set(item["multimedia"].locally_allowed_types),
            set(["Image", "Link"]),
        )
        self.assertTrue(item["multimedia"].exclude_from_search)

        self.assertEqual(item["documenti-allegati"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["documenti-allegati"]), "private")
        self.assertEqual(item["documenti-allegati"].constrain_types_mode, 1)
        self.assertEqual(
            item["documenti-allegati"].locally_allowed_types,
            ("File", "Image"),
        )
        self.assertTrue(item["multimedia"].exclude_from_search)

    def test_venue_substructure_created(self):
        """
        Should have:
        - multimedia
        """
        item = api.content.create(
            container=self.portal,
            type="Venue",
            title="Test",
        )

        self.assertEqual(
            list(item.keys()),
            ["multimedia"],
        )

        self.assertEqual(item["multimedia"].portal_type, "Folder")
        # self.assertEqual(api.content.get_state(item["multimedia"]), "published")
        self.assertEqual(item["multimedia"].constrain_types_mode, 1)
        self.assertEqual(
            item["multimedia"].locally_allowed_types,
            ("Image", "Link"),
        )
        self.assertTrue(item["multimedia"].exclude_from_search)

    def test_persona_substructure_created(self):
        """
        Should have:
        - foto-e-attivita-politica
        - curriculum-vitae
        - situazione-patrimoniale
        - dichiarazione-dei-redditi
        - spese-elettorali
        - spese-elettorali
        - variazione-situazione-patrimoniale" "altre-cariche
        - incarichi
        """
        item = api.content.create(
            container=self.portal,
            type="Persona",
            title="Test",
        )

        self.assertEqual(
            list(item.keys()),
            [
                "foto-e-attivita-politica",
                "curriculum-vitae",
                "compensi",
                "importi-di-viaggio-e-o-servizi",
                "situazione-patrimoniale",
                "dichiarazione-dei-redditi",
                "spese-elettorali",
                "variazione-situazione-patrimoniale",
                "altre-cariche",
            ],
        )

        self.assertEqual(item["foto-e-attivita-politica"].portal_type, "Document")
        self.assertEqual(
            api.content.get_state(item["foto-e-attivita-politica"]), "private"
        )
        self.assertEqual(item["foto-e-attivita-politica"].constrain_types_mode, 1)
        self.assertEqual(
            item["foto-e-attivita-politica"].locally_allowed_types,
            ("Image",),
        )
        self.assertTrue(item["foto-e-attivita-politica"].exclude_from_search)

        self.assertEqual(item["curriculum-vitae"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["curriculum-vitae"]), "private")
        self.assertEqual(item["curriculum-vitae"].constrain_types_mode, 1)
        self.assertEqual(item["curriculum-vitae"].locally_allowed_types, ("File",))
        self.assertTrue(item["curriculum-vitae"].exclude_from_search)

        self.assertEqual(item["situazione-patrimoniale"].portal_type, "Document")
        self.assertEqual(
            api.content.get_state(item["situazione-patrimoniale"]), "private"
        )
        self.assertEqual(item["situazione-patrimoniale"].constrain_types_mode, 1)
        self.assertEqual(
            item["situazione-patrimoniale"].locally_allowed_types, ("File",)
        )
        self.assertTrue(item["situazione-patrimoniale"].exclude_from_search)

        self.assertEqual(item["dichiarazione-dei-redditi"].portal_type, "Document")
        self.assertEqual(
            api.content.get_state(item["dichiarazione-dei-redditi"]), "private"
        )
        self.assertEqual(item["dichiarazione-dei-redditi"].constrain_types_mode, 1)
        self.assertEqual(
            item["dichiarazione-dei-redditi"].locally_allowed_types, ("File",)
        )
        self.assertTrue(item["dichiarazione-dei-redditi"].exclude_from_search)

        self.assertEqual(item["spese-elettorali"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["spese-elettorali"]), "private")
        self.assertEqual(item["spese-elettorali"].constrain_types_mode, 1)
        self.assertEqual(item["spese-elettorali"].locally_allowed_types, ("File",))
        self.assertTrue(item["spese-elettorali"].exclude_from_search)

        self.assertEqual(item["curriculum-vitae"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["curriculum-vitae"]), "private")
        self.assertEqual(item["curriculum-vitae"].constrain_types_mode, 1)
        self.assertEqual(item["curriculum-vitae"].locally_allowed_types, ("File",))
        self.assertTrue(item["curriculum-vitae"].exclude_from_search)

        self.assertEqual(
            item["variazione-situazione-patrimoniale"].portal_type, "Document"
        )
        self.assertEqual(
            api.content.get_state(item["variazione-situazione-patrimoniale"]), "private"
        )
        self.assertEqual(
            item["variazione-situazione-patrimoniale"].constrain_types_mode, 1
        )
        self.assertEqual(
            item["variazione-situazione-patrimoniale"].locally_allowed_types, ("File",)
        )
        self.assertTrue(item["variazione-situazione-patrimoniale"].exclude_from_search)

        self.assertEqual(item["altre-cariche"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["altre-cariche"]), "private")
        self.assertEqual(item["altre-cariche"].constrain_types_mode, 1)
        self.assertEqual(item["altre-cariche"].locally_allowed_types, ("File",))
        self.assertTrue(item["altre-cariche"].exclude_from_search)

    def test_servizio_substructure_created(self):
        """
        Should have:
        - modulistica
        - allegati
        """
        item = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Test",
        )

        self.assertEqual(
            list(item.keys()),
            ["modulistica", "allegati"],
        )

        self.assertEqual(item["modulistica"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["modulistica"]), "private")
        self.assertEqual(item["modulistica"].constrain_types_mode, 1)
        self.assertEqual(item["modulistica"].locally_allowed_types, ("File", "Link"))
        self.assertTrue(item["modulistica"].exclude_from_search)

        self.assertEqual(item["allegati"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["allegati"]), "private")
        self.assertEqual(item["allegati"].constrain_types_mode, 1)
        self.assertEqual(item["allegati"].locally_allowed_types, ("File", "Link"))
        self.assertTrue(item["allegati"].exclude_from_search)

    def test_uo_substructure_created(self):
        """
        Should have:
        - allegati
        """
        item = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="Test",
        )

        self.assertEqual(
            list(item.keys()),
            ["allegati"],
        )

        self.assertEqual(item["allegati"].portal_type, "Document")
        self.assertEqual(api.content.get_state(item["allegati"]), "private")
        self.assertEqual(item["allegati"].constrain_types_mode, 1)
        self.assertEqual(item["allegati"].locally_allowed_types, ("File",))
        self.assertTrue(item["allegati"].exclude_from_search)
