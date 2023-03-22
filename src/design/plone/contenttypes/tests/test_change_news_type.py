# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class MoveNewsItemView(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        # default values are set in italian
        self.request["LANGUAGE"] = "it"
        self.view = api.content.get_view(
            "change_news_type", context=self.portal, request=self.request
        )

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.news_container = api.content.create(
            type="Folder",
            title="News container",
            container=self.portal,
        )
        self.news_item = api.content.create(
            type="News Item",
            title="news item",
            tipologia_notizia=["notizia"],
            container=self.portal,
        )
        self.news_item1 = api.content.create(
            type="News Item",
            title="news item1",
            tipologia_notizia=["notizia"],
            container=self.news_container,
        )

    def test_substitute_news_type(self):
        new_news_type = "comunicato_stampa"
        self.view.request.form["news_type_in_catalog"] = "notizia"
        self.view.request.form["news_type_portal"] = new_news_type
        self.view.request.form["substitute"] = "true"

        # mock the helper methods of our view
        self.view.news_types = lambda: [new_news_type]

        # self.portal.portal_catalog(ti)
        self.view.substitute_news_type()

        self.assertEqual(new_news_type, self.news_item.tipologia_notizia)
        self.assertEqual(new_news_type, self.news_item1.tipologia_notizia)
