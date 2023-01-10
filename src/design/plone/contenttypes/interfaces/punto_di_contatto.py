# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema


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

    form.widget(
        "value_punto_contatto",
        DataGridFieldFactory,
    )
