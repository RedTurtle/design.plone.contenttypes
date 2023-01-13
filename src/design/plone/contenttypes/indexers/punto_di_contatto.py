# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.punto_di_contatto import IPuntoDiContatto
from plone.app.dexterity.textindexer.interfaces import IDynamicTextIndexExtender
from zope.interface import implementer
from zope.component import adapter


@implementer(IDynamicTextIndexExtender)
@adapter(IPuntoDiContatto)
class PuntoDiContattoMoreTextToIndex(object):
    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Extend the searchable text with a custom string"""
        result = []
        field_value = getattr(self.context, "value_punto_contatto", [])
        for value in field_value:
            result.append(value.get("pdc_value", ""))
        return " ".join(result)
