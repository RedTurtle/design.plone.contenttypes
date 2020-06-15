# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class IArgomenti(model.Schema):
    """ Marker interface for Argomenti
    """

    tassonomia_argomenti = schema.List(
        title=_("tassonomia_argomenti_label", default="Tassonomia argomenti"),
        description=_(
            "tassonomia_argomenti_help",
            default="Seleziona una lista di argomenti d'interesse per questo"
            "contenuto.",
        ),
        default=[],
        value_type=schema.Choice(
            vocabulary="design.plone.contenttypes.TagsVocabulary"
        ),
        required=False,
    )

    model.fieldset("categorization", fields=["tassonomia_argomenti"])
    form.order_before(tassonomia_argomenti="IDublinCore.subjects")


@implementer(IArgomenti)
@adapter(IDexterityContent)
class Argomenti(object):
    """
    """

    def __init__(self, context):
        self.context = context
