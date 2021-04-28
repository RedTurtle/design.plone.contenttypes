# -*- coding: utf-8 -*-
# from collective import dexteritytextindexer
from design.plone.contenttypes.interfaces.bando import IBandoAgidSchema
from plone.indexer.decorator import indexer
# from plone.restapi.indexers import SearchableText_blocks
# from zope.component import adapter
# from zope.interface import implementer


@indexer(IBandoAgidSchema)
def office_manager(context, **kw):
    """
    """
    ufficio_responsabile = [x.to_object for x in context.ufficio_responsabile]
    ufficio_responsabile = filter(bool, ufficio_responsabile)
    ufficio_responsabile_title = [x.UID() for x in ufficio_responsabile]
    return ufficio_responsabile_title

# @adapter(IBandoAgidSchema)
# @implementer(dexteritytextindexer.IDynamicTextIndexExtender)
# class SearchableTextExtender(object):
#     def __init__(self, context):
#         self.context = context

#     def __call__(self):
#         """Extend the searchable text with blocks"""
#         return SearchableText_blocks(self.context)()
