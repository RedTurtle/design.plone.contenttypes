# -*- coding: utf-8 -*-

from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from plone import api
from plone.namedfile.file import NamedBlobFile

import unittest
import transaction
import os


class TestDocument(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_documento(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Documento"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.dublincore",
                "plone.relateditems",
                "plone.locking",
                "plone.constraintypes",
                "plone.leadimage",
                "design.plone.contenttypes.behavior.argomenti_documento",
                "design.plone.contenttypes.behavior.descrizione_estesa_documento",  # noqa
                "design.plone.contenttypes.behavior.additional_help_infos",
                "collective.dexteritytextindexer",
                "plone.translatable",
                "kitconcept.seo",
            ),
        )

    def test_event_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Document", "Modulo", "Link"),
            portal_types["Documento"].allowed_content_types,
        )


class TestDocumentoApi(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        self.documento = api.content.create(
            container=self.portal, type="Documento", title="Documento"
        )

        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_document_get_return_more_than_25_results_by_default(self):
        for i in range(50):
            child = api.content.create(
                container=self.documento,
                type="Modulo",
                title="File {}".format(i),
            )
            filename = os.path.join(os.path.dirname(__file__), u"example.pdf")
            child.file = NamedBlobFile(
                data=open(filename, "rb").read(),
                filename="example.pdf",
                contentType="application/pdf",
            )
        transaction.commit()
        response = self.api_session.get(self.documento.absolute_url())
        res = response.json()
        self.assertEqual(
            len(res["items"]), len(self.documento.listFolderContents())
        )

    def test_post_file_will_convert_into_modulo(self):
        response = self.api_session.post(
            self.documento.absolute_url(),
            json={
                "@type": "File",
                "title": "My File",
                "file": {
                    "filename": "test.txt",
                    "data": "Spam and Eggs",
                    "content_type": "text/plain",
                },
            },
        )
        self.assertEqual(201, response.status_code)
        transaction.commit()

        self.assertEqual(self.documento["my-file"].portal_type, "Modulo")

    def test_post_image_will_convert_into_modulo(self):
        response = self.api_session.post(
            self.documento.absolute_url(),
            json={
                "@type": "Image",
                "title": "My Image",
                "image": {
                    "filename": "image.jpg",
                    "data": "Spam and Eggs",
                    "content_type": "image/jpeg",
                },
            },
        )
        self.assertEqual(201, response.status_code)
        transaction.commit()

        self.assertEqual(self.documento["my-image"].portal_type, "Modulo")
