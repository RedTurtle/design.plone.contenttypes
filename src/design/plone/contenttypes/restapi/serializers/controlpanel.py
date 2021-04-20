# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import (
    IDesignPloneSettingsControlpanel,
)
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(ISerializeToJson)
@adapter(IDesignPloneSettingsControlpanel)
class DesignPloneControlPanelSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super(
            DesignPloneControlPanelSerializeToJson, self
        ).__call__()
        # convert fields
        fields = [
            "tipologie_notizia",
            "tipologie_unita_organizzativa",
            "tipologie_documento",
            "tipologie_persona",
        ]
        for field in fields:
            conf = json_data["data"].get(field, "")
            if conf:
                json_data["data"][field] = json.loads(conf)
        return json_data
