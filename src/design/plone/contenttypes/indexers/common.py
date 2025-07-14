# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.i18n.normalizer.base import mapUnicode
from plone.indexer.decorator import indexer
from Products.CMFPlone.CatalogTool import num_sort_regex
from Products.CMFPlone.CatalogTool import zero_fill
from Products.CMFPlone.utils import safe_callable
from Products.CMFPlone.utils import safe_unicode

import six


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


@indexer(IDexterityContent)
def exclude_from_search(context):
    return getattr(context.aq_base, "exclude_from_search", False)


@indexer(IDexterityContent)
def sortable_title(obj):
    """
    Vogliamo introdurre una modifica di plone 6:

    https://github.com/plone/Products.CMFPlone/commit/470fea41e8de344d4b6ab4474609867f5a2fa0b0

    Prima sortable_title veniva troncato a 40 caratteri e generava ordinamenti sballati
    """
    title = getattr(obj, "Title", None)
    if title is not None:
        if safe_callable(title):
            title = title()

        if isinstance(title, six.string_types):
            # Ignore case, normalize accents, strip spaces
            sortabletitle = mapUnicode(safe_unicode(title)).lower().strip()
            # Replace numbers with zero filled numbers
            sortabletitle = num_sort_regex.sub(zero_fill, sortabletitle)
            if six.PY2:
                return sortabletitle.encode("utf-8")
            return sortabletitle
    return ""
