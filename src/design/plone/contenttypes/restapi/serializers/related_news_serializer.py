# -*- coding: utf-8 -*-
from .dxcontent import SerializeFolderToJson as BaseSerializer
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class SerializeFolderToJson(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        # if include_items:
        #     self.request.form = {"fullobjects": ""}
        result = super(SerializeFolderToJson, self).__call__(
            version=version, include_items=include_items
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
@adapter(IServizio, Interface)
class ServizioSerializer(SerializeFolderToJson):
    index = "news_service"
