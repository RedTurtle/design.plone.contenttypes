# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces.bando import IBandoAgidSchema
from design.plone.contenttypes.interfaces.documento import IDocumento
from plone.app.contenttypes.interfaces import IDocument
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.component import adapter
from zope.interface import provider, implementer


class IArgomentiSchema(model.Schema):
    """Marker interface for Argomenti"""

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
    correlato_in_evidenza = RelationList(
        title=_(
            "correlato_in_evidenza_label", default="Correlato in evidenza"
        ),
        description=_(
            "correlato_in_evidenza_help",
            default="Seleziona un correlato da mettere in evidenza per questo"
            " contenuto.",
        ),
        value_type=RelationChoice(
            title=_(u"Correlato in evidenza"),
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
    form.widget(
        "correlato_in_evidenza",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 1},
    )

    dexteritytextindexer.searchable("tassonomia_argomenti")


@provider(IFormFieldProvider)
class IArgomenti(IArgomentiSchema):
    """ """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["correlato_in_evidenza"],
    )
    form.order_after(correlato_in_evidenza="IRelatedItems.relatedItems")


@provider(IFormFieldProvider)
class IArgomentiDocumento(IArgomentiSchema):
    """ """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["correlato_in_evidenza"],
    )
    form.order_after(correlato_in_evidenza="IRelatedItems.relatedItems")
    form.order_after(tassonomia_argomenti="IDublinCore.title")


@provider(IFormFieldProvider)
class IArgomentiDocument(IArgomentiSchema):
    """ """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["correlato_in_evidenza"],
    )
    model.fieldset(
        "testata",
        label=_("testata_fieldset_label", default=u"Testata"),
        fields=["tassonomia_argomenti"],
    )
    form.order_after(correlato_in_evidenza="IRelatedItems.relatedItems")
    form.order_after(tassonomia_argomenti="IInfoTestata.mostra_navigazione")


@provider(IFormFieldProvider)
class IArgomentiBando(IArgomentiSchema):
    """ """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["tassonomia_argomenti", "correlato_in_evidenza"],
    )
    form.order_before(tassonomia_argomenti="IRelatedItems.relatedItems")
    form.order_after(correlato_in_evidenza="IRelatedItems.relatedItems")


@implementer(IArgomenti)
@adapter(IDexterityContent)
class Argomenti(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IArgomentiDocumento)
@adapter(IDocumento)
class ArgomentiDocumento(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IArgomentiBando)
@adapter(IBandoAgidSchema)
class ArgomentiBando(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IArgomentiDocument)
@adapter(IDocument)
class ArgomentiDocument(object):
    """"""

    def __init__(self, context):
        self.context = context
