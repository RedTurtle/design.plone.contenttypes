# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


class IPDCValueSchema(model.Schema):
    pdc_type = schema.Choice(
        title=_("pdc_type_label", default="Tipo"),
        description=_(
            "type_help",
            default="Tipo",
        ),
        vocabulary="collective.taxonomy.tipologia_pdc",
        required=True,
        default="",
    )
    pdc_value = schema.TextLine(
        title=_("pdc_value_label", default="Contatto"),
        description=_(
            "pdc_value_help",
            default="Contatto",
        ),
        required=True,
        default="",
        max_length=255,
    )


class IPuntoDiContatto(model.Schema, IDesignPloneContentType):
    """Marker interface for content type PuntoDiContatto"""

    value_punto_contatto = schema.List(
        title="Valore punto di contatto",
        default=[],
        value_type=DictRow(schema=IPDCValueSchema),
        description=_(
            "value_punto_contatto_help",
            default="Il valore del punto di contatto: il numero compreso di prefisso "
            "internazionale (se telefono), l'account (se social network), l'URL (se sito o pagina web), l'indirizzo email (se email).",  # noqa
        ),
        required=True,
    )
    persona = RelationList(
        title=_(
            "persona_incarico_label",
            default="Persona",
        ),
        description=_(
            "persona_incarico_help",
            default="Seleziona la/e persona/e che ha/hanno la carica e l'incarico.",
        ),
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        default=[],
    )

    form.widget(
        "value_punto_contatto",
        DataGridFieldFactory,
    )

    form.widget(
        "persona",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
        },
    )
