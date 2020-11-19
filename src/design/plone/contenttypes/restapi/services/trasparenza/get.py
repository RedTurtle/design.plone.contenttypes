# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from Products.CMFCore.interfaces import IFolderish


TRASPARENZA_FIELDS = [
    "modalita_avvio",
    "descrizione",
    "soggetti_esterni",
    "decorrenza_termine",
    "dove_rivolgersi",
    "dove_rivolgersi_extra",
    "fine_termine",
    "silenzio_assenso",
    "ufficio_responsabile",
    "provvedimento_finale",
    "organo_competente_provvedimento_finale",
    "modalita_richiesta_informazioni",
    "procedura_online",
    "altre_modalita_invio",
    "atti_documenti_corredo",
    "reperimento_modulistica",
    "pagamenti",
    "strumenti_tutela",
    "titolare_potere_sostitutivo",
    "customer_satisfaction",
    "riferimenti_normativi",
    "tempo_medio",
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


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class TrasparenzaItems(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        if "amministrazione-trasparente" not in self.context.absolute_url():
            return {}

        result = {
            "trasparenza-items": {
                "@id": "{}/@trasparenza-items".format(
                    self.context.absolute_url()
                )
            }
        }
        if not expand:
            return result
        data = self.get_trasparenza_data()
        if data:
            result["trasparenza-items"] = {"items": data}
        return result

    def get_trasparenza_data(self, context=None):
        if context is None:
            context = self.context
        res = []

        for child in context.listFolderContents():
            serializer = queryMultiAdapter(
                (child, self.request), ISerializeToJsonSummary
            )
            data = serializer()
            if child.portal_type == "Document":

                if IFolderish.providedBy(child):
                    children = [
                        x
                        for x in self.get_trasparenza_data(context=child)
                        if x.get("@type", "") in ["Document", ]
                    ]
                    if children:
                        data["items"] = children
            res.append(data)
        return res


class TrasparenzaItemsGet(Service):
    def reply(self):
        data = TrasparenzaItems(self.context, self.request)
        return data(expand=True)["trasparenza-items"]
