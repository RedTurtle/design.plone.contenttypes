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

    # TODO: vocabolario per le tipologie di notizie
    tipologia_notizia = schema.Choice(
        title=_("tipologia_notizia_label", default="Tipologia notizia"),
        description=_(
            "tipologia_notizia_help",
            default="Seleziona la tipologia della notizia.",
        ),
        required=True,
        vocabulary="design.plone.contenttypes.TipologiaNotizia",
    )

    # numero progressivo del cs se esiste. Numero o stringa?
    numero_progressivo_cs = schema.TextLine(
        title=_(
            "numero_progressivo_cs_label",
            default="Numero progressivo del comunicato stampa",
        ),
        required=False,
    )

    a_cura_di = RelationChoice(
        title=_("a_cura_di_label", default="A cura di"),
        description=_(
            "a_cura_di_help",
            default="Seleziona l'ufficio di comunicazione responsabile di "
            "questa notizia/comunicato stampa.",
        ),
        required=True,
        vocabulary="plone.app.vocabularies.Catalog",
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
            "selectableTypes": ["Unita organizzativa"],
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
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["News Item"],
        },
    )

    # custom fieldsets
    model.fieldset(
        "correlati",
        label=_("correlati_label", default=u"Correlati"),
        fields=["notizie_correlate"],
    )

    model.fieldset("categorization", fields=["tipologia_notizia"])
    model.fieldset("settings", fields=["numero_progressivo_cs"])


@implementer(INewsAdditionalFields)
@adapter(INewsItem)
class NewsAdditionalFields(object):
    """
    """

    def __init__(self, context):
        self.context = context
