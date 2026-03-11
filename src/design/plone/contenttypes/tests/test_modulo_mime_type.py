# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from design.plone.contenttypes.upgrades.to_730x import to_7321
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile

import os
import unittest


class TestModuloMimeType(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        filename = os.path.join(os.path.dirname(__file__), "example.pdf")
        with open(filename, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        # Build a real Modulo with a PDF as main file.
        self.documento = api.content.create(
            container=self.portal,
            type="Documento",
            title="Documento",
        )
        self.modulo = api.content.create(
            container=self.documento,
            type="Modulo",
            title="Modulo",
            file_principale=NamedBlobFile(
                data=pdf_data,
                filename="example.pdf",
                contentType="application/pdf",
            ),
        )
        self.modulo_2 = api.content.create(
            container=self.documento,
            type="Modulo",
            title="Modulo_2",
            file_principale=NamedBlobFile(
                data=pdf_data,
                filename="example.pdf",
                contentType="application/pdf",
            ),
        )
        self.enhancedlinks_tool = api.portal.get_tool("portal_enhancedlinks")
        # Simulate the stale cache entry that the upgrade has to refresh.
        self.enhancedlinks_tool._enhanced_links[self.modulo.UID()] = {
            "getObjSize": "1 KB",
            "mime_type": "text/plain",
        }

    def test_to_7321_refreshes_modulo_mime_type_cache(self):
        # Start from the broken cached mime type.
        self.assertEqual(
            self.enhancedlinks_tool.get_enhanced_link(self.modulo.UID())["mime_type"],
            "text/plain",
        )

        # The upgrade reindexes Modulo mime_type and refreshes enhanced links.
        to_7321(self.portal)

        # After the refresh the cache must reflect the PDF mime type.
        self.assertEqual(
            self.enhancedlinks_tool.get_enhanced_link(self.modulo.UID())["mime_type"],
            "application/pdf",
        )

    def test_modulo_mime_type_indexer(self):
        # The indexer should return the correct mime type for the Modulo.

        catalog = api.portal.get_tool("portal_catalog")
        results = catalog(UID=self.modulo_2.UID())
        brain = results[0]

        self.assertEqual(brain.mime_type, "application/pdf")
