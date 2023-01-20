# -*- coding: utf-8 -*-
from Acquisition import aq_base
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.indexer.decorator import indexer


@indexer(IPersona)
def image_field_indexer(obj):
    """"""
    base_obj = aq_base(obj)

    image_field = ""
    if getattr(base_obj, "foto_persona", False):
        image_field = "foto_persona"
    return image_field


@indexer(IPersona)
def ruolo(obj):
    """
    We read this information from incarico related object
    """
    incarichi = obj.incarichi_persona
    if incarichi:
        # in teoria dovremmo averne uno, ma è consentito averne più di uno.
        # usiamo un keyowrd index per cui in realtà per indicizzare ci interessa
        # poco
        return [x.to_object.title for x in obj.incarichi_persona if not x.isBroken()]
    return []
