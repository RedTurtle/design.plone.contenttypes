# -*- coding: utf-8 -*-
"""
We need a solution like that because for some different reasons:
 * we have to customize both SerializeToJson and SerializeFolderToJson
 * If we override SerializeToJson adding this base design_italia_meta_type
   information, we need to override SerializeFolderToJson copying the whole
   code otherwise it will use the code from original SerializeToJson due to
   inheritance
 * Using a monkey patch is the easiest way to include future changes on base
   SerializeToJson and SerializeFolderToJson classes
"""

from plone.restapi.serializer.dxcontent import SerializeToJson
from plone import api
from zope.i18n import translate
from design.plone.contenttypes import _

original_serialize_to_json__call__ = SerializeToJson.__call__


def design_italia_serialize_to_json_call(
    self, version=None, include_items=True
):
    ttool = api.portal.get_tool("portal_types")
    result = original_serialize_to_json__call__(
        self, version=None, include_items=True
    )
    if self.context.portal_type == "News Item":
        result["design_italia_meta_type"] = translate(
            self.context.tipologia_notizia,
            domain=_._domain,
            context=self.request,
        )
    else:
        result["design_italia_meta_type"] = translate(
            ttool[self.context.portal_type].Title(), context=self.request
        )

    return result


def patch_base_serializer():
    SerializeToJson.__call__ = design_italia_serialize_to_json_call
