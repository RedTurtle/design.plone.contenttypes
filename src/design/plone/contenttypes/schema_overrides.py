# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
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
            fieldset = Fieldset(
                "correlati",
                label=_("correlati_label", default=u"Correlati"),
                fields=["relatedItems"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]

        # fieldsets = []
        # if self.schema.getName() == "IRelatedItems":
        #     fieldset_correlati = Fieldset(
        #         "correlati",
        #         label=_("correlati_label", default=u"Correlati"),
        #         fields=["relatedItems"],
        #     )
        #     fieldsets.append(fieldset_correlati)
        # if self.schema.getName() in ("IEventBasic", "IEventRecurrence"):
        #     fieldset_evento_date = Fieldset(
        #         "date_evento",
        #         label=_("date_evento_label", default=u"Date dell'evento"),
        #         fields=[
        #             "start",
        #             "end",
        #             "whole_day",
        #             "open_end",
        #             "sync_uid",
        #             "recurrence",
        #         ],
        #     )
        #     fieldsets.append(fieldset_evento_date)
        # self.schema._Element__tagged_values[
        #     "plone.supermodel.fieldsets"
        # ] = fieldsets
