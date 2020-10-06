# -*- coding: utf-8 -*-
from collective.geolocationbehavior.geolocation import IGeolocatable
from collective.venue.interfaces import IVenue
from design.plone.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import provider, implementer
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)


@provider(IFormFieldProvider)
class IGeolocatableUnitaOrganizzativa(IGeolocatable):

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["geolocation"],
    )


@provider(IFormFieldProvider)
class IGeolocatableVenue(IGeolocatable):

    model.fieldset(
        "dove", label=_("dove_label", default=u"Dove"), fields=["geolocation"]
    )


@provider(IFormFieldProvider)
class IGeolocatableEvent(IGeolocatable):

    model.fieldset(
        "luogo",
        label=_("luogo_label", default=u"Luogo"),
        fields=["geolocation"],
    )


@implementer(IGeolocatableUnitaOrganizzativa)
@adapter(IUnitaOrganizzativa)
class GeolocatableUnitaOrganizzativa(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(IGeolocatableVenue)
@adapter(IVenue)
class GeolocatableVenue(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(IGeolocatableEvent)
@adapter(IDexterityContent)
class GeolocatableEvent(object):
    """
    """

    def __init__(self, context):
        self.context = context
