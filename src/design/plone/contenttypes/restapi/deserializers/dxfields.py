# -*- coding: utf-8 -*-
from datetime import datetime
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone.dexterity.interfaces import IDexterityContent
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.formwidget.geolocation.interfaces import IGeolocationField
from plone.restapi.deserializer.dxfields import CollectionFieldDeserializer
from plone.restapi.deserializer.dxfields import DefaultFieldDeserializer
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from plone.restapi.interfaces import IFieldDeserializer
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import subscribers
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.interfaces import IList
from zope.schema.interfaces import ISourceText

import json


KEYS_WITH_URL = ["linkUrl", "navigationRoot", "showMoreLink"]


@implementer(IFieldDeserializer)
@adapter(IGeolocationField, IDexterityContent, IDesignPloneContenttypesLayer)
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


@implementer(IFieldDeserializer)
@adapter(ISourceText, IDexterityContent, IDesignPloneContenttypesLayer)
class SourceTextDeserializer(DefaultFieldDeserializer):
    def __call__(self, value):
        value = super(SourceTextDeserializer, self).__call__(value)
        if self.field.getName() == "search_sections":
            #  per ora solo con questo, ma potenzialmente con altri simili
            data = json.loads(value)
            for root in data:
                if not root:
                    continue
                for tab in root.get("items", []):
                    for key in KEYS_WITH_URL:
                        url = tab.get(key, [])
                        if url:
                            tab[key] = [
                                x.get("UID", "") for x in url if x.get("UID", "")
                            ]
                    blocks = tab.get("blocks", {})
                    if blocks:
                        for id, block_value in blocks.items():
                            block_type = block_value.get("@type", "")
                            handlers = []
                            for h in subscribers(
                                (self.context, self.request),
                                IBlockFieldDeserializationTransformer,
                            ):
                                if (
                                    h.block_type == block_type
                                    or h.block_type is None  # noqa
                                ):
                                    handlers.append(h)
                            for handler in sorted(handlers, key=lambda h: h.order):
                                block_value = handler(block_value)

                            blocks[id] = block_value
            value = json.dumps(data)
        return value


@implementer(IFieldDeserializer)
@adapter(IList, IServizio, IDesignPloneContenttypesLayer)
class TimelineTempiEScadenzeFieldDeserializer(CollectionFieldDeserializer):
    """
    Volto returns a string in date field, Plone expects <class datetime.date>
    and throws error during validation. Patched.
    Since I cannot have an empty value in data_scadenza (which is NOT a required
    field), I'll have to do some serializing magic in Servizio serializer.
    Also validate milestone field, frontend should take care of it, but you never know.
    """

    def __call__(self, value):
        if self.field.getName() != "timeline_tempi_scadenze" or not value:
            return super().__call__(value)

        timeline = []
        for item in value:
            if not item.get("milestone", None):
                raise BadRequest(
                    {
                        "error": "ValidationError",
                        "message": "Il campo {} è obbligatorio".format(
                            "Titolo della fase"
                        ),
                    }
                )

            entry = {
                "milestone": item.get("milestone", ""),
                "milestone_description": item.get("milestone_description", ""),
                "interval_qt": item.get("interval_qt", ""),
                "interval_type": item.get("interval_type", ""),
                "data_scadenza": datetime.strptime(
                    item["data_scadenza"], "%Y-%m-%d"
                ).date()
                if item.get("data_scadenza", None)
                else None,  # noqa
            }

            timeline.append(entry)

        self.field.validate(timeline)
        return timeline
