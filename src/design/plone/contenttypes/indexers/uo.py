# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa


@indexer(IUnitaOrganizzativa)
def uo_location(context, **kw):
    luoghi = []
    for field in ["sede", "sedi_secondarie"]:
        for ref in getattr(context, field, []):
            sede = ref.to_object
            if sede:
                luoghi.append(sede.UID())
    return luoghi
