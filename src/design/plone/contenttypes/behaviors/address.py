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


class IAddressNomeSede(model.Schema):
    nome_sede = schema.TextLine(
        title=_("nome_sede", default="Nome sede"),
        description=_(
            "help_nome_sede",
            default="Inserisci il nome della "
            "sede, se non è presente tra i Luoghi del sito.",
        ),
        required=False,
    )


class IAddressLocal(model.Schema):
    """
    """

    quartiere = schema.TextLine(
        title=_("quartiere", default="Quartiere"),
        description=_("help_quartiere", default=""),
        required=False,
    )

    circoscrizione = schema.TextLine(
        title=_("circoscrizione", default="Circoscrizione"),
        description=_("help_circoscrizione", default=""),
        required=False,
    )

    # searchabletext indexer
    dexteritytextindexer.searchable("quartiere")
    dexteritytextindexer.searchable("circoscrizione")


@provider(IFormFieldProvider)
class IAddressUnitaOrganizzativa(IAddress, IAddressNomeSede, IAddressLocal):

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "nome_sede",
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
        label=_("dove_label", default="Dove"),
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
class IAddressEvent(IAddress, IAddressNomeSede, IAddressLocal):
    """"""

    model.fieldset(
        "luogo",
        label=_("luogo_label", default="Luogo"),
        fields=[
            "nome_sede",
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
