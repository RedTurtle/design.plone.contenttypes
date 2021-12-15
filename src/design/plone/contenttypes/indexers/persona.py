# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.indexer.decorator import indexer


@indexer(IPersona)
def ruolo(context, **kw):
    return getattr(context.aq_base, "ruolo", "")


@indexer(IPersona)
def data_conclusione_incarico(context, **kw):
    return getattr(context.aq_base, "data_conclusione_incarico", "")
