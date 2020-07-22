# -*- coding: utf-8 -*-
from .related_news_serializer import (
    SerializeFolderToJson as RelatedNewsSerializer,
)
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)

from plone import api
from plone.restapi.interfaces import ISerializeToJson, ISerializeToJsonSummary
from zope.component import adapter, getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IUnitaOrganizzativa, Interface)
class UOSerializer(RelatedNewsSerializer):
    def __call__(self, version=None, include_items=True):
        self.index = "news_uo"
        result = super(UOSerializer, self).__call__(
            version=None, include_items=True
        )

        self.index = "ufficio_responsabile"
        catalog = api.portal.get_tool("portal_catalog")
        query = {
            self.index: result["UID"],
            "portal_type": ["Servizio"],
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }
        # import pdb

        # pdb.set_trace()
        brains = catalog(**query)

        servizi = [
            getMultiAdapter((x, self.request), ISerializeToJsonSummary)()
            for x in brains
        ]
        result["servizi_offerti"] = servizi

        return result
