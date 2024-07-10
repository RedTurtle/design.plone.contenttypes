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

import os
import transaction
import unittest


class TestDocumentoSchema(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING
    maxDiff = None

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

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
                "volto.preview_image",
                "design.plone.contenttypes.behavior.argomenti_documento",
                "design.plone.contenttypes.behavior.descrizione_estesa_documento",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "collective.taxonomy.generated.person_life_events",
                "collective.taxonomy.generated.business_events",
                "collective.taxonomy.generated.tipologia_documenti_albopretorio",
                "collective.taxonomy.generated.tipologia_documento",
                "collective.taxonomy.generated.tipologia_licenze",
            ),
        )

    def test_documento_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Document", "Modulo", "Link"),
            portal_types["Documento"].allowed_content_types,
        )

    def test_documento_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(len(resp["fieldsets"]), 9)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "descrizione",
                "informazioni",
                "settings",
                "correlati",
                "categorization",
                "dates",
                "ownership",
                "seo",
            ],
        )

    def test_documento_required_fields(self):
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "formati_disponibili",
                    "tassonomia_argomenti",
                    "tipologia_documento",
                    "ufficio_responsabile",
                    "tipologia_licenze",
                    "description",
                ]
            ),
        )

    def test_documento_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "identificativo",
                "protocollo",
                "data_protocollo",
                "formati_disponibili",
                "dataset",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tassonomia_argomenti",
                "person_life_events",
                "business_events",
                "tipologia_documenti_albopretorio",
                "tipologia_documento",
            ],
        )

    def test_documento_fields_descrizione_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "ufficio_responsabile",
                "area_responsabile",
                "autori",
                "licenza_distribuzione",
                "descrizione_estesa",
                "tipologia_licenze",
            ],
        )

    def test_documento_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["riferimenti_normativi", "documenti_allegati", "ulteriori_informazioni"],
        )

    def test_documento_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_documento_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["correlato_in_evidenza"],
        )

    def test_documento_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"], ["subjects", "language", "relatedItems"]
        )

    def test_documento_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["effective", "expires"])

    def test_documento_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"], ["creators", "contributors", "rights"]
        )

    def test_documento_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            [
                "seo_title",
                "seo_description",
                "seo_noindex",
                "seo_canonical_url",
                "opengraph_title",
                "opengraph_description",
                "opengraph_image",
            ],
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
            filename = os.path.join(os.path.dirname(__file__), "example.pdf")
            child.file = NamedBlobFile(
                data=open(filename, "rb").read(),
                filename="example.pdf",
                contentType="application/pdf",
            )
        transaction.commit()
        response = self.api_session.get(self.documento.absolute_url())
        res = response.json()
        self.assertEqual(len(res["items"]), len(self.documento.listFolderContents()))

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

    def test_cant_patch_document_that_has_no_required_fields(self):
        new_documento = api.content.create(
            container=self.portal, type="Documento", title="Foo"
        )
        transaction.commit()
        resp = self.api_session.patch(
            new_documento.absolute_url(),
            json={
                "title": "Foo modified",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("La descrizione è obbligatoria", resp.json()["message"])

    def test_can_sort_document_that_has_no_required_fields(self):
        new_documento = api.content.create(
            container=self.portal, type="Documento", title="Foo"
        )
        transaction.commit()

        self.assertEqual(self.documento, self.portal.listFolderContents()[0])
        self.assertEqual(new_documento, self.portal.listFolderContents()[1])

        resp = self.api_session.patch(
            self.portal_url,
            json={"ordering": {"delta": -1, "obj_id": new_documento.getId()}},
        )
        transaction.commit()

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.documento, self.portal.listFolderContents()[1])
        self.assertEqual(new_documento, self.portal.listFolderContents()[0])
