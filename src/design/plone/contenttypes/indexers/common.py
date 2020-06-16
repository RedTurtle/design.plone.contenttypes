# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityItem


@indexer(IDexterityContainer)
@indexer(IDexterityItem)
def tassonomia_argomenti(context, **kw):
    return [
        x.to_object.UID()
        for x in getattr(context.aq_base, "tassonomia_argomenti", [])
        if x.to_object
    ]
