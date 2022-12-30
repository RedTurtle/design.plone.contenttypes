# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

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

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_has_children_returned_in_get_content(self):

        api.content.create(container=self.document, type="Document", title="empty")
        api.content.create(container=self.document, type="Document", title="filled")

        api.content.create(
            container=self.document["filled"], type="Document", title="Example"
        )
        commit()

        response = self.api_session.get(self.document.absolute_url())

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "empty")
        self.assertFalse(items[0]["has_children"])
        self.assertEqual(items[1]["title"], "filled")
        self.assertTrue(items[1]["has_children"])

    def test_has_children_not_returned_in_searches(self):

        api.content.create(container=self.document, type="Document", title="empty")
        api.content.create(container=self.document, type="Document", title="filled")

        api.content.create(
            container=self.document["filled"], type="Document", title="Example"
        )
        commit()

        response = self.api_session.get(
            "/@search?portal_type=Document&path.query=/plone/document&path.depth=1"
        )

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "empty")
        self.assertNotIn("has_children", items[0])
        self.assertEqual(items[1]["title"], "filled")
        self.assertNotIn("has_children", items[1])

    def test_has_children_not_returned_in_backend_serialization(self):

        empty = api.content.create(
            container=self.document, type="Document", title="empty"
        )
        filled = api.content.create(
            container=self.document, type="Document", title="filled"
        )

        api.content.create(
            container=self.document["filled"], type="Document", title="Example"
        )
        commit()

        empty_serialization = getMultiAdapter(
            (empty, self.request), ISerializeToJsonSummary
        )()
        filled_serialization = getMultiAdapter(
            (filled, self.request), ISerializeToJsonSummary
        )()

        self.assertNotIn("has_children", empty_serialization)
        self.assertNotIn("has_children", filled_serialization)

    def test_get_content_return_id_value(self):
        news = api.content.create(container=self.portal, type="News Item", title="news")
        commit()

        response = self.api_session.get(news.absolute_url())

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["id"], "multimedia")
        self.assertEqual(items[1]["id"], "documenti-allegati")

    def test_backend_serialization_return_id_value(self):
        serialization = getMultiAdapter(
            (self.document, self.request), ISerializeToJsonSummary
        )()

        self.assertEqual(serialization["id"], "document")

    def test_summary_return_formatted_remote_url_for_links(self):
        link = api.content.create(
            container=self.portal,
            type="Link",
            title="link",
            remoteUrl="	/plone/resolveuid/{}".format(self.document.UID()),
        )
        commit()

        response = self.api_session.get("@search?portal_type=Link")
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["remoteUrl"], self.document.absolute_url())

        serializer = getMultiAdapter((link, self.request), ISerializeToJsonSummary)()
        self.assertEqual(serializer["remoteUrl"], self.document.absolute_url())

    def test_summary_return_persona_role(self):

        api.content.create(
            container=self.portal, type="Persona", title="John Doe", ruolo="unknown"
        )
        api.content.create(container=self.portal, type="Persona", title="Mario Rossi")

        commit()

        brains = api.content.find(portal_type="Persona", id="mario-rossi")
        results = getMultiAdapter((brains, self.request), ISerializeToJson)(
            fullobjects=False
        )

        self.assertEqual(results["items"][0]["ruolo"], None)
        self.assertEqual(results["items"][0]["title"], "Mario Rossi")

        brains = api.content.find(portal_type="Persona", id="john-doe")
        results = getMultiAdapter((brains, self.request), ISerializeToJson)(
            fullobjects=False
        )

        self.assertEqual(results["items"][0]["ruolo"], "unknown")
        self.assertEqual(results["items"][0]["title"], "John Doe")

        # test also with restapi call
        response = self.api_session.get(
            "{}/@search?portal_type=Persona&id=mario-rossi".format(self.portal_url)
        )

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(items[0]["title"], "Mario Rossi")
        self.assertEqual(items[0]["ruolo"], None)

        response = self.api_session.get(
            "{}/@search?portal_type=Persona&id=john-doe".format(self.portal_url)
        )

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(items[0]["title"], "John Doe")
        self.assertEqual(items[0]["ruolo"], "unknown")

    def test_summary_return_design_meta_type(self):
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            tipologia_notizia="foo",
        )
        commit()

        response = self.api_session.get("@search?portal_type=News Item")
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["design_italia_meta_type"], "foo")

        serializer = getMultiAdapter((news, self.request), ISerializeToJsonSummary)()
        self.assertEqual(serializer["design_italia_meta_type"], "foo")

        # other contents return their name
        response = self.api_session.get("@search?UID={}".format(self.document.UID()))
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["design_italia_meta_type"], "Page")

        serializer = getMultiAdapter(
            (self.document, self.request), ISerializeToJsonSummary
        )()
        self.assertEqual(serializer["design_italia_meta_type"], "Page")

    def test_summary_return_tassonomia_argomenti_expanded(self):
        intids = getUtility(IIntIds)
        argomento = api.content.create(
            container=self.portal,
            type="Pagina Argomento",
            title="Argomento",
        )
        commit()

        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            tipologia_notizia="foo",
        )

        news.tassonomia_argomenti = [RelationValue(intids.getId(argomento))]
        news.reindexObject()
        commit()

        response = self.api_session.get(
            "@search?portal_type=News Item&metadata_fields=tassonomia_argomenti"
        )
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertEqual(len(items[0]["tassonomia_argomenti"]), 1)
        self.assertEqual(items[0]["tassonomia_argomenti"][0]["title"], argomento.title)

    def test_summary_do_not_return_tassonomia_argomenti_if_not_in_metadata_fields(self):
        intids = getUtility(IIntIds)
        argomento = api.content.create(
            container=self.portal,
            type="Pagina Argomento",
            title="Argomento",
        )
        commit()

        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            tipologia_notizia="foo",
        )

        news.tassonomia_argomenti = [RelationValue(intids.getId(argomento))]
        news.reindexObject()
        commit()

        response = self.api_session.get("@search?portal_type=News Item")
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertNotIn("tassonomia_argomenti", items[0])

        serializer = getMultiAdapter((news, self.request), ISerializeToJsonSummary)()
        self.assertNotIn("tassonomia_argomenti", serializer)

        response = self.api_session.get(
            "@search?portal_type=News Item&metadata_fields=tassonomia_argomenti"
        )
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertIn("tassonomia_argomenti", items[0])

        self.request.form["metadata_fields"] = "tassonomia_argomenti"
        serializer = getMultiAdapter((news, self.request), ISerializeToJsonSummary)()
        self.assertIn("tassonomia_argomenti", serializer)

        # works also with _all
        response = self.api_session.get(
            "@search?portal_type=News Item&metadata_fields=_all"
        )
        result = response.json()
        items = result.get("items", [])

        self.assertEqual(len(items), 1)
        self.assertIn("tassonomia_argomenti", items[0])

        self.request.form["metadata_fields"] = "_all"
        serializer = getMultiAdapter((news, self.request), ISerializeToJsonSummary)()
        self.assertIn("tassonomia_argomenti", serializer)
