# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.venue.interfaces import IVenue
from design.plone.contenttypes import _
from collective.volto.blocksfield.field import BlocksField
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa


class IContatti(model.Schema):
    """ """

    telefono = schema.TextLine(
        title=_("telefono_label", default="Telefono"),
        description=_(
            "telefono_help",
            default="Indicare un riferimento telefonico per poter contattare"
            " i referenti.",
        ),
        required=False,
    )

    fax = schema.TextLine(
        title=_("fax_label", default="Fax"),
        description=_("fax_help", default="Indicare un numero di fax."),
        required=False,
    )

    email = schema.TextLine(
        title=_("email_label", default="E-mail"),
        description=_(
            "email_help",
            default="Indicare un indirizzo mail per poter contattare" " i referenti.",
        ),
        required=False,
    )

    pec = schema.TextLine(
        title=_("pec_label", default="Pec"),
        description=_(
            "pec_help",
            default="Indicare un indirizzo pec per poter contattare" " i referenti.",
        ),
        required=False,
    )

    web = schema.TextLine(
        title=_("web_label", default="Sito web"),
        description=_("web_help", default="Indicare un indirizzo web di riferimento."),
        required=False,
    )

    orario_pubblico = BlocksField(
        title=_("orario_pubblico_label", default="Orario per il pubblico"),
        description=_(
            "orario_pubblico_help",
            default="Indicare eventuali orari di accesso al pubblico",
        ),
        required=False,
    )

    dexteritytextindexer.searchable("orario_pubblico")
    dexteritytextindexer.searchable("email")
    dexteritytextindexer.searchable("pec")
    dexteritytextindexer.searchable("web")


@provider(IFormFieldProvider)
class IContattiUnitaOrganizzativa(IContatti):
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["telefono", "fax", "email", "pec", "web", "orario_pubblico"],
    )


@provider(IFormFieldProvider)
class IContattiVenue(IContatti):
    model.fieldset(
        "orari",
        label=_("orari_label", default="Orari di apertura"),
        fields=["orario_pubblico"],
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["telefono", "fax", "email", "pec", "web"],
    )


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
