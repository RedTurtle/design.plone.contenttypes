# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class ILuogo(model.Schema):
    """ """

    # moved to behavior under field name descrizione_estesa?
    descrizione_completa = BlocksField(
        title=_("descrizione_completa", default="Descrizione completa"),
        description=_(
            "help_descrizione_completa",
            default="Indicare una descrizione completa, inserendo tutte le"
            " informazioni rilevanti relative al luogo",
        ),
        required=False,
    )

    nome_alternativo = schema.TextLine(
        title=_("nome_alternativo", default="Nome alternativo"),
        description=_(
            "help_nome_alternativo",
            default="Indicare, se esiste, un nome alternativo per il luogo;"
            " questo sarà mostrato affianco al titolo della"
            " scheda",
        ),
        required=False,
    )

    elementi_di_interesse = BlocksField(
        title=_("elementi_di_interesse", default="Elementi di interesse"),
        description=_(
            "help_elementi_di_interesse",
            default="Indicare eventuali elementi di interesse per il " "cittadino.",
        ),
        required=False,
    )

    modalita_accesso = BlocksField(
        title=_("modalita_accesso", default="Modalita' di accesso"),
        description=_(
            "help_modalita_accesso",
            default="Indicare tutte le informazioni relative alla modalità di"
            " accesso al luogo",
        ),
        required=True,
    )

    struttura_responsabile_correlati = RelationList(
        title=_(
            "struttura_responsabile_correlati",
            default="Struttura responsabile del luogo.",
        ),
        description=_(
            "struttura_responsabile_correlati_help",
            default="Indicare la struttura responsabile del luogo qualora sia"
            " fra unità organizzative del comune inserite nel sito; altrimenti"
            " compilare i campi testuali relativi alla struttura responsabile",
        ),
        value_type=RelationChoice(
            title=_("Struttura responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )

    struttura_responsabile = BlocksField(
        title=_("struttura_responsabile", default="Struttura responsabile"),
        required=False,
        description=_(
            "struttura_responsabile_help",
            default="Nome/link al sito web della struttura che gestisce il"
            " luogo, se questa non è comunale.",
        ),
    )

    orario_pubblico = BlocksField(
        title=_("orario_pubblico", default="Orario per il pubblico"),
        required=False,
        description=_(
            "orario_pubblico_help",
            default="Orario di apertura al pubblico del luogo ed eventuali "
            "regole di accesso (es prenotazione).",
        ),
    )

    # Decisono con Baio di toglierlo: visto il vocabolario, che in realtà sta
    # qui: https://github.com/italia/daf-ontologie-vocabolari-controllati/tree/master/VocabolariControllati/classifications-for-culture/subject-disciplines # noqa
    # riteniamo che possa non fregare nulla a nessuno di questa categorizzazione.
    #  # TODO: aggiungere il vocabolario da https://dataportal.daf.teamdigitale.it/#/vocabularies/subject-disciplines  # noqa
    # # quando ritornano i dati dopo la migrazione, bisognera' vedere dove sono
    # # finiti, link invalido al momento
    # categoria_prevalente = schema.Choice(
    #     title=_("categoria_prevalente", default="Categoria prevalente"),
    #     required=False,
    #     vocabulary="design.plone.contenttypes.Mockup",
    #     missing_value=None,
    #     default=None,
    # )

    # TODO: importare il db del MIBAC, codice DBUnico / ISIL.
    # Non compare nel frontend
    identificativo_mibac = schema.TextLine(
        title=_("identificativo_mibac", default="Identificativo"),
        required=False,
        description=_(
            "identificativo_mibac_help",
            default="Codice identificativo del luogo. Nel MIBAC c'è"
            " il codice del DBUnico per i luoghi della cultura e il codice"
            " ISIL per le biblioteche. Non deve comparire nel"
            " frontend del sito.",
        ),
    )

    # custom fieldsets and order
    form.order_after(nome_alternativo="IBasic.title")

    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default="Descrizione"),
        fields=["descrizione_completa", "elementi_di_interesse"],
    )
    model.fieldset(
        "accesso",
        label=_("accesso_label", default="Modalità di accesso"),
        fields=["modalita_accesso"],
    )

    model.fieldset(
        "categorization",
        fields=["identificativo_mibac"],
    )

    model.fieldset(
        "orari",
        label=_("orari_label", default="Orari di apertura"),
        fields=["orario_pubblico"],
    )
    # TODO: migration script for these commented fields towards PDC
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "struttura_responsabile_correlati",
            "struttura_responsabile",
            # "riferimento_telefonico_struttura",
            # "riferimento_fax_struttura",
            # "riferimento_mail_struttura",
            # "riferimento_pec_struttura",
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
    textindexer.searchable("descrizione_completa")


@implementer(ILuogo)
@adapter(IDexterityContent)
class Luogo(object):
    """ """

    def __init__(self, context):
        self.context = context
