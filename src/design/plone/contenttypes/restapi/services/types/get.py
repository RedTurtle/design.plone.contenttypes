# -*- coding: utf-8 -*-
from plone.restapi.services.types.get import TypesGet as BaseGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
    def reply(self):
        result = super(TypesGet, self).reply()
        if "fieldsets" in result:
            ids = [x["id"] for x in result["fieldsets"]]
            if "correlati" in ids:
                #  move correlati before categorization
                categorization_index = ids.index("categorization")
                correlati_index = ids.index("correlati")
                result["fieldsets"].insert(
                    categorization_index,
                    result["fieldsets"].pop(correlati_index),
                )
        return result
