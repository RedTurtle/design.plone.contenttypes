# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IServizio(model.Schema):
    """Marker interface for content type Servizio
    """

    # TODO: capire come gestire le tipologie di un servizio, FS o da u
    # vocabolario o entrambi?
    # tipologia_servizio
    sottotitolo = schema.TextLine(
        title=_(u"sottotitolo", default=u"Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo per"
            " questo servizio.",
        ),
        required=False,
    )

    # TODO: stato servizio vuol dire si o no? Inoltre, deve essere visibile
    # solo se il servizio
    # non e' attivo
    stato_servizio = schema.Bool(
        title=_(u"stato_servizio", default=u"Servizio non attivo"),
        required=False,
        description=_(
            "stato_servizio_help",
            default="Indica se il servizio è effettivamente fruibile.",
        ),
    )

    motivo_stato_servizio = RichText(
        title=_(
            u"motivo_stato_servizio",
            default=u"Motivo dello stato del servizio nel caso non sia attivo",
        ),
        required=False,
        description=_(
            "motivo_stato_servizio_help",
            default="Descrizione del motivo per cui il servizio non è attivo.",
        ),
    )

    descrizione_destinatari = RichText(
        title=_(u"descrizione_destinatari", default=u"Descrizione destinatari"),
        required=False,
        description=_(
            "descrizione_destinatari_help",
            default="Descrizione dei principali interlocutori del servizio:"
            " a chi si rivolge e chi può usufruirne.",
        ),
    )

    chi_puo_presentare = RichText(
        title=_(u"chi_puo_presentare", default=u"Chi può presentare"),
        required=False,
        description=_(
            "chi_puo_presentare_help",
            default="Descrizione di chi può presentare domanda per usufruire"
            " del servizio e delle diverse casistiche.",
        ),
    )

    copertura_geografica = RichText(
        title=_(u"copertura_geografica", default=u"Copertura geografica"),
        required=False,
        description=_(
            "copertura_geografica_help",
            default="Indicare se il servizio si riferisce ad una particolare"
            " area geografica o all'intero territorio di riferimento.",
        ),
    )

    come_si_fa = RichText(
        title=_(u"come_si_fa", default=u"Come si fa"),
        required=False,
        description=_(
            "come_si_fa_help",
            default="Descrizione della procedura da seguire per poter"
            " usufruire del servizio.",
        ),
    )

    cosa_si_ottiene = RichText(
        title=_(u"cosa_si_ottiene", default=u"Cosa si ottiene"),
        description=_(
            "cosa_si_ottiene_help",
            default="Indicare cosa si può ottenere dal servizio, ad esempio"
            " 'carta di identità elettronica', 'certificato di residenza'.",
        ),
        required=False,
    )

    procedure_collegate = RichText(
        title=_(u"procedure_collegate", default=u"Procedure collegate all'esito"),
        required=False,
        description=_(
            "procedure_collegate_help",
            default="Indicare cosa deve fare l'utente del servizio per"
            " conoscere l'esito della procedura, e dove eventualmente"
            " poter ritirare l'esito.",
        ),
    )

    canale_digitale = RichText(
        title=_(u"canale_digitale", default=u"Canale digitale"),
        description=_(
            "canale_digitale_help",
            default="Collegamento con l'eventuale canale digitale di"
            " attivazione del servizio.",
        ),
        required=False,
    )

    autenticazione = RichText(
        title=_(u"autenticazione", default=u"Autenticazione"),
        description=_(
            "autenticazione_help",
            default="Indicare, se previste, le modalità di autenticazione"
            " necessarie per poter accedere al servizio.",
        ),
        required=False,
    )

    canale_fisico = RichText(
        title=_(u"canale_fisico", default=u"Canale fisico"),
        description=_(
            "canale_fisico_help",
            default="Indica le sedi dove è possibile usufruire del servizio.",
        ),
        required=False,
    )

    canale_fisico_prenotazione = RichText(
        title=_(u"canale_fisico_prenotazione", default=u"Canale fisico - prenotazione"),
        description=_(
            "canale_fisico_prenotazione_help",
            default="Se è possibile prenotare un'appuntamento, indicare"
            " il collegamento al servizio di prenotazione appuntamenti"
            " del Comune.",
        ),
        required=False,
    )

    fasi_scadenze = RichText(
        title=_(u"fasi_scadenze", default=u"Fasi e scadenze"),
        required=False,
        description=_(
            "fasi_scadenze_help",
            default="Prevedere una data di scadenza del servizio."
            " Se il servizio è diviso in fasi, descriverne modalità e"
            " tempistiche.",
        ),
    )

    cosa_serve = RichText(
        title=_(u"cosa_serve", default=u"Cosa serve"),
        required=True,
        description=_(
            "cosa_serve_help",
            default="Descrizione delle istruzioni per usufruire del servizio.",
        ),
    )

    costi = RichText(
        title=_(u"costi", default=u"Costi"),
        required=False,
        description=_(
            "costi_help",
            default="Descrizione delle condizioni e dei termini economici per"
            " completare la procedura di richiesta del servizio.",
        ),
    )

    vincoli = RichText(
        title=_(u"vincoli", default=u"Vincoli"),
        required=False,
        description=_(
            "vincoli_help", default="Descrizione degli eventuali vincoli presenti."
        ),
    )

    casi_particolari = RichText(
        title=_(u"casi_particolari", default=u"Casi particolari"),
        required=False,
        description=_(
            "casi_particolari_help",
            default="Descrizione degli evetuali casi particolari riferiti"
            " alla fruibilità di questo servizio.",
        ),
    )

    # vocabolario dalle unita' organizzative presenti a catalogo?
    ufficio_responsabile = RelationList(
        title=_(u"ufficio_responsabile_erogazione", default=u"Ufficio responsabile"),
        description=_(
            "ufficio_responsabile_help",
            default="Seleziona l'ufficio responsabile dell'erogazione"
            " di questo servizio.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_(u"Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    area = RelationList(
        title=_(u"area", default=u"Area"),
        required=True,
        default=[],
        description=_(
            "area_help", default="Seleziona l'area da cui dipende questo servizio."
        ),
        value_type=RelationChoice(
            title=_(u"Area"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    altri_documenti = RelationList(
        title=u"Documenti correlati",
        default=[],
        description=_(
            "altri_documenti_help",
            default="Seleziona la lista dei documenti di supporto collegati"
            " a questo servizio.",
        ),
        value_type=RelationChoice(
            title=_(u"Documento"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    link_siti_esterni = RichText(
        title=_(u"link_siti_esterni", default=u"Link a siti esterni"),
        required=False,
        description=_(
            "link_siti_esterni_help",
            default="Eventuali collegamenti a pagine web, siti, servizi"
            " esterni all'ambito Comunale utili all'erogazione del servizio.",
        ),
    )

    # come gestiamo "e' parte del life event"?
    # per ora gigavocabolario statico prendendo i valori da github e
    # accumunandoli in una mega lista
    life_event = schema.Choice(
        title=_(u"life_event", default=u"Parte del life event"),
        description=_(
            "life_event_help",
            default="Collegamento tra il servizio e un evento della vita di "
            "una persona o di un'impresa. Ad esempio: il servizio 'Anagrafe' è"
            " collegato alla nascita di un bambino",
        ),
        required=False,
        vocabulary="design.plone.contenttypes.AllLifeEventsVocabulary",
    )

    codice_ipa = schema.TextLine(
        title=_(u"codice_ipa", default=u"Codice dell'ente erogatore (ipa)"),
        required=False,
        description=_(
            "codice_ipa_help",
            default="Specificare il nome dell’organizzazione, come indicato"
            " nell’Indice della Pubblica Amministrazione (IPA), che esercita"
            " uno specifico ruolo sul Servizio.",
        ),
    )

    # classificazione basata sul catalogo dei servizi, stringa o lista?
    settore_merceologico = schema.TextLine(
        title=_(u"settore_merceologico", default=u"Settore merceologico"),
        required=False,
        description=_(
            "settore_merceologico_help",
            default="Classificazione del servizio basata su catalogo dei"
            " servizi (Classificazione NACE).",
        ),
    )

    identificativo = schema.TextLine(
        title=_(u"identificativo", default=u"Identificativo"),
        required=False,
        description=_(
            "identificativo_help",
            default="Eventuale codice identificativo del servizio.",
        ),
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"),
        required=False,
        description=_(
            "box_aiuto_help",
            default="Ulteriori informazioni sul Servizio, FAQ, eventuali"
            " riferimenti normativi ed eventuali contatti di supporto"
            " all'utente.",
        ),
    )

    servizi_collegati = RelationList(
        title=u"Servizi collegati",
        default=[],
        value_type=RelationChoice(
            title=_(u"Servizi collegati"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
        description=_(
            "servizi_collegati_help",
            default="Seleziona la lista dei servizi collegati" " a questo.",
        ),
    )

    sedi_e_luoghi = RelationList(
        title=u"Dove trovarci",
        default=[],
        value_type=RelationChoice(
            title=_(u"Dove trovarci"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
        description=_(
            "sedi_e_luoghi_help",
            default="Seleziona la lista delle sedi e dei luoghi collegati"
            " a questo servizio.",
        ),
    )

    # custom widgets
    form.widget(
        "sedi_e_luoghi",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Venue"],
            # "basePath": "/",
        },
    )
    form.widget(
        "area",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione/aree-amministrative",
        },
    )
    form.widget(
        "ufficio_responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione/uffici",
        },
    )
    form.widget(
        "altri_documenti",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Documento"],
            # "basePath": "/",
        },
    )
    form.widget(
        "servizi_collegati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Servizio"],
            # "basePath": "/",
        },
    )

    # custom fieldset and order
    model.fieldset("correlati", fields=["servizi_collegati", "altri_documenti"])

    # SearchableText fields
    dexteritytextindexer.searchable("sottotitolo")
    dexteritytextindexer.searchable("descrizione_destinatari")
    dexteritytextindexer.searchable("chi_puo_presentare")
    dexteritytextindexer.searchable("come_si_fa")
    dexteritytextindexer.searchable("cosa_si_ottiene")
    dexteritytextindexer.searchable("cosa_serve")
    dexteritytextindexer.searchable("box_aiuto")
    dexteritytextindexer.searchable("area")
    dexteritytextindexer.searchable("ufficio_responsabile")
    dexteritytextindexer.searchable("copertura_geografica")
    dexteritytextindexer.searchable("costi")
    dexteritytextindexer.searchable("life_event")
    dexteritytextindexer.searchable("servizi_collegati")
