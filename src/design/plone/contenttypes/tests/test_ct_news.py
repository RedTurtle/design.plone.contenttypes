# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.vocabularies import (
    IVocabulariesControlPanel,
)
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import transaction
import unittest


class TestNews(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_news(self):
        portal_types = api.portal.get_tool(name="portal_types")

        self.assertEqual(
            portal_types["News Item"].behaviors,
            (
                "plone.dublincore",
                "plone.leadimage",
                "design.plone.contenttypes.behavior.news",
                "design.plone.contenttypes.behavior.argomenti",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "volto.blocks",
            ),
        )

    def test_news_item_ct_title(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            "Notizie e comunicati stampa", portal_types["News Item"].title
        )

    def test_news_item_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            sorted(("Image", "File", "Link", "Document")),
            sorted(portal_types["News Item"].allowed_content_types),
        )


class TestNewsApi(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        api.portal.set_registry_record(
            "tipologie_notizia",
            ["xxx", "yyy"],
            interface=IVocabulariesControlPanel,
        )

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )

        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_newsitem_required_fields(self):
        response = self.api_session.post(
            self.portal_url, json={"@type": "News Item", "title": "Foo"}
        )

        self.assertEqual(400, response.status_code)
        message = response.json()["message"]
        self.assertIn("tipologia_notizia", message)

        response = self.api_session.post(
            self.portal_url,
            json={
                "@type": "News Item",
                "title": "Foo",
                "tipologia_notizia": "xxx",
                "a_cura_di": self.document.UID(),
            },
        )
        self.assertEqual(201, response.status_code)

    def test_newsitem_substructure_created(self):
        self.api_session.post(
            self.portal_url,
            json={
                "@type": "News Item",
                "title": "Foo",
                "tipologia_notizia": "xxx",
                "a_cura_di": self.document.UID(),
            },
        )

        transaction.commit()
        news = self.portal["foo"]

        self.assertEqual(["multimedia", "documenti-allegati"], news.keys())

        self.assertEqual(news["multimedia"].portal_type, "Document")
        self.assertEqual(news["multimedia"].constrain_types_mode, 1)
        self.assertEqual(
            news["multimedia"].locally_allowed_types, ("Link", "Image")
        )

        self.assertEqual(news["documenti-allegati"].portal_type, "Document")
        self.assertEqual(news["documenti-allegati"].constrain_types_mode, 1)
        self.assertEqual(
            news["documenti-allegati"].locally_allowed_types, ("File", "Image")
        )
