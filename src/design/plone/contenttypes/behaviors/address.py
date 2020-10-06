# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.address.behaviors import IAddress
from plone.dexterity.interfaces import IDexterityContent
from design.plone.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope import schema
from zope.interface import provider, implementer
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)


class IAddressLocal(model.Schema):
    """
    """

    quartiere = schema.TextLine(
        title=_(u"quartiere", default=u"Quartiere"),
        description=_(u"help_quartiere", default=u""),
        required=False,
    )

    circoscrizione = schema.TextLine(
        title=_(u"circoscrizione", default=u"Circoscrizione"),
        description=_(u"help_circoscrizione", default=u""),
        required=False,
    )

    # searchabletext indexer
    dexteritytextindexer.searchable("quartiere")
    dexteritytextindexer.searchable("circoscrizione")


@provider(IFormFieldProvider)
class IAddressUnitaOrganizzativa(IAddress, IAddressLocal):

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
        ],
    )


@provider(IFormFieldProvider)
class IAddressVenue(IAddress, IAddressLocal):
    """"""

    model.fieldset(
        "dove",
        label=_("dove_label", default=u"Dove"),
        fields=[
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
        ],
    )


@provider(IFormFieldProvider)
class IAddressEvent(IAddress, IAddressLocal):
    """"""

    model.fieldset(
        "luogo",
        label=_("luogo_label", default=u"Luogo"),
        fields=[
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
        ],
    )


@implementer(IAddressUnitaOrganizzativa)
@adapter(IUnitaOrganizzativa)
class AddressUnitaOrganizzativa(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(IAddressVenue)
@adapter(IDexterityContent)
class AddressVenue(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(IAddressEvent)
@adapter(IDexterityContent)
class AddressEvent(object):
    """
    """

    def __init__(self, context):
        self.context = context
