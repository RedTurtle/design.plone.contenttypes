# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from Acquisition import aq_inner
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone import api
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.base.utils import human_readable_size
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import INamedFileField
from plone.outputfilters.browser.resolveuid import uuidToURL
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import DefaultFieldSerializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import subscribers
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IList
from zope.schema.interfaces import ISourceText
from zope.schema.interfaces import ITextLine

import json
import re


RESOLVEUID_RE = re.compile(".*?/resolve[Uu]id/([^/]*)/?(.*)$")
KEYS_WITH_URL = ["linkUrl", "navigationRoot", "showMoreLink"]


@implementer(IFieldSerializer)
@adapter(ISourceText, IDexterityContent, IDesignPloneContenttypesLayer)
class SourceTextSerializer(DefaultFieldSerializer):
    def __call__(self):
        value = super(SourceTextSerializer, self).__call__()
        if self.field.getName() == "search_sections":
            return json.dumps(serialize_data(context=self.context, json_data=value))
        return value


@implementer(IFieldSerializer)
@adapter(IList, IServizio, IDesignPloneContenttypesLayer)
class TempiEScadenzeValueSerializer(DefaultFieldSerializer):
    def __call__(self):
        value = super(TempiEScadenzeValueSerializer, self).__call__()

        patched_timeline = []
        if self.field.getName() == "timeline_tempi_scadenze" and value:
            for entry in value:
                patched_timeline.append(entry)
            return json_compatible(patched_timeline)
        return value


@adapter(INamedFileField, IDexterityContent, IDesignPloneContenttypesLayer)
class FileFieldViewModeSerializer(DefaultFieldSerializer):
    """
    Ovveride the basic DX serializer to:
        - handle the visualize file functionality
        - add getObjSize info
    """

    def __call__(self):
        namedfile = self.field.get(self.context)
        if namedfile is None:
            return

        url = "/".join(
            (
                self.context.absolute_url(),
                self.get_file_view_mode(namedfile.contentType),
                self.field.__name__,
            )
        )
        size = namedfile.getSize()
        result = {
            "filename": namedfile.filename,
            "content-type": namedfile.contentType,
            "size": size,
            "getObjSize": human_readable_size(size),
            "download": url,
        }

        return json_compatible(result)

    def get_file_view_mode(self, content_type):
        """Pdf view depends on the visualize_files property in thq aq_chain"""
        if self.context and "pdf" in content_type:
            if getattr(aq_inner(self.context), "visualize_files", None):
                return "@@display-file"

        return "@@download"


def serialize_data(context, json_data, show_children=False):
    request = getRequest()
    if not json_data:
        return ""
    data = json.loads(json_data)
    for root in data:
        for tab in root.get("items", []):
            for key in KEYS_WITH_URL:
                value = tab.get(key, [])
                if value:
                    serialized = []
                    for uid in value:
                        try:
                            item = api.content.get(UID=uid)
                        except Unauthorized:
                            # private item and user can't see it
                            continue
                        if not item:
                            continue
                        summary = getMultiAdapter(
                            (item, request), ISerializeToJsonSummary
                        )()
                        if summary:
                            # serializer doesn't return uid
                            summary["UID"] = uid
                            if show_children:
                                summary["items"] = get_item_children(item)
                            serialized.append(summary)
                    tab[key] = serialized
            fix_blocks(context=context, tab=tab)
    return json_compatible(data)


def fix_blocks(context, tab):
    request = getRequest()
    blocks = tab.get("blocks", {})
    if blocks:
        for id, block_value in blocks.items():
            block_type = block_value.get("@type", "")
            handlers = []
            for h in subscribers(
                (context, request),
                IBlockFieldSerializationTransformer,
            ):
                if h.block_type == block_type or h.block_type is None:
                    handlers.append(h)
            for handler in sorted(handlers, key=lambda h: h.order):
                block_value = handler(block_value)

            blocks[id] = block_value


def get_item_children(item):
    path = "/".join(item.getPhysicalPath())
    query = {
        "path": {"depth": 1, "query": path},
        "sort_on": "getObjPositionInParent",
        "exclude_from_nav": False,
    }
    brains = api.content.find(**query)
    return [
        getMultiAdapter((brain, getRequest()), ISerializeToJsonSummary)()
        for brain in brains
    ]


@adapter(ITextLine, IServizio, IDesignPloneContenttypesLayer)
class ServizioTextLineFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        value = self.get_value()
        if self.field.getName() != "canale_digitale_link" or not value:
            return super().__call__()

        path = replace_link_variables_by_paths(context=self.context, url=value)
        match = RESOLVEUID_RE.match(path)
        if match:
            uid, suffix = match.groups()
            value = uuidToURL(uid)
        else:
            portal = getMultiAdapter(
                (self.context, self.context.REQUEST), name="plone_portal_state"
            ).portal()
            ref_obj = portal.restrictedTraverse(path, None)
            if ref_obj:
                value = ref_obj.absolute_url()

        return json_compatible(value)
