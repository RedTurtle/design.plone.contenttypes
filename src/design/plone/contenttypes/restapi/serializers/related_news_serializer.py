# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseSerializer,
)
from design.plone.contenttypes.interfaces.persona import IPersona
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class SerializeFolderToJson(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(SerializeFolderToJson, self).__call__(
            version=None, include_items=True
        )
        catalog = api.portal.get_tool("portal_catalog")
        limit = 3
        query = {
            self.index: result["UID"],
            "portal_type": ["News Item"],
            "sort_on": "effective",
            "sort_order": "descending",
            "sort_limit": limit,
        }

        brains = catalog(**query)[:limit]
        news = [
            {
                "title": x.Title or "",
                "description": x.Description or "",
                "effective": x.effective and x.effective.__str__() or "",
                "@id": x.getURL() or "",
                "typology": x.tipologia_notizia or "",
            }
            for x in brains
        ]
        result["related_news"] = news
        return result


@implementer(ISerializeToJson)
@adapter(IPersona, Interface)
class PersonaSerializer(SerializeFolderToJson):
    index = "news_people"


@implementer(ISerializeToJson)
@adapter(IServizio, Interface)
class ServizioSerializer(SerializeFolderToJson):
    index = "news_service"
