# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.cartella_modulistica import (
    ICartellaModulistica,
)
from plone.dexterity.utils import iterSchemata
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFCore.interfaces import IFolderish
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFields


@implementer(IExpandableElement)
@adapter(ICartellaModulistica, Interface)
class ModulisticaItems(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "modulistica-items": {
                "@id": "{}/@modulistica-items".format(self.context.absolute_url())
            }
        }
        if not expand:
            return result

        data = self.get_modulistica_data()
        if data:
            result["modulistica-items"] = {"items": data}
        return result

    def get_modulistica_data(self, context=None):
        if context is None:
            context = self.context
        res = []
        for child in context.listFolderContents():
            if child.portal_type == "Document" and child.getId() == "multimedia":
                continue

            serializer = queryMultiAdapter(
                (child, self.request), ISerializeToJsonSummary
            )
            data = serializer()
            if child.portal_type == "Document":
                for schema in iterSchemata(context):
                    for name, field in getFields(schema).items():
                        if name not in ["blocks", "blocks_layout"]:
                            continue

                        # serialize the field
                        serializer = queryMultiAdapter(
                            (field, child, self.request), IFieldSerializer
                        )
                        value = serializer()
                        data[json_compatible(name)] = value
            if IFolderish.providedBy(child):
                children = [
                    x
                    for x in self.get_modulistica_data(context=child)
                    if x.get("@type", "") not in ["Document", "CartellaModulistica"]
                ]
                if children:
                    data["items"] = children
            res.append(data)
        return res


class ModulisticaItemsGet(Service):
    def reply(self):
        data = ModulisticaItems(self.context, self.request)
        return data(expand=True)["modulistica-items"]
