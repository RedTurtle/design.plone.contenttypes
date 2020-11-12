# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityItem


@indexer(IDexterityContainer)
@indexer(IDexterityItem)
def tassonomia_argomenti(context, **kw):
    return [
        x.to_object.Title()
        for x in getattr(context.aq_base, "tassonomia_argomenti", [])
        if x.to_object
    ]


@indexer(IDexterityContainer)
@indexer(IDexterityItem)
def ufficio_responsabile(context, **kw):
    uffici = getattr(context.aq_base, "ufficio_responsabile", [])
    return [
        ufficio.UID()
        for ufficio in filter(bool, [x.to_object for x in uffici])
    ]
