# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from collective.volto.blocksfield.field import BlocksField
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

    # moved to behavior under field name descrizione_estesa?
    descrizione_completa = BlocksField(
        title=_(u"descrizione_completa", default=u"Descrizione completa"),
        description=_(
            u"help_descrizione_completa",
            default=u"Indicare una descrizione completa, inserendo tutte le"
            " informazioni rilevanti relative al luogo",
        ),
        required=False,
    )

    nome_alternativo = schema.TextLine(
        title=_(u"nome_alternativo", default=u"Nome alternativo"),
        description=_(
            u"help_nome_alternativo",
            default=u"Indicare, se esiste, un nome alternativo per il luogo;"
            " questo sarà mostrato affianco al titolo della"
            " scheda",
        ),
        required=False,
    )

    elementi_di_interesse = BlocksField(
        title=_(u"elementi_di_interesse", default=u"Elementi di interesse"),
        description=_(
            u"help_elementi_di_interesse",
            default=u"Indicare eventuali elementi di interesse per il "
            "cittadino.",
        ),
        required=False,
    )

    modalita_accesso = BlocksField(
        title=_(u"modalita_accesso", default=u"Modalita' di accesso"),
        description=_(
            u"help_modalita_accesso",
            default=u"Indicare tutte le informazioni relative alla modalità di"
            " accesso al luogo",
        ),
        required=False,
    )

    struttura_responsabile_correlati = RelationList(
        title=_(
            "struttura_responsabile_correlati",
            default=u"Struttura responsabile del luogo.",
        ),
        description=_(
            "struttura_responsabile_correlati_help",
            default="Indicare la struttura responsabile del luogo qualora sia"
            " fra unità organizzative del comune inserite nel sito; altrimenti"
            " compilare i campi testuali relativi alla struttura responsabile",
        ),
        value_type=RelationChoice(
            title=_(u"Struttura responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )

    struttura_responsabile = BlocksField(
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
            default=u"Telefono della struttura responsabile",
        ),
        description=_(
            "help_riferimento_telefonico_struttura",
            default="Indicare il riferimento telefonico per poter contattare"
            " i referenti della struttura responsabile.",
        ),
        required=False,
    )
    riferimento_fax_struttura = schema.TextLine(
        title=_(
            u"riferimento_fax_struttura",
            default=u"Fax della struttura responsabile",
        ),
        description=_(
            "help_riferimento_fax_struttura",
            default="Indicare un numero di fax della struttura responsabile.",
        ),
        required=False,
    )
    riferimento_mail_struttura = schema.TextLine(
        title=_(
            u"riferimento_mail_struttura",
            default=u"E-mail struttura responsabile",
        ),
        description=_(
            "help_riferimento_mail_struttura",
            default="Indicare un indirizzo mail per poter contattare"
            " i referenti della struttura responsabile.",
        ),
        required=False,
    )

    riferimento_pec_struttura = schema.TextLine(
        title=_(
            u"riferimento_pec_struttura",
            default=u"Pec della struttura responsabile",
        ),
        description=_(
            "help_riferimento_pec_struttura",
            default="Indicare un indirizzo pec per poter contattare"
            " i referenti della struttura responsabile.",
        ),
        required=False,
    )

    # Decisono con Baio di toglierlo: visto il vocabolario, che in realtà sta
    # qui: https://github.com/italia/daf-ontologie-vocabolari-controllati/tree/master/VocabolariControllati/classifications-for-culture/subject-disciplines
    # riteniamo che possa non fregare nulla a nessuno di questa categorizzazione.
    #  # TODO: aggiungere il vocabolario da https://dataportal.daf.teamdigitale.it/#/vocabularies/subject-disciplines  # noqa
    # # quando ritornano i dati dopo la migrazione, bisognera' vedere dove sono
    # # finiti, link invalido al momento
    # categoria_prevalente = schema.Choice(
    #     title=_(u"categoria_prevalente", default=u"Categoria prevalente"),
    #     required=False,
    #     vocabulary="design.plone.contenttypes.Mockup",
    #     missing_value=None,
    #     default=None,
    # )

    # TODO: importare il db del MIBAC, codice DBUnico / ISIL.
    # Non compare nel frontend
    # identificativo_mibac = schema.TextLine(
    #     title=_(u"identificativo_mibac", default=u"Identificativo"),
    #     required=False,
    # )

    # custom fieldsets and order
    form.order_after(nome_alternativo="IBasic.title")

    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default=u"Descrizione"),
        fields=["descrizione_completa", "elementi_di_interesse"],
    )
    model.fieldset(
        "accesso",
        label=_("accesso_label", default=u"Modalità di accesso"),
        fields=["modalita_accesso"],
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=[
            "struttura_responsabile_correlati",
            "struttura_responsabile",
            "riferimento_telefonico_struttura",
            "riferimento_fax_struttura",
            "riferimento_mail_struttura",
            "riferimento_pec_struttura",
        ],
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

    # searchabletext indexer
    dexteritytextindexer.searchable("descrizione_completa")


@implementer(ILuogo)
@adapter(IDexterityContent)
class Luogo(object):
    """
    """

    def __init__(self, context):
        self.context = context
