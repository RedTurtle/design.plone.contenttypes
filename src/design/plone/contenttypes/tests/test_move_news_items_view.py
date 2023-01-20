from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone import api

from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING,
)

import unittest


class MoveNewsItemView(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.view = api.content.get_view(
            "move_news_items", context=self.portal, request=self.request
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
            tipologia_notizia="Notizia",
            container=self.portal,
        )
        self.news_item1 = api.content.create(
            type="News Item",
            title="news item1",
            tipologia_notizia="Notizia",
            container=self.news_container,
        )

    def test_news_result(self):
        self.view.request.form["news_type"] = "Notizia"

        result = self.view.news_results()

        self.assertIn(self.news_item.UID(), [i.UID for i in result])
        self.assertIn(self.news_item1.UID(), [i.UID for i in result])

    def test_move_data(self):
        self.view.request.form[self.news_item.UID()] = "on"
        self.view.request.form[self.news_item1.UID()] = "on"
        self.view.request.form["move"] = "true"
        self.view.request.form["to_path"] = "/".join(
            self.news_container.getPhysicalPath()
        )

        self.view.move_data()

        self.assertIn(self.news_item, self.news_container.listFolderContents())
        self.assertIn(self.news_item1, self.news_container.listFolderContents())

    def test_bad_data_endurance(self):
        """Test instatnce endurance to bad data"""
        bad_uid = "bad_uid"
        bad_path = "bad_path"
        self.view.request.form["move"] = "true"

        self.view.request.form["bad_uid"] = "on"

        self.view.move_data()

        self.view.request.form.pop(bad_uid)

        self.view.request.form[self.news_item.UID()] = "on"
        self.view.request.form["to_path"] = bad_path

        self.view.move_data()
