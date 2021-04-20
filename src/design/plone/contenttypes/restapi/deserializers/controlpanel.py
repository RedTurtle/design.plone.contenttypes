# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import (
    IDesignPloneSettingsControlpanel,
)
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import (
    ControlpanelDeserializeFromJson,
)
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(IDeserializeFromJson)
@adapter(IDesignPloneSettingsControlpanel)
class DesignPloneControlPanelSerializeFromJson(
    ControlpanelDeserializeFromJson
):
    def __call__(self):
        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(
            self.schema, prefix=self.schema_prefix
        )
        errors = []
        fields = [
            "tipologie_notizia",
            "tipologie_unita_organizzativa",
            "tipologie_documento",
            "tipologie_persona",
        ]
        for field in fields:
            data = req.get(field, {})
            if not data:
                errors.append({"message": "Missing data", "field": field})
                raise BadRequest(errors)
            try:
                value = json.loads(data)
                setattr(proxy, field, json.dumps(value))
            except ValueError as e:
                errors.append({"message": str(e), "field": field, "error": e})

        if errors:
            raise BadRequest(errors)
