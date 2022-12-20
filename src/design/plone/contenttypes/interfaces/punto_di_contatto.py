# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
# from zope import schema


class IPuntoDiContatto(model.Schema, IDesignPloneContentType):
    """Marker interface for content type PuntoDiContatto"""

    value = BlocksField(
        title=_(
            "value_pdc_label",
            default="Valore punto di contatto",
        ),
        description=_(
            "value_pdc_help",
            default="Il valore del punto di contatto: il numero compreso di prefisso "
            "internazionale (se telefono), l'account (se social network), l'URL (se sito o pagina web), l'indirizzo email (se email).",
        ),
        required=False,
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
        "persona",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
        },
    )
