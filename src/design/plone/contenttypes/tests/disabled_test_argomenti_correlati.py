# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestNews(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.argomento = api.content.create(
            container=self.portal,
            type="Pagina Argomento",
            title="Argomento foo",
        )

    def test_argomento_correctly_indexed(self):
        intids = getUtility(IIntIds)
        argomento_id = intids.getId(self.argomento)

        unita = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="Unità 1",
            tassonomia_argomenti=[RelationValue(argomento_id)],
        )

        pc = api.portal.get_tool('portal_catalog')
        self.assertEqual(
            pc.uniqueValuesFor('tassonomia_argomenti'), (self.argomento.UID(),)
        )
        self.assertEqual(
            api.content.find(tassonomia_argomenti=self.argomento.UID())[0].UID,
            unita.UID(),
        )
