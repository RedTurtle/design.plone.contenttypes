# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.servizio import IServizio
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer,
)
from plone.dexterity.utils import iterSchemata
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFields


@implementer(ISerializeToJsonSummary)
@adapter(IServizio, Interface)
class SerializeServizioToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self):
        """
        Ritorna sempre una serie di campi extra
        """
        summary = super(SerializeServizioToJsonSummary, self).__call__()
        fields = ["canale_digitale"]
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
