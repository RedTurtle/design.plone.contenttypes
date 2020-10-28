# -*- coding: utf-8 -*-
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
class IEvento(model.Schema):
    """Marker inteerface for content type Evento
    """

    sottotitolo = schema.TextLine(
        title=_(u"sottotitolo_label", default=u"Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )

    descrizione_destinatari = RichText(
        title=_(
            u"descrizione_destinatari", default=u"Descrizione destinatari"
        ),
        required=False,
        description=_(
            "descrizione_destinatari_help",
            default="Descrizione dei principali interlocutori dell'evento.",
        ),
    )

    persone_amministrazione = RelationList(
        title=u"Persone dell'amministrazione che partecipano all'evento",
        default=[],
        value_type=RelationChoice(
            title=_(u"Persona dell'amministrazione"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_amministrazione_help",
            default="Elenco delle persone dell'amministrazione che"
            " parteciperanno all'evento.",
        ),
        required=False,
    )

    orari = RichText(
        title=_(u"orari", default=u"Informazioni sugli orari"),
        required=False,
        description=_(
            "orari_help",
            default="Informazioni sugli orari di svolgimento dell'evento.",
        ),
    )

    prezzo = RichText(
        title=_(u"prezzo", default=u"Prezzo"),
        required=False,
        description=_(
            "prezzo_help",
            default="Indicare il prezzo dell'evento, se presente, specificando"
            " se esistono formati diversi.",
        ),
    )
    organizzato_da_interno = RelationList(
        title=_(u"organizzato_da_interno_label", default=u"Organizzato da"),
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

    organizzato_da_esterno = RichText(
        title=_(u"organizzato_da_esterno_label", default=u"Organizzatore"),
        required=False,
        description=_(
            "organizzato_da_esterno_help",
            default="Se l'evento non è organizzato direttamente dal comune oppure ha anche un organizzatore esterno,"
            " indicare il nome del contatto.",
        ),
    )
    telefono = schema.TextLine(
        title=_(u"telefono_event_help", default=u"Telefono"),
        description=_(
            u"telefono_event_label",
            default=u"Indicare un riferimento telefonico per poter contattare"
            " gli organizzatori.",
        ),
        required=False,
    )
    fax = schema.TextLine(
        title=_(u"fax_event_help", default=u"Fax"),
        description=_(
            u"fax_event_label", default="Indicare un numero di fax."
        ),
        required=False,
    )
    reperibilita = schema.TextLine(
        title=_(u"reperibilita", default=u"Reperibilità organizzatore"),
        required=False,
        description=_(
            "reperibilita_help",
            default="Indicare gli orari in cui l'organizzatore è"
            " telefonicamente reperibile.",
        ),
    )
    email = schema.TextLine(
        title=_(u"email_event_label", default=u"E-mail"),
        description=_(
            u"email_event_help",
            default=u"Indicare un indirizzo mail per poter contattare"
            " gli organizzatori.",
        ),
        required=False,
    )

    web = schema.TextLine(
        title=_(u"web_event_label", default=u"Sito web"),
        description=_(
            "web_event_help",
            default="Indicare un indirizzo web di riferimento a "
            "questo evento.",
        ),
        required=False,
    )
    supportato_da = RelationList(
        title=_(u"supportato_da_label", default=u"Evento supportato da"),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        description=_(
            "supportato_da_help",
            default="Indicare gli uffici/enti che supportano l'evento.",
        ),
    )

    # TODO: come fare il rating/recensione dell'evento

    patrocinato_da = schema.TextLine(
        title=_(u"patrocinato_da_label", default=u"Patrocinato da"),
        required=False,
        description=_(
            "patrocinato_da_help",
            default="Indicare l'ente che supporta l'evento, se presente.",
        ),
    )

    # custom widgets
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
        label=_("cose_label", default=u"Cos'è"),
        fields=["descrizione_destinatari", "persone_amministrazione"],
    )
    model.fieldset(
        "date_e_orari",
        label=_("date_e_orari_label", default=u"Date e orari"),
        fields=["orari"],
    )
    model.fieldset(
        "costi", label=_("costi_label", default=u"Costi"), fields=["prezzo"]
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=[
            "organizzato_da_interno",
            "organizzato_da_esterno",
            "telefono",
            "fax",
            "reperibilita",
            "email",
            "web",
            "supportato_da",
        ],
    )
    model.fieldset(
        "informazioni",
        label=_("informazioni_label", default=u"Ulteriori informazioni"),
        fields=["patrocinato_da"],
    )


@implementer(IEvento)
@adapter(IDexterityContent)
class Evento(object):
    """
    """

    def __init__(self, context):
        self.context = context
