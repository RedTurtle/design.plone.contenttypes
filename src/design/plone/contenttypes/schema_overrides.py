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
        if self.schema.getName() == "IEventBasic":
            fieldset = Fieldset(
                "date_evento",
                label=_("date_evento_label", default=u"Date dell'evento"),
                fields=["start", "end", "whole_day", "open_end", "sync_uid",],
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

        if self.schema.getName() == "IEventContact":
            fieldset_informazioni = Fieldset(
                "informazioni",
                label=_("informazioni_label", default=u"Informazioni"),
                fields=["event_url"],
            )
            self.schema._Element__tagged_values[
                "plone.supermodel.fieldsets"
            ] = [fieldset_informazioni]

        # if self.schema.getName() == "IEvento":

        # fieldset_paretecipanti = Fieldset(
        #     "partecipanti",
        #     label=_("partecipanti_label", default=u"Partecipanti"),
        #     fields=["descrizione_destinatari", "persone_amministrazione"],
        # )
        # fieldset_costi = Fieldset(
        #     "costi",
        #     label=_("costi_label", default=u"Costi"),
        #     fields=["prezzo"],
        # )
        # fieldset_contatti = Fieldset(
        #     "contatti",
        #     label=_("contatti_label", default=u"Contatti"),
        #     fields=[
        #         "organizzato_da_esterno",
        #         "organizzato_da_interno",
        #         "contatto_reperibilita",
        #         "evento_supportato_da",
        #     ],
        # )
        # fieldset_informazioni = Fieldset(
        #     "informazioni",
        #     label=_("informazioni_label", default=u"Informazioni"),
        #     fields=[
        #         "ulteriori_informazioni",
        #         "event_url",
        #         "patrocinato_da",
        #         "box_aiuto",
        #     ],
        # )
        # fieldset_correlati = Fieldset(
        #     "correlati",
        #     label=_("correlati_label", default=u"Correlati"),
        #     fields=["relatedItems", "strutture_politiche"],
        # )
        # fielset_categorization = Fieldset(
        #     "categorization",
        #     label=_("categorization_label", default=u"Categorizzazione"),
        #     fields=["tassonomia_argomenti", "subjects", "language"],
        # )
        # fieldset_date_evento = Fieldset(
        #     "date_evento",
        #     label=_("date_evento_label", default=u"Date dell'evento"),
        #     fields=["orari"],
        # )
        # self.schema._Element__tagged_values[
        #     "plone.supermodel.fieldsets"
        # ] = [
        #     fieldset_paretecipanti,
        #     fieldset_costi,
        #     fieldset_contatti,
        #     fieldset_informazioni,
        #     fieldset_correlati,
        #     fielset_categorization,
        #     fieldset_date_evento,
        # ]
        # import pdb

        # pdb.set_trace()

