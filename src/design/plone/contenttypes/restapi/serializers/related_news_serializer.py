# -*- coding: utf-8 -*-
from .dxcontent import SerializeFolderToJson as BaseSerializer
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.component import getMultiAdapter
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
        result["related_news"] = [self.serialize_brain(x) for x in brains]
        return result

    def serialize_brain(self, brain):
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        if brain.effective.Date() != "1969/12/31":
            data["effective"] = json_compatible(brain.effective)
        else:
            data["effective"] = None
        data["typology"] = brain.tipologia_notizia or ""

        return data


@implementer(ISerializeToJson)
@adapter(IServizio, Interface)
class ServizioSerializer(SerializeFolderToJson):
    index = "news_service"
