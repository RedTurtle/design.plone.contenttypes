# -*- coding: utf-8 -*-
from .related_news_serializer import (
    SerializeFolderToJson as RelatedNewsSerializer,
)
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
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
        """
        """
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
                if obj is not None and checkPermission("zope2.View", obj):
                    summary = getMultiAdapter(
                        (obj, getRequest()), ISerializeToJsonSummary
                    )()
                    services.append(summary)
        return sorted(services, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        self.index = "news_uo"
        result = super(UOSerializer, self).__call__(
            version=version, include_items=include_items
        )
        result["servizi_offerti"] = self.get_services()
        return result
