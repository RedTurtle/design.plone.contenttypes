# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IDocumentoBehavior(model.Schema):
    protocollo = schema.TextLine(
        title=_(
            "protocollo_documento_label",
            default="Numero di protocollo",
        ),
        description=_(
            "protocollo_documento_help",
            default="Il numero di protocollo del documento.",
        ),
        max_length=255,
        required=False,
    )
    data_protocollo = schema.Date(
        title=_("data_protocollo", default="Data del protocollo"),
        required=False,
    )

    formati_disponibili = BlocksField(
        title=_("formati_disponibili_label", default="Formati disponibili"),
        description=_(
            "formati_disponibili_help",
            default="Lista dei formati in cui è disponibile il documento",
        ),
        required=True,
    )

    form.order_after(formati_disponibili="identificativo")
    form.order_after(data_protocollo="identificativo")
    form.order_after(protocollo="identificativo")


@implementer(IDocumentoBehavior)
@adapter(IDexterityContent)
class DocumentoBehavior(object):
    """ """

    def __init__(self, context):
        self.context = context
