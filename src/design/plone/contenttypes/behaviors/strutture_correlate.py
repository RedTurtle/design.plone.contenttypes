# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class IStruttureCorrelate(model.Schema):

    strutture_politiche = RelationList(
        title=u"Strutture politiche coinvolte",
        default=[],
        value_type=RelationChoice(
            title=_(u"Struttura politica coinvolta"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        missing_value=(),
        description=_(
            "strutture_politiche_help",
            default="Seleziona la lista delle strutture politiche coinvolte.",
        ),
    )
    form.widget(
        "strutture_politiche",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    model.fieldset(
        "informazioni",
        label=_("informazioni_label", default=u"Ulteriori informazioni"),
        fields=["strutture_politiche"],
    )


@implementer(IStruttureCorrelate)
@adapter(IDexterityContent)
class StruttureCorrelate(object):
    """
    """

    def __init__(self, context):
        self.context = context
