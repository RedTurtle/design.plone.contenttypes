# -*- coding: utf-8 -*-
from .related_news_serializer import (
    SerializeFolderToJson as RelatedNewsSerializer,
)
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer,
)
from plone.restapi.interfaces import ISerializeToJson, ISerializeToJsonSummary
from zope.component import adapter, getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from zope.globalrequest import getRequest


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
            res.append(data)
        return res

    def getParentUo(self):
        parent = self.context.aq_parent
        if parent.portal_type != "UnitaOrganizzativa":
            return None

        data = getMultiAdapter((parent, self.request), ISerializeToJsonSummary)()
        data.update(self.getAdditionalInfos(context=parent))
        return data

    def getAdditionalInfos(self, context):
        return {
            "city": getattr(context, "city", ""),
            "zip_code": getattr(context, "zip_code", ""),
            "street": getattr(context, "street", ""),
            "contact_info": getattr(context, "contact_info", ""),
        }

    def __call__(self, version=None, include_items=True):
        self.index = "news_uo"
        result = super(UOSerializer, self).__call__(
            version=version, include_items=include_items
        )
        result["servizi_offerti"] = self.get_services()
        result["uo_parent"] = self.getParentUo()
        result["uo_children"] = self.getChildrenUo()
        return result


@implementer(ISerializeToJsonSummary)
@adapter(IUnitaOrganizzativa, Interface)
class UOJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, force_all_metadata=False):
        data = super().__call__(force_all_metadata=force_all_metadata)
        for field in ["address", "city", "zip_code", "email", "telefono"]:
            data[field] = getattr(self.context, field, "")
        return data
