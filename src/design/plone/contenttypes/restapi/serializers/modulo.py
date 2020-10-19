# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.modulo import IModulo
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJsonSummary)
@adapter(IModulo, Interface)
class SerializeModuloToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self, version=None, include_items=True):
        summary = super(SerializeModuloToJsonSummary, self).__call__()
        fields = [
            "file_principale",
            "formato_alternativo_1",
            "formato_alternativo_2",
        ]
        for field in fields:
            value = getattr(self.context, field, None)
            if callable(value):
                value = value()
            summary[field] = json_compatible(value)
        return summary
