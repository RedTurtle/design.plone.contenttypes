# -*- coding: utf-8 -*-
from plone.formwidget.geolocation.interfaces import IGeolocation
from plone.restapi.interfaces import IJsonCompatible
from zope.component import adapter
from zope.interface import implementer


@adapter(IGeolocation)
@implementer(IJsonCompatible)
def geolocation_converter(value):
    if value is None:
        return value

    return value.__dict__

    raise TypeError(
        "No converter for making"
        " {0!r} ({1}) JSON compatible.".format(value, type(value))
    )
