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


class IUnitaOrganizzativa(model.Schema):
    """Marker interface for content type UnitaOrganizzativa
    """

    competenze = RichText(
        title=_(u"competenze", default=u"Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=False,
    )

    legami_con_altre_strutture = RelationList(
        title=u"Legami con altre strutture",
        default=[],
        description=_(
            "legami_con_altre_strutture_help",
            default="Selezionare la lista di strutture e/o uffici collegati"
            " a questa unità organizzativa.",
        ),
        value_type=RelationChoice(
            title=_(u"Struttura"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    responsabile = RelationList(
        title=u"Responsabile",
        value_type=RelationChoice(
            title=_(u"Responsabile"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        description=_(
            "responsabile_help",
            default="Selezionare il/i responsabile/i della struttura.",
        ),
        default=[],
        required=False,
    )

    tipologia_organizzazione = schema.Choice(
        title=_(u"tipologia_organizzazione", default=u"Tipologia organizzazione"),
        # vocabolario di rif sara' la lista delle tipologie di organizzazione
        vocabulary="" "design.plone.vocabularies.tipologie_unita_organizzativa",
        description=_(
            "tipologia_organizzazione_help",
            default="Specificare la tipologia di organizzazione: politica,"
            " amminsitrativa o di altro tipo.",
        ),
        required=True,
    )

    assessore_riferimento = RelationList(
        title=u"Assessore di riferimento",
        # vocabolario di riferimento sara' dinamico con i content type
        # persona presenti all'interno della macro Amministrazione"
        value_type=RelationChoice(
            title=_(u"Assessore di riferimento"),
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
        title=u"Persone che compongono la struttura",
        default=[],
        value_type=RelationChoice(
            title=_(u"Persone della struttura"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_struttura_help",
            default="Seleziona la lista delle persone che compongono" " la struttura.",
        ),
        required=False,
    )

    sedi = RelationList(
        title=u"Altre sedi",
        default=[],
        description=_(
            "sedi_help", default="Seleziona una lista delle sedi di questa struttura."
        ),
        value_type=RelationChoice(
            title=_(u"Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    contact_info = RichText(
        title=_(u"contact_info", default=u"Informazioni di contatto generiche"),
        required=False,
        description=_(
            "uo_contact_info_description",
            default="Eventuali informazioni di contatto generiche",
        ),
    )

    #  custom widgets
    form.widget(
        "persone_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 10, "selectableTypes": ["Persona"]},
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
        "sedi",
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
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["legami_con_altre_strutture"],
    )

    form.order_after(sedi="IGeolocatable.geolocation")

    # SearchableText indexers
    dexteritytextindexer.searchable("competenze")
    dexteritytextindexer.searchable("tipologia_organizzazione")
    dexteritytextindexer.searchable("assessore_riferimento")
    dexteritytextindexer.searchable("responsabile")
