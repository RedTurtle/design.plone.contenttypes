# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces.documento import IDocumento
from plone.app.dexterity import textindexer
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class IDescrizioneEstesaSchema(model.Schema):
    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    textindexer.searchable("descrizione_estesa")


@provider(IFormFieldProvider)
class IDescrizioneEstesa(IDescrizioneEstesaSchema):
    """ """

    form.order_after(descrizione_estesa="IBasic.description")


@provider(IFormFieldProvider)
class IDescrizioneEstesaServizio(model.Schema):
    """ """

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    textindexer.searchable("descrizione_estesa")

    model.fieldset(
        "cose",
        label=_("cose_label", default="Cos'è"),
        fields=["descrizione_estesa"],
    )


@provider(IFormFieldProvider)
class IDescrizioneEstesaDocumento(IDescrizioneEstesaSchema):
    """ """

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default="Descrizione"),
        fields=["descrizione_estesa"],
    )


@implementer(IDescrizioneEstesa)
@adapter(IDexterityContent)
class DescrizioneEstesa(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IDescrizioneEstesaServizio)
@adapter(IDexterityContent)
class DescrizioneEstesaServizio(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IDescrizioneEstesaDocumento)
@adapter(IDocumento)
class DescrizioneEstesaDocumento(object):
    """"""

    def __init__(self, context):
        self.context = context
