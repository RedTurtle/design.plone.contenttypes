# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IIncarico(model.Schema, IDesignPloneContentType):
    """Marker interface for content type Incarico"""

    compensi = BlocksField(
        title=_(
            "compensi_incarico_label",
            default="Compensi",
        ),
        description=_(
            "compensi_incarico_help",
            default="Solo per incarico politico: compensi di qualsiasi natura"
            " connessi all'assunzione della carica.",
        ),
        required=False,
    )

    importi_viaggio_servizio = BlocksField(
        title=_(
            "importi_viaggio_servizio_incarico_label",
            default="Importi di viaggio e/o servizio",
        ),
        description=_(
            "importi_viaggio_servizio_incarico_help",
            default="Solo per incarico politico: importi di viaggi di servizio"
            "  e missioni pagati con fondi pubblici.",
        ),
        required=False,
    )

    persona = RelationList(
        title=_(
            "persona_incarico_label",
            default="La persona che ha la carica e l'incarico",
        ),
        description=_(
            "persona_incarico_help",
            default="Seleziona la persona che ha questo incarico",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Persona"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    unita_organizzativa = RelationList(
        title=_(
            "unita_organizzativa_incarico_label",
            default="Unità organizzativa",
        ),
        description=_(
            "unita_organizzativa_incarico_help",
            default="Seleziona l'organizzazione presso la quale svolge l'incarico.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Unità organizzativa"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    responsabile_struttura = RelationList(
        title=_(
            "responsabile_struttura_incarico_label",
            default="Responsabile della struttura",
        ),
        description=_(
            "responsabile_struttura_incarico_help",
            default="Se è un incarico di responsabilità, specificare l'organizzazione "
            "della quale è responsabile in base all'incarico",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Responsabile della struttura"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    data_inizio_incarico = schema.Date(
        title=_("data_inizio_incarico", default="Data inizio incarico"),
        required=True,
    )

    data_conclusione_incarico = schema.Date(
        title=_("data_conclusione_incarico", default="Data conclusione incarico"),
        required=False,
    )

    data_insediamento = schema.Date(
        title=_("data_insediamento", default="Data insediamento"),
        required=False,
    )

    atto_nomina = RelationList(
        title=_(
            "atto_nomina_incarico_label",
            default="Atto di nomina",
        ),
        description=_(
            "atto_nomina_incarico_help",
            default="Inserire riferimento all'atto di nomina della persona",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Atto di nomina"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    # custom widgets
    form.widget(
        "unita_organizzativa",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    form.widget(
        "persona",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
        },
    )

    form.widget(
        "responsabile_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    form.widget(
        "atto_nomina",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Documento"],
        },
    )

    #  custom fieldsets
    model.fieldset(
        "informazioni_compensi",
        label=_("informazioni_compensi_label", default="Compensi e trasparenza"),
        fields=["compensi", "importi_viaggio_servizio"],
    )
    model.fieldset(
        "date_e_informazioni",
        label=_("date_e_informazioni_label", default="Date e informazioni"),
        fields=["data_conclusione_incarico", "data_insediamento", "atto_nomina"],
    )
