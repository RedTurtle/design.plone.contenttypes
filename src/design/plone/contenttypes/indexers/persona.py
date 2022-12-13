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
