# -*- coding: utf-8 -*-
from .related_news_serializer import (
    SerializeFolderToJson as RelatedNewsSerializer,
)

from Acquisition import aq_inner
from collective.venue.interfaces import IVenue
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer,
)
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from zc.relation.interfaces import ICatalog
from zope.component import adapter, getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


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
        return servizi

    def get_venue_offices(self, result):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        offices = []
        for attr in ["sede", "sedi_secondarie"]:
            relations = catalog.findRelations(
                dict(
                    to_id=intids.getId(aq_inner(self.context)),
                    from_attribute=attr,
                )
            )

            for rel in relations:
                obj = intids.queryObject(rel.from_id)
                if obj is not None and checkPermission("zope2.View", obj):
                    summary = getMultiAdapter(
                        (obj, getRequest()), ISerializeToJsonSummary
                    )()
                    offices.append(summary)
        return sorted(offices, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        self.index = "news_venue"
        result = super(VenueSerializer, self).__call__(
            version=None, include_items=True
        )
        result["venue_services"] = self.get_venue_services(result)
        result["sede_di"] = self.get_venue_offices(result)
        return result


@implementer(ISerializeToJsonSummary)
@adapter(IVenue, Interface)
class SerializeVenueToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self):
        summary = super(SerializeVenueToJsonSummary, self).__call__()
        fields = [
            "street",
            "zip_code",
            "city",
            "country",
            "geolocation",
            "orario_pubblico",
            "telefono",
            "fax",
            "email",
            "pec",
            "web",
            "riferimento_telefonico_struttura",
            "riferimento_mail_struttura",
            "riferimento_pec_struttura",
        ]
        for field in fields:
            value = getattr(self.context, field, None)
            if callable(value):
                value = value()
            summary[field] = json_compatible(value)
        return summary
