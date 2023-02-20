from plone import api
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from zope.component import getMultiAdapter


class PrenotazioniFoldersList(Service):
    def reply(self):
        """Lists the PrenotableFolders inside of Servizio
        Returns:
            list: List of PrenotableFolders serialized to JSON summary
        """
        result = []

        prenotazioni_folders = api.portal.get_tool("portal_catalog")(
            portal_type="PrenotazioniFolder",
            path="/".join(self.context.getPhysicalPath()),
        )

        for item in prenotazioni_folders:
            result.append(
                getMultiAdapter(
                    (item.getObject(), self.request), ISerializeToJsonSummary
                )()
            )

        return result
