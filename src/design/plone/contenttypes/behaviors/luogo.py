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
        title=_(u"quartiere", default=u"Quartiere"),
        description=_(
            u"help_quartiere",
            default=u"Indicare l'eventuale"
            " quartiere in cui si trova questo luogo",
        ),
        required=False,
    )

    circoscrizione = schema.TextLine(
        title=_(u"circoscrizione", default=u"Circoscrizione"),
        description=_(
            u"help_circoscrizione",
            default=u"Indicare l'eventuale"
            " circoscrizione in cui si trova questo luogo",
        ),
        required=False,
    )

    # moved to behavior under field name descrizione_estesa?
    descrizione_completa = RichText(
        title=_(u"descrizione_completa", default=u"Descrizione completa"),
        description=_(
            u"help_descrizione_completa",
            default=u"Indicare una descrizione completa, inserendo tutte le"
            " informazioni rilevanti relative al luogo",
        ),
        required=False,
    )

    luoghi_correlati = RelationList(
        title=_("luoghi_correlati", default=u"Luoghi correlati"),
        description=_(
            "luoghi_correlati_help",
            default="Indicare una serie di eventuali luoghi di interesse per "
            "il cittadino correlati a questo.",
        ),
        value_type=RelationChoice(
            title=_(u"Struttura responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )

    nome_alternativo = schema.TextLine(
        title=_(u"nome_alternativo", default=u"Nome alternativo"),
        description=_(
            u"help_nome_alternativo",
            default=u"Indicare, se esiste, un nome alternativo per il luogo;"
            " questo sarà mostrato tra parentesi affiancato al titolo della"
            " scheda",
        ),
        required=False,
    )

    argomenti_di_interesse = RichText(
        title=_(u"argomenti_di_interesse", default=u"Argomenti di interesse"),
        description=_(
            u"help_argomenti_di_interesse",
            default=u"Indicare eventuali argomenti di interesse per il "
            "cittadino.",
        ),
        required=False,
    )

    modalita_accesso = RichText(
        title=_(u"modalita_accesso", default=u"Modalita' di accesso"),
        description=_(
            u"help_modalita_accesso",
            default=u"Indicare tutte le informazioni relative alla modalità di"
            " accesso al luogo",
        ),
        required=False,
    )

    riferimento_telefonico_luogo = schema.TextLine(
        title=_(u"riferimento_telefonico_luogo", default=u"Telefono"),
        description=_(
            u"help_riferimento_telefonico_luogo",
            default=u"Indicare un riferimento telefonico per poter contattare"
            " i referenti del luogo.",
        ),
        required=False,
    )

    riferimento_mail_luogo = schema.TextLine(
        title=_(u"riferimento_mail_luogo", default=u"E-mail"),
        description=_(
            u"help_riferimento_mail_luogo",
            default=u"Indicare un indirizzo mail per poter contattare"
            " i referenti del luogo.",
        ),
        required=False,
    )

    riferimento_pec_luogo = schema.TextLine(
        title=_(u"riferimento_pec_luogo", default=u"Pec"),
        description=_(
            u"help_riferimento_pec_luogo",
            default=u"Indicare un indirizzo pec per poter contattare"
            " i referenti del luogo.",
        ),
        required=False,
    )

    orario_pubblico = RichText(
        title=_(u"orario_pubblico", default=u"Orario per il pubblico"),
        description=_(
            u"help_orario_pubblico",
            default=u"Indicare eventuali orari di accesso al pubblico",
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
            default=u"Telefono della struttura responsabile",
        ),
        description=_(
            "help_riferimento_telefonico_struttura",
            default="Indicare il riferimento telefonico per poter contattare"
            " i referenti della struttura responsabile.",
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

    riferimento_web = schema.TextLine(
        title=_(u"riferimento_web", default=u"Indirizzo web"),
        description=_(
            "help_riferimento_web",
            default="Indicare un indirizzo web utile per ottenere i contatti"
            " del luogo.",
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
    form.order_after(circoscrizione="IAddress.city")
    form.order_after(quartiere="IAddress.city")
    form.order_after(nome_alternativo="IBasic.title")
    form.order_before(argomenti_di_interesse="ILeadImageBehavior.image")
    # form.order_after(orario_pubblico="ILeadImageBehavior.image_caption")
    # form.order_after(modalita_accesso="ILeadImageBehavior.image_caption")
    # form.order_after(argomenti_di_interesse="ILeadImageBehavior.image_caption")
    # form.order_after(descrizione_completa="ILeadImageBehavior.image_caption")

    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default=u"Descrizione"),
        fields=["descrizione_completa", "luoghi_correlati"],
    )
    model.fieldset(
        "accesso",
        label=_("accesso_label", default=u"Modalità di accesso"),
        fields=["modalita_accesso"],
    )
    model.fieldset(
        "dove",
        label=_("dove_label", default=u"Dove"),
        fields=["quartiere", "circoscrizione"],
    )
    model.fieldset(
        "orari",
        label=_("orari_label", default=u"Orari di apertura"),
        fields=["orario_pubblico"],
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=[
            "riferimento_telefonico_luogo",
            "riferimento_mail_luogo",
            "riferimento_pec_luogo",
            "struttura_responsabile_correlati",
            "struttura_responsabile",
            "riferimento_telefonico_struttura",
            "riferimento_mail_struttura",
            "riferimento_pec_struttura",
            "riferimento_web",
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
    form.widget(
        "luoghi_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    # searchabletext indexer
    dexteritytextindexer.searchable("quartiere")
    dexteritytextindexer.searchable("circoscrizione")
    dexteritytextindexer.searchable("descrizione_completa")
    dexteritytextindexer.searchable("orario_pubblico")


@implementer(ILuogo)
@adapter(IDexterityContent)
class Luogo(object):
    """
    """

    def __init__(self, context):
        self.context = context
