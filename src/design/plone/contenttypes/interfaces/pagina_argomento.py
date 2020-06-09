# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IPaginaArgomento(model.Schema):
    """ Marker interface for PaginaArgomento
    """

    tassonomia_argomenti = schema.Choice(
        title=_(u"tassonomia_argomenti", default=u"Tassonomia argomenti"),
        description=_(
            u"tassonomia_description",
            default=u"Scegli l'argomento di riferimento; utile per capire a quali elementi del sito questo argomento è collegato",  # noqa
        ),
        vocabulary="design.plone.contenttypes.TagsVocabulary",
        required=True,
    )

    area_appartenenza = RelationList(
        title=_(u"area_di_appartenenza", default=u"Area di appartenenza"),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_(u"Area di appartenenza"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "area_appartenenza",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione/aree-amministrative",
        },
    )

    assessorati_riferimento = RelationList(
        title=_(
            u"assessorati_riferimento", default=u"Assessorati di riferimento"
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_(u"Assessorati di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "assessorati_riferimento",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"), required=True
    )

    # TODO: come gestire "in primo piano", "servizi", "novita'", "documenti",
    # "amministrazione"?
