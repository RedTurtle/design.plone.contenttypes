# -*- coding: utf-8 -*-

"""Setup tests for this package."""
from design.plone.contenttypes.testing import (
    DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class TestBaseSerializer(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.news = api.content.create(
            container=self.portal, type="News Item", title="TestNews"
        )
        self.news.tipologia_notizia = "Comunicati stampa"
        self.service = api.content.create(
            container=self.portal, type="Servizio", title="TestService"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_design_italia_meta_type_with_news(self):
        """
        News should return the news type (tipologia_notizia field)
        Other types shoule return their own portal_type.
        """
        response_news = self.api_session.get(self.news.absolute_url() + "?fullobjects")
        self.assertTrue(
            response_news.json()["design_italia_meta_type"] == "Comunicati stampa"
        )

    def test_design_italia_meta_type_with_type_different_from_news(self):
        """
        News should return the news type (tipologia_notizia field)
        Other types shoule return their own portal_type.
        """
        response_service = self.api_session.get(
            self.service.absolute_url() + "?fullobjects"
        )
        self.assertTrue(
            response_service.json()["design_italia_meta_type"] == "Servizio"
        )
