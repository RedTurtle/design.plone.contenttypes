# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import interfaces
from plone.supermodel.model import Fieldset
from zope.component import adapter
from zope.interface import implementer


@implementer(interfaces.ISchemaPlugin)
@adapter(IFormFieldProvider)
class SchemaTweaks(object):
    """
    """

    order = 999999

    def __init__(self, schema):
        self.schema = schema

    def __call__(self):
        if self.schema.getName() == "IRelatedItems":
            fieldset = Fieldset("correlati", fields=["relatedItems"])
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]
        # if self.schema.getName() == "ICategorization":
        #     import pdb

        #     pdb.set_trace()
        #     # ownership
