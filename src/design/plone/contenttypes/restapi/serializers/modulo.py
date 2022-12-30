# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.interfaces.modulo import IModulo
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer,
)
from plone.dexterity.utils import iterSchemata
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.schema import getFields


@implementer(ISerializeToJsonSummary)
@adapter(IModulo, IDesignPloneContenttypesLayer)
class SerializeModuloToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self, force_all_metadata=False):
        summary = super().__call__(force_all_metadata=force_all_metadata)
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
