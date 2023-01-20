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
class IEvento(model.Schema):
    """Marker inteerface for content type Evento"""

    sottotitolo = schema.TextLine(
        title=_("sottotitolo_label", default="Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    descrizione_destinatari = BlocksField(
        title=_("descrizione_destinatari", default="Descrizione destinatari"),
        required=False,
        description=_(
            "descrizione_destinatari_help",
            default="Descrizione dei principali interlocutori dell'evento.",
        ),
    )

    persone_amministrazione = RelationList(
        title="Persone dell'amministrazione che partecipano all'evento",
        default=[],
        value_type=RelationChoice(
            title=_("Persona dell'amministrazione"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_amministrazione_help",
            default="Elenco delle persone dell'amministrazione che"
            " parteciperanno all'evento.",
        ),
        required=False,
    )

    orari = BlocksField(
        title=_("orari", default="Informazioni sugli orari"),
        required=False,
        description=_(
            "orari_help",
            default="Informazioni sugli orari di svolgimento dell'evento.",
        ),
    )

    prezzo = BlocksField(
        title=_("prezzo", default="Costo"),
        required=False,
        description=_(
            "prezzo_help",
            default="Eventuale costo dell'evento (se ci sono uno o più biglietti), "
            "con link all'alcquisto se disponibile",
        ),
    )

    # campi presenti nelle vecchie grafiche che abbiamo deciso di continuare a mostrare
    organizzato_da_interno = RelationList(
        title=_("organizzato_da_interno_label", default="Organizzato da"),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        description=_(
            "organizzato_da_interno_help",
            default="Se l'evento è organizzato direttamente dal comune,"
            " indicare l'ufficio/ente organizzatore. I dati di contatto "
            "verranno presi direttamente dall'ufficio selezionato. Se l'evento"
            " non è organizzato direttamente dal comune, o si vogliono "
            "sovrascrivere alcuni dati di contatto, utilizzare i seguenti campi.",  # noqa
        ),
    )
    organizzato_da_esterno = BlocksField(
        title=_("organizzato_da_esterno_label", default="Organizzatore"),
        required=False,
        description=_(
            "organizzato_da_esterno_help",
            default="Se l'evento non è organizzato direttamente dal comune oppure ha anche un organizzatore esterno,"  # noqa
            " indicare il nome del contatto.",
        ),
    )
    supportato_da = RelationList(
        title=_("supportato_da_label", default="Evento supportato da"),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        description=_(
            "supportato_da_help",
            default="Indicare gli uffici/enti che supportano l'evento.",
        ),
    )

    # campi aggiunti con il pnrr
    patrocinato_da = schema.TextLine(
        title=_("patrocinato_da_label", default="Patrocinato da"),
        required=False,
        description=_(
            "patrocinato_da_help",
            default="Indicare l'ente che supporta l'evento, se presente.",
        ),
    )

    parteciperanno = RelationList(
        title=_("parteciperanno_label", default="Parteciperanno (Persone)"),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        description=_(
            "parteciperanno_help",
            default="Link a persone dell'amministrazione che interverranno all'evento",
        ),
    )

    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "a_chi_si_rivolge_help",
            default="Descrizione testuale dei principali destinatari dell'Evento",
        ),
    )

    # custom widgets
    form.widget(
        "parteciperanno",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
        },
    )
    form.widget(
        "supportato_da",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "organizzato_da_interno",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona", "UnitaOrganizzativa", "Servizio"],
        },
    )
    form.widget(
        "persone_amministrazione",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
        },
    )

    # custom fieldsets and order
    form.order_before(sottotitolo="ILeadImageBehavior.image")

    model.fieldset(
        "cose",
        label=_("cose_label", default="Cos'è"),
        fields=[
            "descrizione_estesa",
            "descrizione_destinatari",
            "persone_amministrazione",
        ],
    )
    model.fieldset(
        "date_e_orari",
        label=_("date_e_orari_label", default="Date e orari"),
        fields=["orari"],
    )
    model.fieldset("costi", label=_("costi_label", default="Costi"), fields=["prezzo"])
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "organizzato_da_interno",
            "organizzato_da_esterno",
            "supportato_da",
            "patrocinato_da",
        ],
    )

    textindexer.searchable("descrizione_estesa")


@implementer(IEvento)
@adapter(IDexterityContent)
class Evento(object):
    """ """

    def __init__(self, context):
        self.context = context
