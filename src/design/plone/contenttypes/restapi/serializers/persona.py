# -*- coding: utf-8 -*-
from .related_news_serializer import SerializeFolderToJson
from Acquisition import aq_inner
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
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
@adapter(IPersona, Interface)
class PersonaSerializer(SerializeFolderToJson):
    index = "news_people"

    def related_contents(self, field):
        """ """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        items = []
        relations = catalog.findRelations(
            dict(
                to_id=intids.getId(aq_inner(self.context)),
                from_attribute=field,
            )
        )

        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission("zope2.View", obj):
                summary = getMultiAdapter(
                    (obj, getRequest()), ISerializeToJsonSummary
                )()
                items.append(summary)
        return sorted(items, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        result = super(PersonaSerializer, self).__call__(
            version=version, include_items=include_items
        )
        strutture_correlate = self.related_contents(field="persone_struttura")
        responsabile_di = self.related_contents(field="responsabile")
        assessore_di = self.related_contents(field="assessore_riferimento")

        result["assessore_di"] = []
        result["responsabile_di"] = []
        result["strutture_correlate"] = []
        if assessore_di:
            result["assessore_di"] = assessore_di
        if responsabile_di:
            result["responsabile_di"] = responsabile_di
        if strutture_correlate:
            result["strutture_correlate"] = strutture_correlate
        result["organizzazione_riferimento"] = None
        return result
