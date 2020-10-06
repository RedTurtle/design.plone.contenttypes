# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.contenttypes.interfaces import INewsItem
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class INewsAdditionalFields(model.Schema):

    tipologia_notizia = schema.Choice(
        title=_("tipologia_notizia_label", default="Tipologia notizia"),
        description=_(
            "tipologia_notizia_help",
            default="Seleziona la tipologia della notizia.",
        ),
        required=True,
        vocabulary="design.plone.vocabularies.tipologie_notizia",
    )

    numero_progressivo_cs = schema.TextLine(
        title=_(
            "numero_progressivo_cs_label",
            default="Numero progressivo del comunicato stampa",
        ),
        required=False,
    )

    a_cura_di = RelationList(
        title=_("a_cura_di_label", default="A cura di"),
        description=_(
            "a_cura_di_help",
            default="Seleziona l'ufficio di comunicazione responsabile di "
            "questa notizia/comunicato stampa.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    a_cura_di_persone = RelationList(
        title=_("a_cura_di_persone_label", default="Persone"),
        description=_(
            "a_cura_di_persone_help",
            default="Seleziona una lista di persone dell'amministrazione "
            "citate in questa notizia/comunicato stampa.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    luoghi_correlati = RelationList(
        title=_("luoghi_correlati_label", default="Luoghi correlati"),
        description=_(
            "luoghi_correlati_help",
            default="Seleziona una lista di luoghi citati.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    notizie_correlate = RelationList(
        title=_("notizie_correlate_label", default="Notizie correlate"),
        description=_(
            "notizie_correlate_help",
            default="Seleziona una lista di notizie correlate a questa.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    # custom widgets
    form.widget(
        "a_cura_di",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "a_cura_di_persone",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "recentlyUsed": True,  # Just turn on. Config in plone.app.widgets.
            "selectableTypes": ["Persona"],
        },
    )
    form.widget(
        "notizie_correlate",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["News Item"],
        },
    )
    form.widget(
        "luoghi_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "recentlyUsed": True,  # Just turn on. Config in plone.app.widgets.
            "selectableTypes": ["Venue"],
        },
    )

    # custom fieldsets and order
    form.order_before(tipologia_notizia="ILeadImageBehavior.image")
    form.order_before(numero_progressivo_cs="ILeadImageBehavior.image")
    form.order_before(a_cura_di="ILeadImageBehavior.image")


@implementer(INewsAdditionalFields)
@adapter(INewsItem)
class NewsAdditionalFields(object):
    """
    """

    def __init__(self, context):
        self.context = context
