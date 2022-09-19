# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


def onModify(argomento, event):
    """ """
    should_update_references = False
    for descr in event.descriptions:
        for fieldname in getattr(descr, "attributes", []):
            if fieldname == "IBasic.title":
                should_update_references = True
    if not should_update_references:
        return
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    for rel in catalog.findRelations(
        dict(
            to_id=intids.getId(aq_inner(argomento)),
            from_attribute="tassonomia_argomenti",
        )  # noqa
    ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission("zope2.View", obj):
            obj.reindexObject(idxs=["tassonomia_argomenti"])
