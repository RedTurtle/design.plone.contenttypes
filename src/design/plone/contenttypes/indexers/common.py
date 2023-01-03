# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer


@indexer(IDexterityContent)
def tassonomia_argomenti(context, **kw):
    return [
        x.to_object.Title()
        for x in getattr(context.aq_base, "tassonomia_argomenti", [])
        if x.to_object
    ]


@indexer(IDexterityContent)
def tassonomia_argomenti_uid(context, **kw):
    return [
        x.to_object.UID()
        for x in getattr(context.aq_base, "tassonomia_argomenti", [])
        if x.to_object
    ]


@indexer(IDexterityContent)
def ufficio_responsabile(context, **kw):
    uffici = getattr(context.aq_base, "ufficio_responsabile", [])
    return [ufficio.UID() for ufficio in filter(bool, [x.to_object for x in uffici])]


@indexer(IDexterityContent)
def parent(context):
    obj_parent = context.aq_parent
    return {
        "title": obj_parent.Title(),
        "UID": obj_parent.UID(),
        "@id": obj_parent.absolute_url(),
    }
