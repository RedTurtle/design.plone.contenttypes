# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_hasattr
from pkg_resources import get_distribution
from pkg_resources import parse_version
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getMultiAdapter
from plone.batching import Batch

zcatalog_version = get_distribution("Products.ZCatalog").version
if parse_version(zcatalog_version) >= parse_version("5.1"):
    SUPPORT_NOT_UUID_QUERIES = True
else:
    SUPPORT_NOT_UUID_QUERIES = False


class ScadenziarioSearchPost(Service):
    """Returns the querystring search results given a p.a.querystring data.
    """

    def reply(self):
        data = json_body(self.request)
        query = data.get("query", None)
        b_start = int(data.get("b_start", 0))
        # b_size = int(data.get("b_size", 25))
        b_size = 4 # we fix this one
        sort_on = data.get("sort_on", None)
        sort_order = data.get("sort_order", None)
        limit = int(data.get("limit", 1000))
        fullobjects = data.get("fullobjects", False)

        if query is None:
            raise Exception("No query supplied")

        if sort_order:
            sort_order = "descending" if sort_order else "ascending"

        querybuilder = getMultiAdapter(
            (self.context, self.request), name="querybuilderresults"
        )

        querybuilder_parameters = dict(
            query=query,
            brains=True,
            # b_start=b_start,
            # b_size=b_size,
            sort_on=sort_on,
            sort_order=sort_order,
            limit=limit,
        )

        # Exclude "self" content item from the results when ZCatalog supports NOT UUID
        # queries and it is called on a content object.
        if not IPloneSiteRoot.providedBy(self.context) and SUPPORT_NOT_UUID_QUERIES:
            querybuilder_parameters.update(
                dict(custom_query={"UID": {"not": self.context.UID()}})
            )

        results = querybuilder(**querybuilder_parameters)
        brains_grouped = {}
        for brain in results:
            if not safe_hasattr(results[0], 'start'):
                continue
            brains_grouped.setdefault(
                brain.start.strftime("%Y/%m/%d"), []
            ).append(brain)
        import pdb;pdb.set_trace()
        # {k: result[k] for k in sorted(brain_grouped)}
        batch = Batch(results, size=b_size, orphan=0)

        # results = getMultiAdapter((list(batch), self.request), ISerializeToJson)(
        #     fullobjects=fullobjects
        # )
        return results
