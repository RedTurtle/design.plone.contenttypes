from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.types.utils import get_info_for_type
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

import logging


logger = logging.getLogger(__name__)


@implementer(IBlockFieldSerializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class SearchTableVariationBlockSerialize:
    order = 100
    block_type = "search"
    value_field = "listingBodyTemplate"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _get_schema(self, portal_type):
        dtool = queryMultiAdapter(
            (api.portal.get(), self.request), name="dexterity-types"
        )
        try:
            dtype = dtool.publishTraverse(self.request, portal_type)
        except KeyError:
            logger.warning(f"KeyError: portal_type '{portal_type}' not found.")
            return None
        schema = get_info_for_type(dtype, self.request, portal_type)
        return schema

    def __call__(self, value):
        schemas = {}
        if value.get(self.value_field) == "table":
            for col in value.get("columns") or []:
                if not col.get("ct") or not col.get("field"):
                    continue
                if col["ct"] not in schemas:
                    # get schema as plone.restapi /@types/Schema
                    schemas[col["ct"]] = self._get_schema(col["ct"])
                if not schemas[col["ct"]]:
                    continue
                schema = schemas[col["ct"]]
                if "properties" in schema and col["field"] in schema["properties"]:
                    # TODO: ma servono veramente tutte le info o solo una parte ?
                    col["field_properties"] = schema["properties"][col["field"]]
        return value


class ListingTableVariationBlockSerialize(SearchTableVariationBlockSerialize):
    block_type = "listing"
    value_field = "variation"
