from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from plone.restapi.services import Service

TRASPARENZA_FIELDS = [
    "modalita_avvio",
    "descrizione",
    "soggetti_esterni",
    "decorrenza_termine",
    "dove_rivolgersi",
    "dove_rivolgersi_extra",
    "fine_termine",
    "silenzio_assenso",
    "provvedimento_finale",
    "organo_competente_provvedimento_finale",
    "procedura_online",
    "altre_modalita_invio",
    "atti_documenti_corredo",
    "reperimento_modulistica",
    "pagamenti",
    "strumenti_tutela",
    "titolare_potere_sostitutivo",
    "customer_satisfaction",
    "riferimenti_normativi",
    "tempo medio",
    "file_correlato",
    "responsabile_procedimento",
    "dirigente",
]


class TrasparenzaService(Service):
    def reply(self):
        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog(**{"UID": self.request.uid})[0]
        obj = getMultiAdapter(
            (brains.getObject(), getRequest()), ISerializeToJson
        )()
        result = {}
        for field in TRASPARENZA_FIELDS:
            result[field] = obj.get(field)
        return result
