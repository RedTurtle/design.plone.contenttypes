# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


# TODO: merge with NEWS
@provider(IFormFieldProvider)
class IDatasetCorrelati(model.Schema):

    dataset_correlati = RelationList(
        title=_("dataset_correlati_label", default="Dataset correlati"),
        description=_(
            "dataset_correlati_help",
            default="Seleziona una lista di schede dataset collegate a questo"
            " contenuto.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )
    form.widget(
        "dataset_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Dataset"],
            "maximumSelectionSize": 50,
        },
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["dataset_correlati"],
    )


@implementer(IDatasetCorrelati)
@adapter(IDexterityContent)
class DatasetCorrelati(object):
    """ """

    def __init__(self, context):
        self.context = context
