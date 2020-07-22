# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseSerializer,
)
from design.plone.contenttypes.interfaces.pagina_argomento import (
    IPaginaArgomento,
)
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from plone import api


@implementer(ISerializeToJson)
@adapter(IPaginaArgomento, Interface)
class PaginaArgomentoSerializer(BaseSerializer):
    def __call__(self, version=None, include_items=False):
        result = super(PaginaArgomentoSerializer, self).__call__(
            version=None, include_items=False
        )
        self.index = "argomenti_correlati"

        catalog = api.portal.get_tool("portal_catalog")
        query = {
            self.index: result["UID"],
            "portal_type": [
                # "Servizio",
                "UnitaOrganizzativa",
                # "Documento",
                # "NewsItem",
            ],
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        brains = catalog(**query)
        responsible_UOs = []
        for x in brains:
            obj = x.getObject()
            responsible_UOs.append(
                {
                    "title": x.Title or "",
                    "description": x.Description or "",
                    "@id": x.getURL() or "",
                    "street": obj.street,
                    "zip_code": obj.zip_code,
                }
            )
        result["unita_amministrativa_responsabile"] = responsible_UOs
        # related_services = []
        # related_uos = []
        # related_news = []
        # related_docs = []
        # for x in brains:

        #     if x.portal_type == "Servizio":
        #         related_services.append(
        #             {
        #                 "title": x.Title or "",
        #                 "description": x.Description or "",
        #                 "@id": x.getURL() or "",
        #             }
        #         )
        #     if x.portal_type == "UnitaOrganizzativa":
        #         related_uos.append(
        #             {
        #                 "title": x.Title or "",
        #                 "description": x.Description or "",
        #                 "@id": x.getURL() or "",
        #             }
        #         )
        #     if x.portal_type == "NewsItem":
        #         related_news.append(
        #             {
        #                 "title": x.Title or "",
        #                 "description": x.Description or "",
        #                 "effective": x.effective
        #                 and x.effective.__str__()
        #                 or "",
        #                 "@id": x.getURL() or "",
        #             }
        #         )
        #     if x.portal_type == "Documento":
        #         related_docs.append(
        #             {
        #                 "title": x.Title or "",
        #                 "description": x.Description or "",
        #                 "@id": x.getURL() or "",
        #             }
        #         )

        # result["related_uo"] = related_uos
        # result["related_news"] = related_news
        # result["related_services"] = related_services
        # result["related_docs"] = related_docs

        return result
