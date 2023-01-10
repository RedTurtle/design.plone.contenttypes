# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.app.contenttypes.interfaces import INewsItem
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class INewsAdditionalFields(model.Schema):
    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=True,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
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
        required=True,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    a_cura_di_persone = RelationList(
        title=_("a_cura_di_persone_label", default="Persone"),
        description=_(
            "a_cura_di_persone_help",
            default="Seleziona una lista di persone dell'amministrazione "
            "citate in questa notizia/comunicato stampa. Questa informazione "
            'verrà mostrata nella sezione "A cura di".',
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
            "selectableTypes": ["Persona"],
            "maximumSelectionSize": 50,
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
            "selectableTypes": ["Venue"],
            "maximumSelectionSize": 50,
        },
    )

    # custom fieldsets and order
    form.order_before(descrizione_estesa="ILeadImageBehavior.image")
    form.order_before(numero_progressivo_cs="ILeadImageBehavior.image")
    form.order_before(a_cura_di="ILeadImageBehavior.image")

    textindexer.searchable("descrizione_estesa")


@implementer(INewsAdditionalFields)
@adapter(INewsItem)
class NewsAdditionalFields(object):
    """ """

    def __init__(self, context):
        self.context = context
