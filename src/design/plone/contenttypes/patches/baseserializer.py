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

from plone.restapi.serializer.dxcontent import (
    SerializeToJson,
    SerializeFolderToJson,
)
from plone import api
from plone.restapi.batching import HypermediaBatch
from plone.restapi.deserializer import boolean_value
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18n import translate
from design.plone.contenttypes import _

original_serialize_to_json__call__ = SerializeToJson.__call__


def design_italia_serialize_to_json_call(
    self, version=None, include_items=True
):
    ttool = api.portal.get_tool("portal_types")
    result = original_serialize_to_json__call__(
        self, version=version, include_items=include_items
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


def design_italia_serialize_folder_to_json_call(
    self, version=None, include_items=True
):
    folder_metadata = super(SerializeFolderToJson, self).__call__(
        version=version, include_items=include_items
    )

    folder_metadata.update({"is_folderish": True})
    result = folder_metadata
    include_items = self.request.form.get("include_items", include_items)
    include_items = boolean_value(include_items)
    if include_items:
        query = self._build_query()

        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(query)

        batch = HypermediaBatch(self.request, brains)

        # These lines generate wrong result in field @id of the returned items
        # if "fullobjects" not in self.request.form:
        #   result["@id"] = batch.canonical_url
        result["items_total"] = batch.items_total
        if batch.links:
            result["batching"] = batch.links
        if "fullobjects" in list(self.request.form):
            result["items"] = getMultiAdapter(
                (brains, self.request), ISerializeToJson
            )(fullobjects=True)["items"]
        else:
            result["items"] = [
                getMultiAdapter(
                    (brain, self.request), ISerializeToJsonSummary
                )()
                for brain in batch
            ]
    return result


def patch_base_folder_serializer():
    SerializeFolderToJson.__call__ = (
        design_italia_serialize_folder_to_json_call
    )
