# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.pagina_argomento import IPaginaArgomento
from plone.app.dexterity.textindexer.interfaces import IDynamicTextIndexExtender
from plone.restapi.indexers import SearchableText_blocks
from zope.component import adapter
from zope.interface import implementer


@adapter(IPaginaArgomento)
@implementer(IDynamicTextIndexExtender)
class SearchableTextExtender(object):
    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Extend the searchable text with blocks"""
        return SearchableText_blocks(self.context)()
