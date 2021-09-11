# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.bando import IBandoAgidSchema
from plone.indexer.decorator import indexer


@indexer(IBandoAgidSchema)
def ufficio_responsabile_bando(context, **kw):
    uffici = getattr(context.aq_base, "ufficio_responsabile", [])
    return [ufficio.UID() for ufficio in filter(bool, [x.to_object for x in uffici])]


@indexer(IBandoAgidSchema)
def Subject_bando(context, **kw):

    return context.Subject
