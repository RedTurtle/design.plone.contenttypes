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

from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.restapi.batching import HypermediaBatch
from plone.restapi.deserializer import boolean_value
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.i18n import translate


original_serialize_to_json__call__ = SerializeToJson.__call__


def design_italia_serialize_to_json_call(self, version=None, include_items=True):
    ttool = api.portal.get_tool("portal_types")
    result = original_serialize_to_json__call__(
        self, version=version, include_items=include_items
    )
    result["design_italia_meta_type"] = translate(
        ttool[self.context.portal_type].Title(), context=self.request
    )
    if self.context.portal_type == "News Item":
        tipologia_notizia = getattr(self.context, "tipologia_notizia", "")
        if tipologia_notizia:
            taxonomy = queryUtility(
                ITaxonomy, name="collective.taxonomy.tipologia_notizia"
            )
            if taxonomy:
                taxonomy_voc = taxonomy.makeVocabulary(self.request.get("LANGUAGE"))

                title = taxonomy_voc.inv_data.get(self.context.tipologia_notizia, None)
                if title and title.startswith(PATH_SEPARATOR):
                    result["design_italia_meta_type"] = title.replace(
                        PATH_SEPARATOR, "", 1
                    )
            else:
                result["design_italia_meta_type"] = tipologia_notizia
    return result


def patch_base_serializer():
    SerializeToJson.__call__ = design_italia_serialize_to_json_call


def design_italia_serialize_folder_to_json_call(self, version=None, include_items=True):
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
            result["items"] = getMultiAdapter((brains, self.request), ISerializeToJson)(
                fullobjects=True
            )["items"]
        else:
            result["items"] = [
                getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
                for brain in batch
            ]
    return result


def patch_base_folder_serializer():
    SerializeFolderToJson.__call__ = design_italia_serialize_folder_to_json_call
