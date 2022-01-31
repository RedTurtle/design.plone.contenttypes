# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IUnitaOrganizzativa(model.Schema, IDesignPloneContentType):
    """Marker interface for content type UnitaOrganizzativa"""

    competenze = BlocksField(
        title=_("competenze", default="Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=False,
    )

    legami_con_altre_strutture = RelationList(
        title="Servizi o uffici di riferimento",
        default=[],
        description=_(
            "legami_con_altre_strutture_help",
            default="Selezionare la lista di strutture e/o uffici collegati"
            " a questa unità organizzativa.",
        ),
        value_type=RelationChoice(
            title=_("Struttura"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    responsabile = RelationList(
        title="Responsabile",
        value_type=RelationChoice(
            title=_("Responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "responsabile_help",
            default="Selezionare il/i responsabile/i della struttura.",
        ),
        default=[],
        required=False,
    )

    tipologia_organizzazione = schema.Choice(
        title=_("tipologia_organizzazione", default="Tipologia organizzazione"),
        # vocabolario di rif sara' la lista delle tipologie di organizzazione
        vocabulary="" "design.plone.vocabularies.tipologie_unita_organizzativa",
        description=_(
            "tipologia_organizzazione_help",
            default="Specificare la tipologia di organizzazione: politica,"
            " amminsitrativa o di altro tipo.",
        ),
        required=False,
    )

    assessore_riferimento = RelationList(
        title="Assessore di riferimento",
        # vocabolario di riferimento sara' dinamico con i content type
        # persona presenti all'interno della macro Amministrazione"
        value_type=RelationChoice(
            title=_("Assessore di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "assessore_riferimento_help",
            default="Inserire l'assessore di riferimento della struttura,"
            " se esiste.",
        ),
        required=False,
        default=[],
    )

    # vocabolario di riferimento sara' dinamico con i content type persona
    persone_struttura = RelationList(
        title="Persone che compongono la struttura",
        default=[],
        value_type=RelationChoice(
            title=_("Persone della struttura"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_struttura_help",
            default="Seleziona la lista delle persone che compongono" " la struttura.",
        ),
        required=False,
    )

    sede = RelationList(
        title="Sede principale",
        default=[],
        description=_(
            "sede_help",
            default="Seleziona il Luogo in cui questa struttura ha sede. "
            "Se non è presente un contenuto di tipo Luogo a cui far "
            "riferimento, puoi compilare i campi seguenti. Se selezioni un "
            "Luogo, puoi usare comunque i campi seguenti per sovrascrivere "
            "alcune informazioni.",
        ),
        value_type=RelationChoice(
            title=_("Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    sedi_secondarie = RelationList(
        title="Sedi secondarie",
        default=[],
        description=_(
            "sedi_secondarie_help",
            default="Seleziona una lista di eventuali contenuti di tipo Luogo"
            " che sono sedi secondarie di questa struttura. "
            "Per queste sedi non sarà possibile sovrascrivere i dati. "
            "Nel caso servano informazioni diverse, è possibile usare il campo"
            " sottostante.",
        ),
        value_type=RelationChoice(
            title=_("Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    contact_info = BlocksField(
        title=_("contact_info", default="Informazioni di contatto generiche"),
        required=False,
        description=_(
            "uo_contact_info_description",
            default="Inserisci eventuali informazioni di contatto aggiuntive "
            "non contemplate nei campi precedenti. "
            "Utilizza questo campo se ci sono dei contatti aggiuntivi rispetto"
            " ai contatti della sede principale. Se inserisci un collegamento "
            'con un indirizzo email, aggiungi "mailto:" prima dell\'indirizzo'
            ", per farlo aprire direttamente nel client di posta.",
        ),
    )

    #  custom widgets
    form.widget(
        "persone_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"], "maximumSelectionSize": 50},
    )
    form.widget(
        "legami_con_altre_strutture",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )
    form.widget(
        "assessore_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )
    form.widget(
        "sede",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 1, "selectableTypes": ["Venue"]},
    )
    form.widget(
        "sedi_secondarie",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Venue"],
            # "basePath": "/servizi",
        },
    )

    # custom fieldsets and order
    model.fieldset(
        "cosa_fa",
        label=_("cosa_fa_label", default="Cosa fa"),
        fields=["competenze"],
    )
    model.fieldset(
        "struttura",
        label=_("struttura_label", default="Struttura"),
        fields=[
            "legami_con_altre_strutture",
            "responsabile",
            "tipologia_organizzazione",
            "assessore_riferimento",
        ],
    )
    model.fieldset(
        "persone",
        label=_("persone_label", default="Persone"),
        fields=["persone_struttura"],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["sede", "sedi_secondarie", "contact_info"],
    )
    form.order_after(sedi_secondarie="IContattiUnitaOrganizzativa.orario_pubblico")
    form.order_after(contact_info="sedi_secondarie")

    # SearchableText indexers
    dexteritytextindexer.searchable("competenze")
    dexteritytextindexer.searchable("tipologia_organizzazione")
    dexteritytextindexer.searchable("assessore_riferimento")
    dexteritytextindexer.searchable("responsabile")
