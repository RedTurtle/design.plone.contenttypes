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

    if value.latitude == 0.0 and value.longitude == 0.0:
        return None
    return value.__dict__
