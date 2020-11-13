# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_hasattr
from pkg_resources import get_distribution
from pkg_resources import parse_version
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getMultiAdapter
from plone.app.querystring import queryparser
from plone.app.event.base import expand_events
from plone.app.event.recurrence import EventOccurrenceAccessor
from plone.app.event.dx.behaviors import EventAccessor
from DateTime import DateTime

zcatalog_version = get_distribution("Products.ZCatalog").version
if parse_version(zcatalog_version) >= parse_version("5.1"):
    SUPPORT_NOT_UUID_QUERIES = True
else:
    SUPPORT_NOT_UUID_QUERIES = False


class ScadenziarioSearchPost(Service):
    """
    Ritorna la lista dei giorni in cui sono presenti elementi da visualizzare
    {
        "@id": "http://localhost:9080/Plone/@scadenziario",
        "items": [
            "2020/11/19",
            "2020/11/26",
            "2020/12/17",
            "2020/12/24",
            "2020/12/31",
            "2021/01/07"
        ]
    }
    """

    def reply(self):
        data = json_body(self.request)
        query = data.get("query", None)
        # b_start = int(data.get("b_start", 0))
        # b_size = int(data.get("b_size", 25))
        sort_on = data.get("sort_on", None)
        sort_order = data.get("sort_order", None)
        limit = int(data.get("limit", 1000))
        # fullobjects = data.get("fullobjects", False)

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

        # Exclude "self" content item from the results when ZCatalog supports
        # NOT UUID
        # queries and it is called on a content object.
        if (
            not IPloneSiteRoot.providedBy(self.context)
            and SUPPORT_NOT_UUID_QUERIES
        ):
            querybuilder_parameters.update(
                dict(custom_query={"UID": {"not": self.context.UID()}})
            )

        # Ottieni tutti i risultati
        results = querybuilder(**querybuilder_parameters)

        # preparati per l'expand degli eventi.
        not_events = [x for x in results if x.portal_type != "Event"]
        events = [x for x in results if x.portal_type == "Event"]
        # prende la query e la trasforma in una query per il catalogo
        # così poi se e quando dobbiamo litigare con delle ricorrenze e date
        # di start ed end, le abbiamo già calcolate, come plone le proporrebbe
        # al catalogo
        query_for_catalog = queryparser.parseFormquery(
            self.context, query, sort_on=sort_on, sort_order=sort_order
        )
        start = None
        end = None
        if "start" in query_for_catalog:
            start = query_for_catalog["start"]["query"]
        if "end" in query_for_catalog:
            end = query_for_catalog["end"]["query"]
        expanded_events = expand_events(events, 3, start, end)

        all_results = not_events + expanded_events
        brains_grouped = {}
        for brain in all_results:
            if not safe_hasattr(brain, "start") or not brain.start:
                continue
            brains_grouped.setdefault(
                brain.start.strftime("%Y/%m/%d"), []
            ).append(brain)
        keys = list(brains_grouped.keys())
        if sort_order:
            keys.sort(reverse=True)
        else:
            keys.sort()

        return {"@id": self.request.get("URL"), "items": keys}


class ScadenziarioDayPost(Service):
    def reply(self):
        data = json_body(self.request)
        query = data.get("query", None)
        sort_on = data.get("sort_on", None)
        sort_order = data.get("sort_order", None)

        if query is None:
            raise Exception("No query supplied")

        if sort_order:
            sort_order = "descending" if sort_order else "ascending"

        # results = querybuilder(**querybuilder_parameters)
        # Seems that origina querybuilder is not able to handle event search on
        # a single day... I can handle this calling catalog and going through
        # DateTime conversion
        query_for_catalog = queryparser.parseFormquery(
            self.context, query, sort_on=sort_on, sort_order=sort_order
        )
        query_for_catalog["start"]["query"][0] = DateTime(
            query_for_catalog["start"]["query"][0]
        )
        query_for_catalog["start"]["query"][1] = DateTime(
            query_for_catalog["start"]["query"][1]
        )
        results = self.context.portal_catalog(query_for_catalog)
        # preparati per l'expand degli eventi.
        not_events = [x for x in results if x.portal_type != "Event"]
        events = [x for x in results if x.portal_type == "Event"]
        start = None
        end = None
        # qui ce l'abbiamo per forza start
        if "start" in query_for_catalog:
            start = query_for_catalog["start"]["query"]
        if "end" in query_for_catalog:
            end = query_for_catalog["end"]["query"]

        expanded_events = expand_events(events, 3, start, end)
        start_date = start[0].strftime("%Y/%m/%d")
        correct_events = []
        for x in expanded_events:
            if start_date == x.start.strftime("%Y/%m/%d"):
                correct_events.append(x)

        all_results = not_events + correct_events

        brains_grouped = {}
        for brain in all_results:
            if not safe_hasattr(results[0], "start"):
                continue
            brains_grouped.setdefault(
                brain.start.strftime("%Y/%m/%d"), []
            ).append(brain)

        keys = list(brains_grouped.keys())
        keys.sort()

        results_to_be_returned = {}
        for key in keys:
            results_to_be_returned[key] = []
            for brain in brains_grouped[key]:
                if isinstance(brain, (EventAccessor, EventOccurrenceAccessor)):
                    if brain.context.portal_type == "Occurrence":
                        url = brain.url[:-10]
                    else:
                        url = brain.url
                    results_to_be_returned[key].append(
                        {
                            "@id": url,
                            "id": brain.id,
                            "title": brain.title,
                            "text": brain.description,
                            "start": brain.start.strftime("%Y/%m/%d"),
                            "type": self.context.translate("Event"),
                            "category": brain.subjects,
                        }
                    )
                else:
                    results_to_be_returned[key].append(
                        {
                            "@id": brain.getURL(),
                            "id": brain.getId,
                            "title": brain.Title,
                            "text": brain.Description,
                            "start": brain.start.strftime("%Y/%m/%d"),
                            "type": self.context.translate(brain.portal_type),
                            "category": brain.subject,
                        }
                    )
                results_to_be_returned[key].sort(key=lambda x: x["title"])
        return {
            "@id": self.request.get("URL"),
            "items": results_to_be_returned,
        }
