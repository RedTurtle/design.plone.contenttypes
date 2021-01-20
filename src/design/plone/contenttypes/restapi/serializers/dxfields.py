# -*- coding: utf-8 -*-
from design.plone.contenttypes.fields import IBlocksField
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import DefaultFieldSerializer
from zope.component import adapter
from zope.component import subscribers
from zope.interface import implementer
from zope.interface import Interface

import copy


@adapter(IBlocksField, IDexterityContent, Interface)
@implementer(IFieldSerializer)
class BlocksFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        value = copy.deepcopy(self.get_value())
        if not value:
            return {}
        blocks = value.get("blocks", {})
        if blocks:
            for id, block_value in blocks.items():
                block_type = block_value.get("@type", "")
                handlers = []
                for h in subscribers(
                    (self.context, self.request),
                    IBlockFieldSerializationTransformer,
                ):
                    if h.block_type == block_type or h.block_type is None:
                        handlers.append(h)

                for handler in sorted(handlers, key=lambda h: h.order):
                    if not getattr(handler, "disabled", False):
                        block_value = handler(block_value)

                blocks[id] = block_value

        return json_compatible(value)
