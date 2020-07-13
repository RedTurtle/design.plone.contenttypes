# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.vocabularies import (
    IVocabulariesControlPanel,
)
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestControlpanelVocabularies(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.portal.set_registry_record(
            "tipologie_notizia",
            ["xxx", "yyy"],
            interface=IVocabulariesControlPanel,
        )
        api.portal.set_registry_record(
            "tipologie_unita_organizzativa",
            ["foo", "bar"],
            interface=IVocabulariesControlPanel,
        )

        api.portal.set_registry_record(
            "lead_image_dimension",
            ["News Item|1920x600", "UnitaOrganizzativa|900x900"],
            interface=IVocabulariesControlPanel,
        )

    def test_tipologia_notizia_vocab(self):
        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_notizia"
        )
        vocab = factory(self.portal)
        self.assertEqual(["", "xxx", "yyy"], [(x.value) for x in vocab])

    def test_tipologie_unita_organizzativa_vocab(self):
        factory = getUtility(
            IVocabularyFactory,
            "design.plone.vocabularies.tipologie_unita_organizzativa",
        )
        vocab = factory(self.portal)
        self.assertEqual(["", "foo", "bar"], [(x.value) for x in vocab])

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
        self.assertTrue(terms["UnitaOrganizzativa"] == "900x900")
