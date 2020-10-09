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

    sottotitolo = schema.TextLine(
        title=_(u"sottotitolo_label", default=u"Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )

    # TODO: stato servizio vuol dire si o no? Inoltre, deve essere visibile
    # solo se il servizio
    # non e' attivo
    stato_servizio = schema.Bool(
        title=_(u"stato_servizio_label", default=u"Servizio non attivo"),
        required=False,
        description=_(
            "stato_servizio_help",
            default="Indica se il servizio è effettivamente fruibile.",
        ),
    )

    motivo_stato_servizio = RichText(
        title=_(
            u"motivo_stato_servizio_label",
            default=u"Motivo dello stato del servizio nel caso non sia attivo",
        ),
        required=False,
        description=_(
            "motivo_stato_servizio_help",
            default="Descrizione del motivo per cui il servizio non è attivo.",
        ),
    )

    a_chi_si_rivolge = RichText(
        title=_(u"a_chi_si_rivolge_label", default=u"A chi si rivolge"),
        required=False,
        description=_(
            "a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio e chi può usufruirne.",
        ),
    )

    chi_puo_presentare = RichText(
        title=_(u"chi_puo_presentare_label", default=u"Chi può presentare"),
        required=False,
        description=_(
            "chi_puo_presentare_help",
            default="Descrizione di chi può presentare domanda per usufruire"
            " del servizio e delle diverse casistiche.",
        ),
    )

    copertura_geografica = RichText(
        title=_(
            u"copertura_geografica_label", default=u"Copertura geografica"
        ),
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
        title=_(
            u"procedure_collegate", default=u"Procedure collegate all'esito"
        ),
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

    dove_rivolgersi = RelationList(
        title=u"Dove rivolgersi",
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        description=_(
            "dove_rivolgersi_help",
            default="Seleziona una lista delle sedi e dei luoghi in cui è presente"
            " questo servizio.",
        ),
    )

    dove_rivolgersi_extra = RichText(
        title=_(
            u"dove_rivolgersi_extra",
            default=u"Dove rivolgersi: informazioni aggiuntive",
        ),
        description=_(
            "dove_rivolgersi_extra_help",
            default="Indicare eventuali informazioni aggiuntive riguardo al dove "
            "rivolgersi per questo servizio.",
        ),
        required=False,
    )

    prenota_appuntamento = RichText(
        title=_(u"prenota_appuntamento", default=u"Prenota un appuntamento"),
        description=_(
            "prenota_appuntamento_help",
            default="Se è possibile prenotare un'appuntamento, indicare"
            " le informazioni necessarie e il collegamento al servizio di "
            "prenotazione appuntamenti del Comune.",
        ),
        required=False,
    )

    tempi_e_scadenze = RichText(
        title=_(u"tempi_e_scadenze", default=u"Tempi e scadenze"),
        required=False,
        description=_(
            "tempi_e_scadenze_help",
            default="Descrivere le informazioni dettagliate riguardo eventuali tempi"
            " e scadenze di questo servizio.",
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
            "vincoli_help",
            default="Descrizione degli eventuali vincoli presenti.",
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
        title=_(
            u"ufficio_responsabile_erogazione", default=u"Ufficio responsabile"
        ),
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
        required=False,
        default=[],
        description=_(
            "area_help",
            default="Seleziona l'area da cui dipende questo servizio.",
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

    servizi_collegati = RelationList(
        title=u"Servizi collegati",
        default=[],
        value_type=RelationChoice(
            title=_(u"Servizi collegati"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        description=_(
            "servizi_collegati_help",
            default="Seleziona la lista dei servizi collegati" " a questo.",
        ),
    )

    # custom widgets
    form.widget(
        "dove_rivolgersi",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Venue", "UnitaOrganizzativa"],
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
    model.fieldset(
        "a_chi_si_rivolge",
        label=_("a_chi_si_rivolge_label", default=u"A chi si rivolge"),
        fields=[
            "a_chi_si_rivolge",
            "chi_puo_presentare",
            "copertura_geografica",
        ],
    )
    model.fieldset(
        "accedi_al_servizio",
        label=_("accedi_al_servizio_label", default=u"Accedere al servizio"),
        fields=[
            "come_si_fa",
            "cosa_si_ottiene",
            "procedure_collegate",
            "canale_digitale",
            "autenticazione",
            "dove_rivolgersi",
            "dove_rivolgersi_extra",
            "prenota_appuntamento",
        ],
    )
    model.fieldset(
        "cosa_serve",
        label=_("cosa_serve_label", default=u"Cosa serve"),
        fields=["cosa_serve"],
    )
    model.fieldset(
        "costi_e_vincoli",
        label=_("costi_e_vincoli_label", default=u"Costi e vincoli"),
        fields=["costi", "vincoli"],
    )

    model.fieldset(
        "tempi_e_scadenze",
        label=_("tempi_e_scadenze_label", default=u"Tempi e scadenze"),
        fields=["tempi_e_scadenze"],
    )

    model.fieldset(
        "casi_particolari",
        label=_("casi_particolari_label", default=u"Casi particolari"),
        fields=["casi_particolari"],
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=["ufficio_responsabile", "area"],
    )
    model.fieldset(
        "documenti",
        label=_("documenti_label", default=u"Documenti"),
        fields=["altri_documenti"],
    )
    model.fieldset(
        "link_utili",
        label=_("link_utili_label", default=u"Link utili"),
        fields=["link_siti_esterni"],
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default=u"Contenuti collegati"),
        fields=["servizi_collegati"],
    )

    model.fieldset(
        "categorization",
        fields=["codice_ipa", "settore_merceologico", "identificativo"],
    )

    # SearchableText fields
    dexteritytextindexer.searchable("sottotitolo")
    dexteritytextindexer.searchable("a_chi_si_rivolge")
    dexteritytextindexer.searchable("chi_puo_presentare")
    dexteritytextindexer.searchable("come_si_fa")
    dexteritytextindexer.searchable("cosa_si_ottiene")
    dexteritytextindexer.searchable("cosa_serve")
    dexteritytextindexer.searchable("area")
    dexteritytextindexer.searchable("ufficio_responsabile")
    dexteritytextindexer.searchable("copertura_geografica")
    dexteritytextindexer.searchable("costi")
    dexteritytextindexer.searchable("servizi_collegati")
