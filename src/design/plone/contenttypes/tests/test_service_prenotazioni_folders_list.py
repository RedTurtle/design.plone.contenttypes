# -*- coding: utf-8 -*-
# TODO: skip se redturtle.prenotazioni non è presente
from design.plone.contenttypes.testing import (
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


class TestServicePrnotazioniFoldersList(unittest.TestCase):
    layer = DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.testing_view_name = "@prenotazioni_folders-list"

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})

        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.servizio = api.content.create(
            type="Servizio", title="servizio", container=self.portal
        )
        self.prenotazioni_folders_folder = api.content.create(
            type="Folder", title="PrenotazioniFolders", container=self.servizio
        )

        transaction.commit()

    def test_no_prenotazioni_folders(self):
        res = self.api_session.get(
            self.servizio.absolute_url() + "/" + self.testing_view_name
        ).json()

        self.assertFalse(res)

    def test_prenotazioni_folders(self):
        prenotazione_folder = api.content.create(
            type="PrenotazioniFolder",
            title="prenotazioni_folder",
            container=self.prenotazioni_folders_folder,
        )
        transaction.commit()

        res = self.api_session.get(
            self.servizio.absolute_url() + "/" + self.testing_view_name
        ).json()

        self.assertIn(prenotazione_folder.absolute_url(), [item["@id"] for item in res])
