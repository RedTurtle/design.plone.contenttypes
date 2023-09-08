# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IDocumentoBehavior(model.Schema):
    ufficio_responsabile = RelationList(
        title=_(
            "ufficio_responsabile_documento_label",
            default="Ufficio responsabile del documento",
        ),
        description=_(
            "ufficio_responsabile_documento_help",
            default="Seleziona l'ufficio responsabile di questo documento.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    protocollo = schema.TextLine(
        title=_(
            "protocollo_documento_label",
            default="Numero di protocollo",
        ),
        description=_(
            "protocollo_documento_help",
            default="Il numero di protocollo del documento.",
        ),
        max_length=255,
        required=False,
    )
    data_protocollo = schema.Date(
        title=_("data_protocollo", default="Data del protocollo"),
        required=False,
    )

    formati_disponibili = BlocksField(
        title=_("formati_disponibili_label", default="Formati disponibili"),
        description=_(
            "formati_disponibili_help",
            default="Lista dei formati in cui è disponibile il documento",
        ),
        required=True,
    )

    form.order_after(
        ufficio_responsabile="IDescrizioneEstesaDocumento.descrizione_estesa"
    )
    form.order_after(formati_disponibili="identificativo")
    form.order_after(data_protocollo="identificativo")
    form.order_after(protocollo="identificativo")

    form.widget(
        "ufficio_responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    #  custom fieldsets
    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default="Descrizione"),
        fields=[
            "ufficio_responsabile",
        ],
    )


@implementer(IDocumentoBehavior)
@adapter(IDexterityContent)
class DocumentoBehavior(object):
    """ """

    def __init__(self, context):
        self.context = context
