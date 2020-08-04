# -*- coding: utf-8 -*-
from plone.formwidget.geolocation.interfaces import IGeolocationField
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IFieldDeserializer
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.restapi.deserializer.dxfields import DefaultFieldDeserializer
from plone.formwidget.geolocation.geolocation import Geolocation
from design.plone.contenttypes import _
from zope.i18n import translate


@implementer(IFieldDeserializer)
@adapter(IGeolocationField, IDexterityContent, IBrowserRequest)
class GeolocationFieldDeserializer(DefaultFieldDeserializer):
    def __call__(self, value):
        if "latitude" not in value or "longitude" not in value:
            raise ValueError(
                translate(
                    _(
                        "geolocation_field_validator_label",
                        default="Invalid geolocation data: ${value}. Provide latitude and longitude coordinates.",  # noqa
                        mapping={"value": value},
                    ),
                    context=self.request,
                )
            )
        return Geolocation(latitude=value["latitude"], longitude=value["longitude"])
