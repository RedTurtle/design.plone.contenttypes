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
                label=_("correlati_label", default="Contenuti collegati"),
                fields=["relatedItems"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]
        if self.schema.getName() == "IEventBasic":
            fieldset = Fieldset(
                "date_evento",
                label=_("date_evento_label", default=u"Date dell'evento"),
                fields=["start", "end", "whole_day", "open_end", "sync_uid"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]
        if self.schema.getName() == "IEventRecurrence":
            fieldset = Fieldset(
                "date_evento",
                label=_("date_evento_label", default=u"Date dell'evento"),
                fields=["recurrence"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]
        if self.schema.getName() == "IAddress":
            fieldset = Fieldset(
                "dove",
                label=_("dove_label", default=u"Dove"),
                fields=["street", "zip_code", "city", "country"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]
        if self.schema.getName() == "IGeolocatable":

            fieldset = Fieldset(
                "dove",
                label=_("dove_label", default=u"Dove"),
                fields=["geolocation"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset]
