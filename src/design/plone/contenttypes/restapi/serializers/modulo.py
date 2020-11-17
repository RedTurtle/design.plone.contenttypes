# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.modulo import IModulo
from plone.dexterity.utils import iterSchemata
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFields


@implementer(ISerializeToJsonSummary)
@adapter(IModulo, Interface)
class SerializeModuloToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self, version=None, include_items=True):
        summary = super(SerializeModuloToJsonSummary, self).__call__(
            version=version, include_items=include_items
        )
        fields = [
            "file_principale",
            "formato_alternativo_1",
            "formato_alternativo_2",
        ]
        for schema in iterSchemata(self.context):
            for name, field in getFields(schema).items():
                if name not in fields:
                    continue

                # serialize the field
                serializer = queryMultiAdapter(
                    (field, self.context, self.request), IFieldSerializer
                )
                value = serializer()
                summary[name] = value
        return summary
