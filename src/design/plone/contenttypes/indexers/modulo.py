# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.modulo import IModulo
from plone.indexer.decorator import indexer


@indexer(IModulo)
def mime_type(context, **kw):
    value = getattr(context, "file_principale", None)
    return getattr(value, "contentType", None)
