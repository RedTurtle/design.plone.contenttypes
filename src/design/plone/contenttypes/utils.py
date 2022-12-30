# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from plone import api
from uuid import uuid4

import json
import logging
import six


logger = logging.getLogger(__name__)


def get_settings_for_language(field):
    values = api.portal.get_registry_record(
        field, interface=IDesignPloneSettings, default=[]
    )
    if not values:
        return []
    if not isinstance(values, six.text_type):
        return values
    try:
        json_data = json.loads(values)
    except Exception as e:
        logger.exception(e)
        return values
    lang = api.portal.get_current_language()
    return json_data.get(lang, [])


def create_default_blocks(context):
    title_uuid = str(uuid4())
    context.blocks = {title_uuid: {"@type": "title"}}
    context.blocks_layout = {"items": [title_uuid]}
