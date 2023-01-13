# -*- coding: utf-8 -*-
from .related_news_serializer import SerializeFolderToJson as RelatedNewsSerializer
from Acquisition import aq_inner
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer,
)
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


@implementer(ISerializeToJson)
@adapter(IUnitaOrganizzativa, Interface)
class UOSerializer(RelatedNewsSerializer):
    def get_services(self):
        """ """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        services = []
        for attr in ["ufficio_responsabile", "area"]:
            relations = catalog.findRelations(
                dict(
                    to_id=intids.getId(aq_inner(self.context)),
                    from_attribute=attr,
                )
            )

            for rel in relations:
                obj = intids.queryObject(rel.from_id)
                if (
                    obj is not None
                    and checkPermission("zope2.View", obj)  # noqa
                    and obj.portal_type == "Servizio"  # noqa
                ):
                    summary = getMultiAdapter(
                        (obj, getRequest()), ISerializeToJsonSummary
                    )()
                    services.append(summary)
        return sorted(services, key=lambda k: k["title"])

    def getChildrenUo(self):
        res = []
        children = self.context.listFolderContents(
            contentFilter={"portal_type": "UnitaOrganizzativa"}
        )
        if not children:
            return []

        for child in children:
            data = getMultiAdapter((child, self.request), ISerializeToJsonSummary)()
            data.update(self.getAdditionalInfos(context=child))
            res.append(json_compatible(data))
        return res

    def getParentUo(self):
        parent = self.context.aq_parent
        if parent.portal_type != "UnitaOrganizzativa":
            return None

        data = getMultiAdapter((parent, self.request), ISerializeToJsonSummary)()
        data.update(self.getAdditionalInfos(context=parent))
        return json_compatible(data)

    def getAdditionalInfos(self, context):
        return {
            "city": getattr(context, "city", ""),
            "zip_code": getattr(context, "zip_code", ""),
            "street": getattr(context, "street", ""),
            "contact_info": getattr(context, "contact_info", ""),
        }

    def getUOServiziDoveRivolgersi(self, UID):
        """Returns list of servizio having reference to
        current object in servizio.dove_rivolgersi field
        """
        catalog = api.portal.get_tool("portal_catalog")
        query = {
            "service_venue": UID,
            "portal_type": ["Servizio"],
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        return [
            getMultiAdapter((i, self.request), ISerializeToJsonSummary)()
            for i in catalog(**query)
        ]

    def __call__(self, version=None, include_items=True):
        self.index = "news_uo"
        result = super(UOSerializer, self).__call__(
            version=version, include_items=include_items
        )
        result["servizi_offerti"] = json_compatible(self.get_services())
        result["uo_parent"] = json_compatible(self.getParentUo())
        result["uo_children"] = json_compatible(self.getChildrenUo())
        result["prestazioni"] = json_compatible(
            self.getUOServiziDoveRivolgersi(result.get("UID", ""))
        )

        return result


@implementer(ISerializeToJsonSummary)
@adapter(IUnitaOrganizzativa, Interface)
class UOJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, force_all_metadata=False):
        data = super().__call__(force_all_metadata=force_all_metadata)
        fields = [
            "address",
            "city",
            "zip_code",
            # "email",
            # "telefono",
            "nome_sede",
            "title",
            "quartiere",
            "circoscrizione",
            "street",
            "contact_info",
        ]

        for field in fields:
            if field == "contact_info":
                data[field] = json_compatible(getattr(self.context, field, ""))
            else:
                data[field] = getattr(self.context, field, "")

        data["geolocation"] = self.getGeolocation()

        return data

    def getGeolocation(self):
        longitude = 0
        latitude = 0

        if getattr(self.context, "geolocation", None):
            longitude = getattr(self.context.geolocation, "longitude", 0)
            latitude = getattr(self.context.geolocation, "latitude", 0)

        return {"longitude": longitude, "latitude": latitude}
