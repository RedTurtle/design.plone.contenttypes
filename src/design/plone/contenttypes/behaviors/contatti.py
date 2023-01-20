# -*- coding: utf-8 -*-
from collective.venue.interfaces import IVenue
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces.persona import IPersona
from design.plone.contenttypes.interfaces.servizio import IServizio
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IContattiUnitaOrganizzativa(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Punti di contatto dell'unità organizzativa",
        ),
        description=_(
            "contact_info_help",
            default="Contatti dell'unità organizzativa.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Informazioni di contatto"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "contact_info",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@provider(IFormFieldProvider)
class IContattiPersona(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Punti di contatto della persona.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Punti di contatto"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    form.widget(
        "contact_info",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@provider(IFormFieldProvider)
class IContattiServizio(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Contatti",
        ),
        description=_(
            "contact_info_help",
            default="I contatti per il servizio.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Contatti"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "contact_info",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@provider(IFormFieldProvider)
class IContattiVenue(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Telefono, mail o altri punti di contatto.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Punti di contatto"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "contact_info",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@provider(IFormFieldProvider)
class IContattiEvent(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Relazione con i punti di contatto dell'evento.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Punti di contatto"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "contact_info",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@implementer(IContattiEvent)
@adapter(IContattiEvent)
class ContattiEvent(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IContattiPersona)
@adapter(IPersona)
class ContattiPersona(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IContattiServizio)
@adapter(IServizio)
class ContattiServizio(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IContattiUnitaOrganizzativa)
@adapter(IUnitaOrganizzativa)
class ContattiUnitaOrganizzativa(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IContattiVenue)
@adapter(IVenue)
class ContattiVenue(object):
    """ """

    def __init__(self, context):
        self.context = context
