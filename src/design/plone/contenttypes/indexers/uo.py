# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)
from zope.security import checkPermission


@indexer(IUnitaOrganizzativa)
def office_venue(context, **kw):
    luoghi = []
    if getattr(context, "sede", None):
        sede = context.sede.to_object
        if sede and checkPermission("zope2.View", sede):
            luoghi.append(sede.UID())
    for ref in getattr(context, "sedi_secondarie", []):
        sede = ref.to_object
        if sede and checkPermission("zope2.View", sede):
            luoghi.append(sede.UID())
    return luoghi
