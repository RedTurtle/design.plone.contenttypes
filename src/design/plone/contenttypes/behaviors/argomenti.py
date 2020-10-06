# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.component import adapter
from zope.interface import provider, implementer


class IArgomentiSchema(model.Schema):
    """ Marker interface for Argomenti
    """

    tassonomia_argomenti = RelationList(
        title=_("tassonomia_argomenti_label", default="Tassonomia argomenti"),
        description=_(
            "tassonomia_argomenti_help",
            default="Seleziona una lista di argomenti d'interesse per questo"
            " contenuto.",
        ),
        value_type=RelationChoice(
            title=_(u"Argomenti correlati"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )
    form.widget(
        "tassonomia_argomenti",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 20,
            "selectableTypes": ["Pagina Argomento"],
        },
    )

    dexteritytextindexer.searchable("tassonomia_argomenti")


@provider(IFormFieldProvider)
class IArgomenti(IArgomentiSchema):
    model.fieldset("categorization", fields=["tassonomia_argomenti"])


@provider(IFormFieldProvider)
class IArgomentiNews(IArgomentiSchema):
    """ """


@implementer(IArgomenti)
@adapter(IDexterityContent)
class Argomenti(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(IArgomentiNews)
@adapter(IDexterityContent)
class ArgomentiNews(object):
    """
    """

    def __init__(self, context):
        self.context = context
