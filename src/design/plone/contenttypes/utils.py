# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import (
    IDesignPloneSettings,
)
from plone import api

import logging
import json
import six


logger = logging.getLogger(__name__)


def get_settings_for_language(field):
    values = api.portal.get_registry_record(
        field, interface=IDesignPloneSettings, default=[]
    )
    if not isinstance(values, six.text_type):
        return values
    try:
        json_data = json.loads(values)
    except Exception as e:
        logger.exception(e)
        return values
    lang = api.portal.get_current_language()
    return json_data.get(lang, [])
