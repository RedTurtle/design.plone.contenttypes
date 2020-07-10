# -*- coding: utf-8 -*-
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
    model.fieldset(
        "correlati",
        label=_("correlati_label", default=u"Correlati"),
        fields=["legami_con_altre_strutture"],
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

    responsabile = RelationList(
        title=u"Responsabile",
        value_type=RelationChoice(
            title=_(u"Responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "responsabile_help",
            default="Selezionare il/i responsabile/i della struttura.",
        ),
        default=[],
        required=False,
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

    tipologia_organizzazione = schema.Choice(
        title=_(
            u"tipologia_organizzazione", default=u"Tipologia organizzazione"
        ),
        # vocabolario di rif sara' la lista delle tipologie di organizzazione
        vocabulary=""
        "design.plone.vocabularies.tipologie_unita_organizzativa",
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
            default="Seleziona la lista delle persone che compongono"
            " la struttura.",
        ),
        required=False,
    )
    form.widget(
        "persone_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )

    # # vocabolario di riferimento sara' da definire, probabilmente dinamico
    # dai ct servizi presenti nella macro Amministrazione"
    # servizi_offerti = RelationList(
    #     title=u"Servizi offerti",
    #     default=[],
    #     value_type=RelationChoice(
    #         title=_(u"Servizio"), vocabulary="plone.app.vocabularies.Catalog"
    #     ),
    #     required=False,
    # )
    # form.widget(
    #     "servizi_offerti",
    #     RelatedItemsFieldWidget,
    #     pattern_options={
    #         "maximumSelectionSize": 10,
    #         "selectableTypes": ["Servizio"],
    #         # "basePath": "/servizi",
    #     },
    # )

    ulteriori_informazioni = RichText(
        title=_(u"unteriori_informazioni", default=u"Informazioni"),
        required=False,
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"),
        required=False,
        description=_(
            "uo_box_aiuto_help",
            default="Eventuali contatti di supporto all'utente.",
        ),
    )

    sedi = RelationList(
        title=u"Sedi",
        default=[],
        description=_(
            "sedi_help",
            default="Seleziona una lista delle sedi di questa struttura.",
        ),
        value_type=RelationChoice(
            title=_(u"Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
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
