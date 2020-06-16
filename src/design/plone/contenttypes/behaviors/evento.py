# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone import api
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IContextSourceBinder)
class SourceGeneratorTest(object):
    def __init__(self, portalType):
        self.portalType = portalType

    def __call__(self, context):
        _ = api.content.find(context=context, portal_type=self.portalType)
        terms = []

        for item in _:
            if item is not None:
                obj = item.getObject()
                terms.append(
                    SimpleVocabulary.createTerm(obj.id, str(obj.id), obj.title)
                )

        return SimpleVocabulary(terms)


@provider(IFormFieldProvider)
class IEvento(model.Schema):
    """Marker inteerface for content type Evento
    """

    # questo deve essere progressivo!!
    identifier = schema.TextLine(
        title=_(u"identifier", default=u"Identifier"), required=True
    )

    # TODO: come trattare il campo tipologia dell'evento

    # TODO: sottotitolo

    immagine = field.NamedImage(
        title=_(u"immagine", default=u"Immagine"), required=False
    )

    tassonomia_argomenti = schema.List(
        title=_(u"tassonomia_argomenti", default=u"Tassonomia argomenti"),
        default=[],
        value_type=schema.Choice(
            title=_(u"Argomenti"),
            vocabulary="design.plone.contenttypes.TagsVocabulary",
        ),
        required=False,
    )

    evento_genitore = schema.Bool(
        title=_(u"evento_genitore", default=u"Evento genitore"), required=True
    )

    # ci sara un calendario eventi
    # calendario_eventi_link = RichText(
    #     title=_(u'calendario_eventi_link', default=u'Vedi calendario eventi')
    #     required=False,
    # )

    # backref
    # parte_di = schema.Choice(
    #     title=_(u'parte_di', default=u'Parte di'),
    #     required=False,
    #     missing_value=(),
    #     vocabulary='design.plone.contenttypes.Mockup',
    # )

    # publucation date di Plone (effective_date)
    # data_pubblicazione = schema.Date(
    #     title=_(u'data_pubblicazione', default=u'Data di pubblicazione'),
    #     required=True,
    # )

    introduzione = RichText(
        title=_(u"introduzione", default=u"Introduzione"), required=False
    )

    # TODO: decidere come implementare i video e i media
    # video_evento = schema.TextLine()

    descrizione_destinatari = RichText(
        title=_(
            u"descrizione_destinatari", default=u"Descrizione destinatari"
        ),
        required=True,
    )

    persone_amministrazione = RelationList(
        title=u"Persone dell'amministrazione",
        default=[],
        value_type=RelationChoice(
            title=_(u"Persona dell'amminnistrazione"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "persone_amministrazione",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
        },
    )

    # ref
    luogo_event = RelationList(
        title=_(u"luogo_evento", default=u"Luogo dell'evento"),
        required=True,
        value_type=RelationChoice(
            title=_(u"Luogo dell'evento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "luogo_event",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Luogo"],
        },
    )

    indirizzo = schema.TextLine(
        title=_(u"indirizzo", default=u"Indirizzo"), required=True
    )

    quartiere = schema.TextLine(
        title=_(u"quartiere", default=u"Quartiere"), required=False
    )

    circoscrizione = schema.TextLine(
        title=_(u"circoscrizione", default=u"Circoscrizione"), required=False
    )

    cap = schema.TextLine(title=_(u"cap", default=u"CAP"), required=True)

    date_significative = RichText(
        title=_(u"date_significative", default=u"Date significative"),
        required=True,
    )

    orari = RichText(title=_(u"orari", default=u"Orari"), required=True)

    # TODO: come gestire il campo "Aggiungi al calendario"

    prezzo = RichText(title=_(u"prezzo", default=u"Prezzo"), required=True)

    organizzato_da_esterno = RichText(
        title=_(u"organizzato_da_esterno", default=u"Organizzato da"),
        required=True,
    )

    organizzato_da_interno = RelationList(
        title=_(
            u"Organizzato da_interno", default=u"Organizzato da (interno)"
        ),
        default=[],
        value_type=RelationChoice(
            title=_(u"Organizzatore"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "organizzato_da_interno",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona", "Unita Organizzativa", "Servizio"],
        },
    )
    # using default event
    # contatto_persona = schema.TextLine(
    #     title=_(u'contatto_persona', default=u'Contatto: persona'),
    #     required=False,
    # )

    # using default event
    # contatto_telefono = schema.TextLine(
    #     title=_(u'contatto_telefono', default=u'Contatto: telefono'),
    #     required=False,
    # )

    contatto_reperibilita = schema.TextLine(
        title=_(u"contatto_reperibilita", default=u"Contatto: reperibilità"),
        required=False,
    )

    # using default event
    # contatto_mail = schema.TextLine(
    #     title=_(u'contatto_mail', default=u'Contatto: mail'),
    #     required=False,
    # )

    # using default event
    # sito_web = schema.TextLine(
    #     title=_(u'sito_web', default=u'Sito web'),
    #     required=False,
    # )

    # ref
    evento_supportato_da = RelationList(
        title=_(u"supportato_da", default=u"Evento supportato da"),
        required=True,
        value_type=RelationChoice(
            title=_(u"Evento supportato da"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "evento_supportato_da",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita Organizzativa"],
        },
    )

    # buggatissimo con source=CatalogSource(portal_type=['Venue']),
    #   Module plone.app.vocabularies.principals, line 147, in getTerm
    # Module plone.app.vocabularies.principals, line 113, in
    # _get_term_from_source
    # ValueError: value or token must be provided (only one of those)

    lista_eventi_figli = RelationList(
        title=u"Lista eventi figli",
        default=[],
        value_type=RelationChoice(
            title=_(u"Evento figlio"), source=SourceGeneratorTest("Venue")
        ),
        required=False,
    )
    form.widget(
        "lista_eventi_figli",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Venue"],
        },
    )

    # TODO: come fare il rating/recensione dell'evento

    ulteriori_informazioni = RichText(
        title=_(u"ulteriori_informazioni", default=u"Ulteriori informazioni"),
        required=False,
    )

    patrocinato_da = schema.TextLine(
        title=_(u"patrocinato_da", default=u"Patrocinato da"), required=False
    )

    # qui ci va anche loghi
    sponsor = RichText(title=_(u"sponsor", default=u"Sponsor"), required=False)

    # ref
    strutture_politiche = RelationList(
        title=u"Strutture politiche coinvolte",
        default=[],
        value_type=RelationChoice(
            title=_(u"Struttura politica coinvolta"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        missing_value=(),
    )
    form.widget(
        "strutture_politiche",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Unita Organizzativa"],
        },
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"), required=True
    )

    # TODO: come gestire correlati: novita'


@implementer(IEvento)
@adapter(IDexterityContent)
class Evento(object):
    """
    """

    def __init__(self, context):
        self.context = context
