# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class ILuogo(model.Schema):
    """
    """

    quartiere = schema.TextLine(
        title=_(u"quartiere", default=u"Quartiere"), required=False
    )

    circoscrizione = schema.TextLine(
        title=_(u"circoscrizione", default=u"Circoscrizione"), required=False
    )

    descrizione_breve = RichText(
        title=_(u"descrizione_breve", default=u"Descrizione breve"), required=True
    )

    nome_alternativo = schema.TextLine(
        title=_(u"nome_alternativo", default=u"Nome alternativo"), required=False
    )

    elementi_di_interesse = RichText(
        title=_(u"elementi_di_interesse", default=u"Elementi di interesse"),
        required=False,
    )

    modalita_accesso = RichText(
        title=_(u"modalita_accesso", default=u"Modalita' di accesso"), required=True
    )

    riferimento_telefonico_luogo = schema.TextLine(
        title=_(
            u"riferimento_telefonico_luogo", default=u"Riferimento telefonico luogo"
        ),
        required=False,
    )

    riferimento_mail_luogo = schema.TextLine(
        title=_(u"riferimento_mail_luogo", default=u"Riferimento mail luogo"),
        required=False,
    )

    orario_pubblico = RichText(
        title=_(u"orario_pubblico", default=u"Orario per il pubblico"), required=False
    )

    struttura_responsabile = RichText(
        title=_(u"struttura_responsabile", default=u"Struttura responsabile"),
        required=False,
        description=_(
            "struttura_responsabile_help",
            default="Nome/link al sito web della struttura che gestisce il"
            " luogo, se questa non è comunale.",
        ),
    )

    riferimento_telefonico_struttura = schema.TextLine(
        title=_(
            u"riferimento_telefonico_struttura",
            default=u"Riferimento telefonico struttura responsabile",
        ),
        required=False,
    )

    riferimento_mail_struttura = schema.TextLine(
        title=_(
            u"riferimento_mail_struttura",
            default=u"Riferimento mail struttura responsabile",
        ),
        required=False,
    )

    riferimento_web = schema.TextLine(
        title=_(u"riferimento_web", default=u"Riferimento sito web"), required=False
    )

    # TODO: aggiungere il vocabolario da https://dataportal.daf.teamdigitale.it/#/vocabularies/subject-disciplines  # noqa
    # quando ritornano i dati dopo la migrazione, bisognera' vedere dove sono
    # finiti, link invalido al momento
    categoria_prevalente = schema.Choice(
        title=_(u"categoria_prevalente", default=u"Categoria prevalente"),
        required=False,
        vocabulary="design.plone.contenttypes.Mockup",
        missing_value=None,
        default=None,
    )

    # TODO: importare il db del MIBAC, codice DBUnico / ISIL.
    # Non compare nel frontend
    identificativo_mibac = schema.TextLine(
        title=_(u"identificativo_mibac", default=u"Identificativo"), required=True
    )

    struttura_responsabile_correlati = RelationList(
        title=u"Struttura responsabile del luogo",
        description=_(
            "struttura_responsabile_help",
            default="Struttura comunale che gestisce il luogo.",
        ),
        value_type=RelationChoice(
            title=_(u"Struttura responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )

    riferimento_pec = schema.TextLine(
        title=_(u"riferimento_pec", default=u"Riferimento pec"), required=False
    )

    # custom widgets
    form.widget(
        "struttura_responsabile_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # custom fieldsets and order
    form.order_after(circoscrizione="IAddress.city")
    form.order_after(quartiere="IAddress.city")

    model.fieldset(
        "correlati",
        label=_("correlati_label", default=u"Correlati"),
        fields=["struttura_responsabile_correlati"],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=[
            "riferimento_telefonico_luogo",
            "riferimento_mail_luogo",
            "struttura_responsabile",
            "riferimento_telefonico_struttura",
            "riferimento_mail_struttura",
            "riferimento_pec",
            "riferimento_web",
        ],
    )

    # searchabletext indexer
    dexteritytextindexer.searchable("quartiere")
    dexteritytextindexer.searchable("circoscrizione")
    dexteritytextindexer.searchable("descrizione_breve")
    dexteritytextindexer.searchable("orario_pubblico")
    dexteritytextindexer.searchable("identificativo_mibac")


@implementer(ILuogo)
@adapter(IDexterityContent)
class Luogo(object):
    """
    """

    def __init__(self, context):
        self.context = context
