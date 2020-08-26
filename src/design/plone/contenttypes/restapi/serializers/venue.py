# -*- coding: utf-8 -*-
from .related_news_serializer import (
    SerializeFolderToJson as RelatedNewsSerializer,
)

from collective.venue.interfaces import IVenue

from plone import api
from plone.restapi.interfaces import ISerializeToJson, ISerializeToJsonSummary
from zope.component import adapter, getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IVenue, Interface)
class VenueSerializer(RelatedNewsSerializer):
    def search(self, index, UID):
        catalog = api.portal.get_tool("portal_catalog")
        query = {
            index: UID,
            "portal_type": ["Servizio"],
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        return catalog(**query)

    def get_venue_services(self, result):
        brains = self.search("service_venue", result["UID"])
        servizi = [
            getMultiAdapter((x, self.request), ISerializeToJsonSummary)()
            for x in brains
        ]
        result["venue_services"] = servizi
        return result

    def get_venue_offices(self, result):
        brains = self.search("office_venue", result["UID"])
        offices = [
            getMultiAdapter((x, self.request), ISerializeToJsonSummary)()
            for x in brains
        ]
        result["venue_offices"] = offices
        return result

    def __call__(self, version=None, include_items=True):
        self.index = "news_venue"
        result = super(VenueSerializer, self).__call__(
            version=None, include_items=True
        )
        result = self.get_venue_services(result)
        result = self.get_venue_offices(result)
        return result
