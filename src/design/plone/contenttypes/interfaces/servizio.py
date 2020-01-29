from plone.supermodel import model
from plone.app.textfield import RichText
from zope import schema
from plone.namedfile import field
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.form.browser.orderedselect import OrderedSelectWidget
from plone.autoform import directives as form
from design.plone.contenttypes import _


class IServizio(model.Schema):
    """Marker interface for content type Servizio
    """

    # TODO: capire come gestire le tipologie di un servizio, FS o da u vocabolario o entrambi?
    # tipologia_servizio

    # TODO: stato servizio vuol dire si o no? Inoltre, deve essere visibile solo se il servizio
    # non e' attivo
    stato_servizio = schema.Bool(
        title=_(u"stato_servizio", default=u"Stato del servizio"),
        required=True,
    )

    motivo_stato_servizio = RichText(
        title=_(
            u"motivo_stato_servizio",
            default=u"Motivo dello stato del servizio",
        ),
        required=True,
    )

    sottotitolo = schema.TextLine(
        title=_(u"sottotitolo", default=u"Sottotitolo"), required=False,
    )

    immagine = field.NamedImage(
        title=_(u"immagine", default=u"Immagine"), required=False,
    )

    # tassonomia_argomenti = schema.Choice(
    #     title=_(u"tassonomia_argomenti", default=u"Tassonomia argomenti"),
    #     required=True,
    #     vocabulary="design.plone.contenttypes.TagsVocabulary",
    # )
    tassonomia_argomenti = schema.List(
        title=_(u"tassonomia_argomenti", default=u"Tassonomia argomenti"),
        default=[],
        value_type=schema.Choice(
            title=_(u"Argomenti"),
            vocabulary="design.plone.contenttypes.TagsVocabulary",
        ),
        required=False,
    )

    descrizione_estesa = RichText(
        title=_(u"descrizione_estesa", default=u"Descrizione estesa"),
        required=False,
    )

    descrizione_destinatari = RichText(
        title=_(
            u"descrizione_destinatari", default=u"Descrizione destinatari"
        ),
        required=True,
    )

    chi_puo_presentare = RichText(
        title=_(u"chi_puo_presentare", default=u"Chi può presentare"),
        required=False,
    )

    copertura_geografica = RichText(
        title=_(u"copertura_geografica", default=u"Copertura geografica"),
        required=False,
    )

    come_si_fa = RichText(
        title=_(u"come_si_fa", default=u"Come si fa"), required=True,
    )

    cosa_si_ottiene = RichText(
        title=_(u"cosa_si_ottiene", default=u"Cosa si ottiene"), required=True,
    )

    procedure_collegate = RichText(
        title=_(
            u"procedure_collegate", default=u"Procedure collegate all'esito"
        ),
        required=True,
    )

    # TODO: capire come gestirlo -> va benissimo cosi'
    canale_digitale = schema.TextLine(
        title=_(u"canale_digitale", default=u"Canale digitale"),
        required=False,
    )

    autenticazione = RichText(
        title=_(u"autenticazione", default=u"Autenticazione"), required=False,
    )

    canale_fisico = RichText(
        title=_(u"canale_fisico", default=u"Canale fisico"), required=True,
    )

    canale_fisico_prenotazione = schema.TextLine(
        title=_(
            u"canale_fisico_prenotazione",
            default=u"Canale fisico - prenotazione",
        ),
        required=False,
    )

    fasi_scadenze = RichText(
        title=_(u"fasi_scadenze", default=u"Fasi e scadenze"), required=True,
    )

    cosa_serve = RichText(
        title=_(u"cosa_serve", default=u"Cosa serve"), required=True,
    )

    costi = RichText(title=_(u"costi", default=u"Costi"), required=False,)

    vincoli = RichText(
        title=_(u"vincoli", default=u"Vincoli"), required=False,
    )

    # TODO: capire come gestire e cosa vogliono dal campo "fasi e scadenze"

    casi_particolari = RichText(
        title=_(u"casi_particolari", default=u"Casi particolari"),
        required=True,
    )

    # vocabolario dalle unita' organizzative presenti a catalogo?
    ufficio_responsabile = RelationList(
        title=_(u"ufficio_responsabile", default=u"Ufficio resposabile"),
        required=True,
        value_type=RelationChoice(
            title=_(u"Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "ufficio_responsabile",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione/uffici",
        },
    )

    area = RelationList(
        title=_(u"area", default=u"Area"),
        required=True,
        value_type=RelationChoice(
            title=_(u"Area"), vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "area",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione/aree-amministrative",
        },
    )

    altri_documenti = RelationList(
        title=u"Altri documenti",
        default=[],
        value_type=RelationChoice(
            title=_(u"Documento"), vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "altri_documenti",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Documento"],
            # "basePath": "/",
        },
    )

    link_siti_esterni = RichText(
        title=_(u"link_siti_esterni", default=u"Link a siti esterni"),
        required=True,
    )

    # come gestiamo "e' parte del life event"?
    # per ora gigavocabolario statico prendendo i valori da github e
    # accumunandoli in una mega lista
    life_event = schema.Choice(
        title=_(u"life_event", default=u"Parte del life event"),
        required=False,
        vocabulary="design.plone.contenttypes.AllLifeEventsVocabulary",
    )

    codice_ipa = schema.TextLine(
        title=_(u"codice_ipa", default=u"Codice dell'ente erogatore (ipa)"),
        required=True,
    )

    # classificazione basata sul catalogo dei servizi, stringa o lista?
    settore_merceologico = schema.TextLine(
        title=_(u"settore_merceologico", default=u"Settore merceologico"),
        required=True,
    )

    identificativo = schema.TextLine(
        title=_(u"identificativo", default=u"Identificativo"), required=True,
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"), required=False,
    )

    # TODO: come gestiamo i correlati novita', documenti, amministrazione, servizi
