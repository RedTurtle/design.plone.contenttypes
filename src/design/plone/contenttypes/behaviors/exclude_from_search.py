# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IExcludeFromSearch(model.Schema):
    """ """

    exclude_from_search = schema.Bool(
        title=_("exclude_from_search_label", default="Escludi dalla ricerca"),
        description=_(
            "help_exclude_from_search",
            default="Se selezionato, questo contenuto non verrà mostrato nelle ricerche del sito per gli utenti anonimi.",
        ),
        required=False,
        default=False,
    )
    model.fieldset(
        "settings",
        fields=["exclude_from_search"],
    )


@implementer(IExcludeFromSearch)
@adapter(IDexterityContent)
class ExcludeFromSearch(object):
    """ """

    def __init__(self, context):
        self.context = context
