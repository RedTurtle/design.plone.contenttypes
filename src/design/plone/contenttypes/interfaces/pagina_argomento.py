# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


class IPaginaArgomento(model.Schema):
    """ Marker interface for PaginaArgomento
    """

    area_appartenenza = RelationList(
        title=_(u"area_di_appartenenza", default=u"Area di appartenenza"),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Area di appartenenza"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "area_appartenenza_help",
            default="Seleziona la lista delle aree amministrative collegate"
            " a questo argomento.",
        ),
    )
    form.widget(
        "area_appartenenza",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione/aree-amministrative",
        },
    )

    assessorati_riferimento = RelationList(
        title=_(
            u"assessorati_riferimento", default=u"Assessorati di riferimento"
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Assessorati di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "assessorati_riferimento_help",
            default="Seleziona la lista degli assessorati di riferimento"
            " per questo argomento.",
        ),
    )
    form.widget(
        "assessorati_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"),
        required=False,
        description=_(
            "box_aiuto_help",
            default="Eventuali contatti di supporto all'utente.",
        ),
    )
