# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from design.plone.contenttypes.interfaces.persona import IPersona


@indexer(IPersona)
def ruolo(obj):
    """ """
    return getattr(obj.aq_base, "ruolo", "")
