# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IDesignPloneContenttypesLayer)
class DefaultJSONSummarySerializer(BaseSerializer):
    def __call__(self):
        res = super(DefaultJSONSummarySerializer, self).__call__()
        res["id"] = self.context.id
        try:
            obj = self.context.getObject()
        except AttributeError:
            obj = self.context
        res["has_children"] = False
        try:
            if obj.aq_base.keys():
                res["has_children"] = True
        except AttributeError:
            return res
        return res
