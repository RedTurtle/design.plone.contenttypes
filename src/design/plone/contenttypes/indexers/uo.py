# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)


@indexer(IUnitaOrganizzativa)
def office_venue(context, **kw):
    luoghi = context.luoghi_correlati
    return [
        luogo.UID() for luogo in filter(bool, [x.to_object for x in luoghi])
    ]
