# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from uuid import uuid4

import json
import transaction
import unittest


class TestNews(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING
    maxDiff = None

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_news(self):
        portal_types = api.portal.get_tool(name="portal_types")

        self.assertEqual(
            portal_types["News Item"].behaviors,
            (
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "plone.versioning",
                "plone.locking",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.news",
                "design.plone.contenttypes.behavior.argomenti_news",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "collective.taxonomy.generated.tipologia_notizia",
            ),
        )

    def test_news_item_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual("Notizie e comunicati stampa", portal_types["News Item"].title)

    def test_news_item_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            sorted(("Image", "File", "Link", "Document")),
            sorted(portal_types["News Item"].allowed_content_types),
        )

    def test_news_provide_design_pct_marker_interface(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        news = api.content.create(container=self.portal, type="News Item", title="News")
        self.assertTrue(IDesignPloneContentType.providedBy(news))


class TestNewsApi(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )

        # we need it because of vocabularies
        api.portal.set_registry_record(
            "tipologie_notizia",
            json.dumps({"en": ["foo", "bar"]}),
            interface=IDesignPloneSettings,
        )
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_newsitem_required_fields(self):
        response = self.api_session.post(
            self.portal_url, json={"@type": "News Item", "title": "Foo"}
        )

        self.assertEqual(response.status_code, 400)
        message = response.json()["message"]
        # TODO: anche `tipologia_notizia` è obbligatorio ?
        # self.assertIn("tipologia_notizia", message)
        self.assertIn("descrizione_estesa", message)

        text_uuid = str(uuid4())
        response = self.api_session.post(
            self.portal_url,
            json={
                "@type": "News Item",
                "title": "Foo",
                # TODO: se la tipologia non è nel vocabolario della
                # tassonomia, il server restituisce un errore 500
                # "tipologia_notizia": "foo",
                "tipologia_notizia": "avviso",
                "a_cura_di": self.document.UID(),
                # campo obbligatorio
                "description": "Test",
                # campo obbligatorio
                "descrizione_estesa": {
                    "blocks": {
                        text_uuid: {
                            "@type": "text",
                            "text": {"blocks": [{"text": "Test", "type": "paragraph"}]},
                        },
                    },
                    "blocks_layout": {"items": [text_uuid]},
                },
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_newsitem_substructure_created(self):
        text_uuid = str(uuid4())
        response = self.api_session.post(
            self.portal_url,
            json={
                "@type": "News Item",
                "title": "Foo",
                # TODO: se la tipologia non è nel vocabolario della
                # tassonomia, il server restituisce un errore 500
                # "tipologia_notizia": "foo",
                "tipologia_notizia": "avviso",
                "a_cura_di": self.document.UID(),
                # campo obbligatorio
                "description": "Test",
                # campo obbligatorio
                "descrizione_estesa": {
                    "blocks": {
                        text_uuid: {
                            "@type": "text",
                            "text": {"blocks": [{"text": "Test", "type": "paragraph"}]},
                        },
                    },
                    "blocks_layout": {"items": [text_uuid]},
                },
            },
        )
        self.assertEqual(response.status_code, 201)

        response = self.api_session.get(
            f"{self.portal_url}/foo", params={"fullobjects": 1}
        )
        self.assertEqual(response.status_code, 200)
        news = response.json()

        self.assertEqual(
            set([i["id"] for i in news["items"]]),
            set(["multimedia", "documenti-allegati"]),
        )
        self.assertEqual(news["description"], "Test")
        self.assertIn(
            '"text": "Test"',
            json.dumps(news["descrizione_estesa"]),
        )

        # self.assertEqual(news["multimedia"].portal_type, "Document")
        # self.assertEqual(news["multimedia"].constrain_types_mode, 1)
        # self.assertEqual(news["multimedia"].locally_allowed_types, ("Link", "Image"))

        # self.assertEqual(news["documenti-allegati"].portal_type, "Document")
        # self.assertEqual(news["documenti-allegati"].constrain_types_mode, 1)
        # self.assertEqual(
        #     news["documenti-allegati"].locally_allowed_types, ("File", "Image")
        # )

    def test_cant_patch_news_that_has_no_required_fields(self):
        news = api.content.create(container=self.portal, type="News Item", title="Foo")
        transaction.commit()
        resp = self.api_session.patch(
            news.absolute_url(),
            json={
                "title": "Foo modified",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("La descrizione è obbligatoria", resp.json()["message"])

    def test_can_sort_news_that_has_no_required_fields(self):
        news = api.content.create(container=self.portal, type="News Item", title="News")
        transaction.commit()

        self.assertEqual(self.document, self.portal.listFolderContents()[0])
        self.assertEqual(news, self.portal.listFolderContents()[1])

        resp = self.api_session.patch(
            self.portal_url,
            json={"ordering": {"delta": -1, "obj_id": news.getId()}},
        )
        transaction.commit()

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.document, self.portal.listFolderContents()[1])
        self.assertEqual(news, self.portal.listFolderContents()[0])
