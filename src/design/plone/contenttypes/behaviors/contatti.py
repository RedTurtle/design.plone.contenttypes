# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.venue.interfaces import IVenue
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)


class IContatti(model.Schema):
    """
    """

    telefono = schema.TextLine(
        title=_(u"telefono_label", default=u"Telefono"),
        description=_(
            u"telefono_help",
            default=u"Indicare un riferimento telefonico per poter contattare"
            " i referenti.",
        ),
        required=False,
    )

    fax = schema.TextLine(
        title=_(u"fax_label", default=u"Fax"),
        description=_(u"fax_help", default=u"Indicare un numero di fax."),
        required=False,
    )

    email = schema.TextLine(
        title=_(u"email_label", default=u"E-mail"),
        description=_(
            u"email_help",
            default=u"Indicare un indirizzo mail per poter contattare"
            " i referenti.",
        ),
        required=False,
    )

    pec = schema.TextLine(
        title=_(u"pec_label", default=u"Pec"),
        description=_(
            u"pec_help",
            default=u"Indicare un indirizzo pec per poter contattare"
            " i referenti.",
        ),
        required=False,
    )

    web = schema.TextLine(
        title=_(u"web_label", default=u"Sito web"),
        description=_(
            "web_help", default="Indicare un indirizzo web di riferimento."
        ),
        required=False,
    )

    orario_pubblico = RichText(
        title=_(u"orario_pubblico_label", default=u"Orario per il pubblico"),
        description=_(
            u"orario_pubblico_help",
            default=u"Indicare eventuali orari di accesso al pubblico",
        ),
        required=False,
    )

    dexteritytextindexer.searchable("orario_pubblico")


@provider(IFormFieldProvider)
class IContattiUnitaOrganizzativa(IContatti):
    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=["telefono", "fax", "email", "pec", "web", "orario_pubblico"],
    )


@provider(IFormFieldProvider)
class IContattiVenue(IContatti):

    model.fieldset(
        "orari",
        label=_("orari_label", default=u"Orari di apertura"),
        fields=["orario_pubblico"],
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default=u"Contatti"),
        fields=["telefono", "fax", "email", "pec", "web"],
    )


@implementer(IContattiUnitaOrganizzativa)
@adapter(IUnitaOrganizzativa)
class ContattiUnitaOrganizzativa(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(IContattiVenue)
@adapter(IVenue)
class ContattiVenue(object):
    """
    """

    def __init__(self, context):
        self.context = context
