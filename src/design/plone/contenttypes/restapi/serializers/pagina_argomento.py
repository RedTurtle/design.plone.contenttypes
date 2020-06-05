# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseSerializer,
)
from design.plone.contenttypes.interfaces.pagina_argomento import (
    IPaginaArgomento,
)
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


def get_related_news(catalog, argomento):
    limit = 4
    query = {
        "portal_type": ["News Item"],
        "sort_on": "effective",
        "sort_order": "descending",
        "sort_limit": limit,
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)[:limit]
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "effective": x.effective and x.effective.__str__() or "",
            "@id": x.getURL() or "",
            "typology": x.tipologia_notizia or "",
        }
        for x in brains
    ]


def get_related_servizio(catalog, argomento):
    query = {
        "portal_type": ["Servizio"],
        "sort_on": "sortable_title",
        "sort_order": "ascending",
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "@id": x.getURL() or "",
        }
        for x in brains
    ]


def get_related_uo(catalog, argomento):
    query = {
        "portal_type": ["Unita organizzativa"],
        "sort_on": "sortable_title",
        "sort_order": "ascending",
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "@id": x.getURL() or "",
        }
        for x in brains
    ]


def get_related_doc(catalog, argomento):
    query = {
        "portal_type": ["Documento"],
        "sort_on": "sortable_title",
        "sort_order": "ascending",
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "@id": x.getURL() or "",
        }
        for x in brains
    ]


@implementer(ISerializeToJson)
@adapter(IPaginaArgomento, Interface)
class PaginaArgomentoSerializer(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(PaginaArgomentoSerializer, self).__call__(
            version=None, include_items=True
        )
        # ptypes = api.portal.get_tool("portal_types")
        # behaviours_argomenti = ptypes["Pagina Argomento"].behaviors
        # result["is_using_blokcs"] = "volto.blocks" in behaviours_argomenti
        # if result["is_using_blocks"]:
        #     # don't waste your time: if we are using block, we don't need other
        #     # info
        #     return True

        catalog = api.portal.get_tool("portal_catalog")
        result["related_news"] = get_related_news(
            catalog, self.context.tassonomia_argomenti
        )
        result["related_services"] = get_related_servizio(
            catalog, self.context.tassonomia_argomenti
        )

        result["related_uo"] = get_related_uo(
            catalog, self.context.tassonomia_argomenti
        )

        result["related_docs"] = get_related_doc(
            catalog, self.context.tassonomia_argomenti
        )

        return result
