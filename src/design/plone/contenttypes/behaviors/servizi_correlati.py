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
class IServiziCorrelati(model.Schema):

    servizi_correlati = RelationList(
        title=_("servizi_correlati_label", default="Servizi correlati"),
        description=_(
            "servizi_correlati_description",
            default="Questi servizi non verranno mostrati nel contenuto, ma"
            " permetteranno di vedere questo contenuto associato quando si"
            " visita il servizio",
        ),
        default=[],
        value_type=RelationChoice(
            title="Related", vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )
    form.widget(
        "servizi_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Servizio"],
        },
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["servizi_correlati"],
    )
    form.order_before(servizi_correlati="IRelatedItems.relatedItems")


@implementer(IServiziCorrelati)
@adapter(IDexterityContent)
class ServiziCorrelati(object):
    """"""

    def __init__(self, context):
        self.context = context
