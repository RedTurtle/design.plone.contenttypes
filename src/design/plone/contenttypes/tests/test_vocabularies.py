# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from transaction import commit
from design.plone.contenttypes.controlpanels.settings import (
    IDesignPloneSettings,
)

import unittest
import json


class TestControlpanelVocabularies(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # default values are set in italian
        self.request["LANGUAGE"] = "it"

    def set_value_for_language(self, field, data):
        values = api.portal.get_registry_record(
            field, interface=IDesignPloneSettings, default=[]
        )
        json_value = json.loads(values)
        json_value.update(data)

        api.portal.set_registry_record(
            field, json.dumps(json_value), interface=IDesignPloneSettings
        )
        commit()

    def test_tipologia_notizia_vocab(self):
        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_notizia"
        )
        vocab = factory(self.portal)
        self.assertEqual(
            ["", "Avviso", "Comunicato stampa", "Novità"],
            [(x.value) for x in vocab],
        )

    def test_tipologia_notizia_vocab_in_another_language(self):
        self.request["LANGUAGE"] = "en"
        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_notizia"
        )
        vocab = factory(self.portal)
        self.assertEqual(
            [], [(x.value) for x in vocab],
        )

        #  set values also for en
        self.set_value_for_language(
            field="tipologie_notizia", data={"en": ["news-foo", "news-bar"]}
        )

        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_notizia"
        )
        vocab = factory(self.portal)
        self.assertEqual(
            ["", "news-foo", "news-bar"], [(x.value) for x in vocab],
        )

    def test_tipologie_unita_organizzativa_vocab(self):
        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.tipologie_unita_organizzativa",
        )
        vocab = factory(self.portal)
        self.assertEqual(
            ["", "Politica", "Amministrativa", "Altro"],
            [(x.value) for x in vocab],
        )

    def test_tipologia_unita_organizzativa_vocab_in_another_language(self):
        self.request["LANGUAGE"] = "en"
        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.tipologie_unita_organizzativa",
        )
        vocab = factory(self.portal)
        self.assertEqual(
            [], [(x.value) for x in vocab],
        )

        #  set values also for en
        self.set_value_for_language(
            field="tipologie_unita_organizzativa",
            data={"en": ["uo-foo", "uo-bar"]},
        )

        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.tipologie_unita_organizzativa",
        )
        vocab = factory(self.portal)
        self.assertEqual(
            ["", "uo-foo", "uo-bar"], [(x.value) for x in vocab],
        )

    def test_tipologie_tipologie_documento_vocab(self):
        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.tipologie_documento",
        )
        vocab = factory(self.portal)
        self.assertEqual(
            [
                "",
                "Accordi tra enti",
                "Atti normativi",
                "Dataset",
                "Documenti (tecnici) di supporto",
                "Documenti albo pretorio",
                "Documenti attività politica",
                "Documenti funzionamento interno",
                "Istanze",
                "Modulistica",
            ],
            [(x.value) for x in vocab],
        )

    def test_tipologie_documento_vocab_in_another_language(self):
        self.request["LANGUAGE"] = "en"
        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.tipologie_documento",
        )
        vocab = factory(self.portal)
        self.assertEqual(
            [], [(x.value) for x in vocab],
        )

        #  set values also for en
        self.set_value_for_language(
            field="tipologie_documento", data={"en": ["doc-foo", "doc-bar"]},
        )

        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_documento"
        )
        vocab = factory(self.portal)
        self.assertEqual(
            ["", "doc-foo", "doc-bar"], [(x.value) for x in vocab],
        )

    def test_dimensioni_immagini(self):
        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.leadimage_dimension",
        )
        vocab = factory(self.portal)
        terms = {x.token: x.title for x in vocab}
        self.assertTrue("News Item" in terms)
        self.assertTrue(terms["News Item"] == "1920x600")
        self.assertTrue("UnitaOrganizzativa" in terms)
        self.assertTrue(terms["UnitaOrganizzativa"] == "1920x600")
