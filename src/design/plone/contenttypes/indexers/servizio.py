# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from design.plone.contenttypes.interfaces.servizio import IServizio


@indexer(IServizio)
def ufficio_responsabile(context, **kw):
    uffici = context.ufficio_responsabile
    return [
        ufficio.UID()
        for ufficio in filter(bool, [x.to_object for x in uffici])
    ]


@indexer(IServizio)
def service_venue(context, **kw):
    luoghi = context.sedi_e_luoghi
    return [
        luogo.UID() for luogo in filter(bool, [x.to_object for x in luoghi])
    ]
