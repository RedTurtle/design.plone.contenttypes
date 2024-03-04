# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from transaction import commit
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import json
import unittest


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
