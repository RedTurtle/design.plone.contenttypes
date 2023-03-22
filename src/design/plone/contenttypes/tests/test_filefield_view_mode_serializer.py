# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class SummarySerializerTest(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.cartella_modulistica = api.content.create(
            container=self.portal,
            type="CartellaModulistica",
            title="Cartella Modulistica",
        )
        self.document = api.content.create(
            container=self.cartella_modulistica, type="Documento", title="Document"
        )
        self.modulo = api.content.create(
            container=self.document,
            type="Modulo",
            title="Modulo",
            file_principale=NamedBlobFile("some data", filename="file.pdf"),
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_if_visualize_files_false_so_download(self):
        response = self.api_session.get(self.modulo.absolute_url()).json()

        self.assertIn("@@download", response["file_principale"]["download"])

    def test_if_visualize_files_true_so_dsiplay(self):
        self.cartella_modulistica.visualize_files = True

        commit()

        response = self.api_session.get(self.modulo.absolute_url()).json()

        self.assertIn("@@display-file", response["file_principale"]["download"])
