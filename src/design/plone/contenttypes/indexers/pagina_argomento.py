# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes.interfaces.pagina_argomento import IPaginaArgomento
from zope.component import adapter
from zope.interface import implementer
from plone.restapi.indexers import SearchableText_blocks


@adapter(IPaginaArgomento)
@implementer(dexteritytextindexer.IDynamicTextIndexExtender)
class SearchableTextExtender(object):
    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Extend the searchable text with blocks"""
        return SearchableText_blocks(self.context)()
