# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import DateFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class ITempiEScadenzeValueSchema(model.Schema):
    data_scadenza = schema.Date(
        title=_("data_scadenza_label", default="Data scadenza"),
        description=_(
            "data_scadenza_help",
            default="Data di scadenza della fase",
        ),
        required=False,
    )
    milestone = schema.TextLine(
        title=_("milestone_label", default="Titolo"),
        description=_(
            "milestone_help",
            default="Titolo della fase",
        ),
        required=True,
        default="",
    )
    interval_qt = schema.TextLine(
        title=_("interval_qt_label", default="Intervallo"),
        description=_(
            "interval_qt_help",
            default="Intervallo della fase",
        ),
        required=False,
        default="",
    )
    interval_type = schema.TextLine(
        title=_("interval_type_label", default="Tipo intervallo"),
        description=_(
            "interval_type_help",
            default="Ad esempio: " "ore, giorni, settimane, mesi.",
        ),
        required=False,
        default="",
    )
    milestone_description = schema.TextLine(
        title=_("milestone_description_label", default="Sottotitolo"),
        description=_(
            "milestone_description_help",
            default="Sottotitolo della fase",
        ),
        required=False,
        default="",
    )

    form.widget(
        "data_scadenza",
        DateFieldWidget,
    )


class IServizio(model.Schema, IDesignPloneContentType):
    """Marker interface for content type Servizio"""

    sottotitolo = schema.TextLine(
        title=_("sottotitolo_label", default="Sottotitolo"),
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
        title=_("stato_servizio_label", default="Servizio non fruibile"),
        required=False,
        description=_(
            "stato_servizio_help",
            default="Indica se il servizio è effettivamente fruibile; spuntare se non è fruibile.",  # noqa
        ),
    )

    motivo_stato_servizio = BlocksField(
        title=_(
            "motivo_stato_servizio_label",
            default="Motivo dello stato",
        ),
        required=False,
        description=_(
            "motivo_stato_servizio_help",
            default="Descrizione del motivo per cui il servizio non è attivo. È obbligatorio se il campo precedente è spuntato.",  # noqa
        ),
    )

    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio e chi può usufruirne.",
        ),
    )

    chi_puo_presentare = BlocksField(
        title=_("chi_puo_presentare_label", default="Chi può presentare"),
        required=False,
        description=_(
            "chi_puo_presentare_help",
            default="Descrizione di chi può presentare domanda per usufruire"
            " del servizio e delle diverse casistiche.",
        ),
    )

    copertura_geografica = BlocksField(
        title=_("copertura_geografica_label", default="Copertura geografica"),
        required=False,
        description=_(
            "copertura_geografica_help",
            default="Indicare se il servizio si riferisce ad una particolare"
            " area geografica o all'intero territorio di riferimento.",
        ),
    )

    come_si_fa = BlocksField(
        title=_("come_si_fa", default="Come fare"),
        required=True,
        description=_(
            "come_si_fa_help",
            default="Descrizione della procedura da seguire per poter"
            " usufruire del servizio.",
        ),
    )

    cosa_si_ottiene = BlocksField(
        title=_("cosa_si_ottiene", default="Cosa si ottiene"),
        description=_(
            "cosa_si_ottiene_help",
            default="Indicare cosa si può ottenere dal servizio, ad esempio"
            " 'carta di identità elettronica', 'certificato di residenza'.",
        ),
        required=True,
    )

    procedure_collegate = BlocksField(
        title=_("procedure_collegate", default="Procedure collegate all'esito"),
        required=False,
        description=_(
            "procedure_collegate_help",
            default="Indicare cosa deve fare l'utente del servizio per"
            " conoscere l'esito della procedura, e dove eventualmente"
            " poter ritirare l'esito.",
        ),
    )

    canale_digitale = BlocksField(
        title=_("canale_digitale", default="Canale digitale"),
        description=_(
            "canale_digitale_help",
            default="Testo di introduzione del canale digitale",
        ),
        required=False,
    )

    canale_digitale_link = schema.URI(
        title=_("canale_digitale_link", default="Link al canale digitale"),
        description=_(
            "canale_digitale_link_help",
            default="Collegamento con l'eventuale canale digitale di"
            " attivazione del servizio.",
        ),
        required=False,
    )
    # vocabolario dalle unita' organizzative presenti a catalogo?
    canale_fisico = RelationList(
        title=_("canale_fisico", default="Canale fisico"),
        description=_(
            "canale_fisico_help",
            default="Sedi per la fruizione del servizio",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Canale fisico"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    autenticazione = BlocksField(
        title=_("autenticazione", default="Autenticazione"),
        description=_(
            "autenticazione_help",
            default="Indicare, se previste, le modalità di autenticazione"
            " necessarie per poter accedere al servizio.",
        ),
        required=False,
    )

    dove_rivolgersi = RelationList(
        title="Dove rivolgersi",
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        description=_(
            "dove_rivolgersi_help",
            default="Seleziona una lista delle sedi e dei luoghi in cui è presente"
            " questo servizio.",
        ),
    )

    dove_rivolgersi_extra = BlocksField(
        title=_(
            "dove_rivolgersi_extra",
            default="Dove rivolgersi: informazioni aggiuntive",
        ),
        description=_(
            "dove_rivolgersi_extra_help",
            default="Indicare eventuali informazioni aggiuntive riguardo al dove "
            "rivolgersi per questo servizio.",
        ),
        required=False,
    )

    prenota_appuntamento = BlocksField(
        title=_("prenota_appuntamento", default="Prenota un appuntamento"),
        description=_(
            "prenota_appuntamento_help",
            default="Se è possibile prenotare un'appuntamento, indicare"
            " le informazioni necessarie e il collegamento al servizio di "
            "prenotazione appuntamenti del Comune.",
        ),
        required=False,
    )

    tempi_e_scadenze = BlocksField(
        title=_("tempi_e_scadenze", default="Tempi e scadenze"),
        required=True,
        description=_(
            "tempi_e_scadenze_help",
            default="Descrivere le informazioni dettagliate riguardo eventuali tempi"
            " e scadenze di questo servizio.",
        ),
    )

    timeline_tempi_scadenze = schema.List(
        title=_("timeline_tempi_scadenze", default="Timeline tempi e scadenze"),
        default=[],
        value_type=DictRow(schema=ITempiEScadenzeValueSchema),
        description=_(
            "timeline_tempi_scadenze_help",
            default="Timeline tempi e scadenze del servizio: indicare per ogni "
            "scadenza un titolo descritttivo di tale scadenza e, opzionalmente,"
            " informazioni sulle date o gli intervalli di tempo che "
            "intercorrono tra una fase e la successiva.",
        ),
        required=False,
    )

    cosa_serve = BlocksField(
        title=_("cosa_serve", default="Cosa serve"),
        required=True,
        description=_(
            "cosa_serve_help",
            default="Descrizione delle istruzioni per usufruire del servizio.",
        ),
    )

    costi = BlocksField(
        title=_("costi", default="Costi"),
        required=False,
        description=_(
            "costi_help",
            default="Descrizione delle condizioni e dei termini economici per"
            " completare la procedura di richiesta del servizio.",
        ),
    )

    vincoli = BlocksField(
        title=_("vincoli", default="Vincoli"),
        required=False,
        description=_(
            "vincoli_help",
            default="Descrizione degli eventuali vincoli presenti.",
        ),
    )

    casi_particolari = BlocksField(
        title=_("casi_particolari", default="Casi particolari"),
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
            "ufficio_responsabile_erogazione",
            default="Unità organizzativa responsabile",
        ),
        description=_(
            "ufficio_responsabile_help",
            default="Seleziona gli uffici responsabili dell'erogazione"
            " di questo servizio.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Unità organizzativa responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    area = RelationList(
        title=_("area", default="Area"),
        required=False,
        default=[],
        description=_(
            "area_help",
            default="Seleziona l'area da cui dipende questo servizio.",
        ),
        value_type=RelationChoice(
            title=_("Area"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    altri_documenti = RelationList(
        title="Documenti",
        default=[],
        description=_(
            "altri_documenti_help",
            default="Seleziona la lista dei documenti di supporto collegati"
            " a questo servizio.",
        ),
        value_type=RelationChoice(
            title=_("Documento"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    link_siti_esterni = BlocksField(
        title=_("link_siti_esterni", default="Link a siti esterni"),
        required=False,
        description=_(
            "link_siti_esterni_help",
            default="Eventuali collegamenti a pagine web, siti, servizi"
            " esterni all'ambito Comunale utili all'erogazione del servizio.",
        ),
    )

    codice_ipa = schema.TextLine(
        title=_("codice_ipa", default="Codice dell'ente erogatore (ipa)"),
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
        title=_("settore_merceologico", default="Settore merceologico"),
        required=False,
        description=_(
            "settore_merceologico_help",
            default="Classificazione del servizio basata su catalogo dei"
            " servizi (Classificazione NACE).",
        ),
    )

    identificativo = schema.TextLine(
        title=_("identificativo", default="Identificativo"),
        required=False,
        description=_(
            "identificativo_help",
            default="Eventuale codice identificativo del servizio.",
        ),
    )

    condizioni_di_servizio = field.NamedBlobFile(
        title=_("condizioni_di_servizio", default="Condizioni di servizio"),
        required=True,
    )

    servizi_collegati = RelationList(
        title=_("servizi_collegati_label", default="Servizi collegati"),
        description=_(
            "servizi_collegati_help",
            default="Seleziona la lista dei servizi collegati a questo.",
        ),
        default=[],
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )

    # custom widgets
    form.widget(
        "canale_fisico",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
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
            "selectableTypes": ["Documento", "CartellaModulistica"],
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
    form.widget(
        "timeline_tempi_scadenze",
        DataGridFieldFactory,
        frontendOptions={"widget": "data_grid"},
    )

    # custom fieldset and order
    model.fieldset(
        "a_chi_si_rivolge",
        label=_("a_chi_si_rivolge_label", default="A chi si rivolge"),
        fields=["a_chi_si_rivolge", "chi_puo_presentare", "copertura_geografica"],
    )

    model.fieldset(
        "accedi_al_servizio",
        label=_("accedi_al_servizio_label", default="Accedere al servizio"),
        fields=[
            "come_si_fa",
            "cosa_si_ottiene",
            "procedure_collegate",
            "canale_digitale",
            "canale_digitale_link",
            "canale_fisico",
            "autenticazione",
            "dove_rivolgersi",
            "dove_rivolgersi_extra",
            "prenota_appuntamento",
        ],
    )
    model.fieldset(
        "cosa_serve",
        label=_("cosa_serve_label", default="Cosa serve"),
        fields=["cosa_serve"],
    )
    model.fieldset(
        "costi_e_vincoli",
        label=_("costi_e_vincoli_label", default="Costi e vincoli"),
        fields=["costi", "vincoli"],
    )

    model.fieldset(
        "tempi_e_scadenze",
        label=_("tempi_e_scadenze_label", default="Tempi e scadenze"),
        fields=["tempi_e_scadenze", "timeline_tempi_scadenze"],
    )

    model.fieldset(
        "casi_particolari",
        label=_("casi_particolari_label", default="Casi particolari"),
        fields=["casi_particolari"],
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["ufficio_responsabile", "area"],
    )
    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=["altri_documenti"],
    )
    model.fieldset(
        "link_utili",
        label=_("link_utili_label", default="Link utili"),
        fields=["link_siti_esterni"],
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["servizi_collegati"],
    )

    model.fieldset(
        "categorization",
        fields=["codice_ipa", "settore_merceologico", "identificativo"],
    )

    # SearchableText fields
    textindexer.searchable("sottotitolo")
    textindexer.searchable("a_chi_si_rivolge")
    textindexer.searchable("chi_puo_presentare")
    textindexer.searchable("come_si_fa")
    textindexer.searchable("cosa_si_ottiene")
    textindexer.searchable("cosa_serve")
    textindexer.searchable("area")
    textindexer.searchable("ufficio_responsabile")
    textindexer.searchable("copertura_geografica")
    textindexer.searchable("costi")
    textindexer.searchable("servizi_collegati")
    textindexer.searchable("link_siti_esterni")
