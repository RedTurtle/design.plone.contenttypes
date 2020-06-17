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

    model.fieldset("categorization", fields=["notizie_collegate"])

    competenze = RichText(
        title=_(u"competenze", default=u"Competenze"), required=False
    )

    legami_con_altre_strutture = RelationList(
        title=u"Legami con altre strutture",
        default=[],
        value_type=RelationChoice(
            title=_(u"Struttura"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
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

    # vocabolario di riferimento sara' da definire, probabilmente dinamico dai
    # ct servizi presenti nella macro Amministrazione"
    notizie_collegate = RelationList(
        title=u"Notizie collegate",
        default=[],
        value_type=RelationChoice(
            title=_(u"Notizia"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )
    form.widget(
        "notizie_collegate",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["News Item"],
            # "basePath": "/servizi",
        },
    )

    ulteriori_informazioni = RichText(
        title=_(u"unteriori_informazioni", default=u"Informazioni"),
        required=False,
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"), required=True
    )

    sedi = RelationList(
        title=u"Sedi",
        default=[],
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
