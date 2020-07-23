# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import provider, implementer
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RichTextFieldWidget
from collective import dexteritytextindexer


@provider(IFormFieldProvider)
class IDescrizioneEstesa(model.Schema):
    descrizione_estesa = RichText(
        title=_(u"descrizione_estesa", default=u"Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help", default="Descrizione dettagliata e completa."
        ),
    )

    form.widget("descrizione_estesa", RichTextFieldWidget)
    form.order_after(descrizione_estesa="IBasic.description")
    dexteritytextindexer.searchable("descrizione_estesa")


@implementer(IDescrizioneEstesa)
@adapter(IDexterityContent)
class DescrizioneEstesa(object):
    """
    """

    def __init__(self, context):
        self.context = context
