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
from design.plone.contenttypes.fields import IBlocksField
from zope.component import subscribers
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer


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
        return Geolocation(
            latitude=value["latitude"], longitude=value["longitude"]
        )


@implementer(IFieldDeserializer)
@adapter(IBlocksField, IDexterityContent, IBrowserRequest)
class BlocksFieldDeserializer(DefaultFieldDeserializer):
    def __call__(self, value):
        value = super(BlocksFieldDeserializer, self).__call__(value)
        blocks = value.get("blocks", {})
        if blocks:
            for id, block_value in blocks.items():
                block_type = block_value.get("@type", "")
                handlers = []
                for h in subscribers(
                    (self.context, self.request),
                    IBlockFieldDeserializationTransformer,
                ):
                    if h.block_type == block_type or h.block_type is None:
                        handlers.append(h)
                for handler in sorted(handlers, key=lambda h: h.order):
                    if not getattr(handler, "disabled", False):
                        block_value = handler(block_value)

                blocks[id] = block_value
        return value
