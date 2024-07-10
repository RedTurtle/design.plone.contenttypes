# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.pagina_argomento import IPaginaArgomento
from plone.app.dexterity.textindexer.interfaces import IDynamicTextIndexExtender
from zope.component import adapter
from zope.interface import implementer


HAVE_REST_API_PRE_961 = False

try:
    # plone 6.0.11 with last plone.restapi>9.6.0
    from plone.app.contenttypes.indexers import SearchableText
    from plone.restapi.indexers import get_blocks_text
    from plone.restapi.indexers import text_strip

except ImportError:
    # plone 6.0.10.1 with plone.restapi<9.6.1
    HAVE_REST_API_PRE_961 = True
    from plone.restapi.indexers import SearchableText_blocks


@adapter(IPaginaArgomento)
@implementer(IDynamicTextIndexExtender)
class SearchableTextExtender(object):
    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Extend the searchable text with blocks"""
        if HAVE_REST_API_PRE_961:
            return SearchableText_blocks(self.context)()
        else:
            blocks_text = get_blocks_text(self.context)
            std_text = SearchableText(self.context)
            blocks_text.append(std_text)
            return text_strip(blocks_text)
