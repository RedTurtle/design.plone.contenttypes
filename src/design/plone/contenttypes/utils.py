# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from plone import api
from plone.restapi.behaviors import IBlocks
from uuid import uuid4
from zope.interface import implementer

import json
import logging
import six


HAVE_REST_API_PRE_961 = False

try:
    # plone 6.0.11 with last plone.restapi>9.6.0
    from plone.restapi.indexers import get_blocks_text
    from plone.restapi.indexers import text_strip

except ImportError:
    # plone 6.0.10.1 with plone.restapi<9.6.1
    HAVE_REST_API_PRE_961 = True
    from plone.restapi.indexers import SearchableText_blocks


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


def text_in_block(blocks):
    @implementer(IBlocks)
    class FakeObject(object):
        """
        We use a fake object to use SearchableText Indexer
        """

        def Subject(self):
            return ""

        def __init__(self, blocks, blocks_layout):
            self.blocks = blocks
            self.blocks_layout = blocks_layout
            self.id = ""
            self.title = ""
            self.description = ""

    if not blocks:
        return None

    fakeObj = FakeObject(blocks.get("blocks", ""), blocks.get("blocks_layout", ""))

    if HAVE_REST_API_PRE_961:
        return SearchableText_blocks(fakeObj)()
    else:
        blocks_text = get_blocks_text(fakeObj)
        return text_strip(blocks_text)
