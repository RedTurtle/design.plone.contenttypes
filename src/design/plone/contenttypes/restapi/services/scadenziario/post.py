# -*- coding: utf-8 -*-
from DateTime import DateTime
from pkg_resources import get_distribution
from pkg_resources import parse_version
from plone.app.event.base import _get_compare_attr
from plone.app.event.base import _obj_or_acc
from plone.app.event.base import RET_MODE_BRAINS
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.event.recurrence import EventOccurrenceAccessor
from plone.app.querystring import queryparser
from plone.base.interfaces import IImageScalesAdapter
from plone.event.interfaces import IEvent
from plone.event.interfaces import IEventRecurrence
from plone.event.interfaces import IRecurrenceSupport
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_hasattr
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter

zcatalog_version = get_distribution("Products.ZCatalog").version
if parse_version(zcatalog_version) >= parse_version("5.1"):
    SUPPORT_NOT_UUID_QUERIES = True
else:
    SUPPORT_NOT_UUID_QUERIES = False


class BaseService(Service):
    def expand_events(
        self, events, ret_mode, start=None, end=None, sort=None, sort_reverse=None
    ):
        """Expand to the recurrence occurrences of a given set of events.

        :param events: IEvent based objects or IEventAccessor object wrapper.

        :param ret_mode: Return type of search results. These options are
                        available:

                            * 2 (objects): Return results as IEvent and/or
                                            IOccurrence objects.
                            * 3 (accessors): Return results as IEventAccessor
                                            wrapper objects.
                        Option "1" (brains) is not supported.

        :type ret_mode: integer [2|3]

        :param start: Date, from which on events should be expanded.
        :type start: Python datetime.

        :param end: Date, until which events should be expanded.
        :type end: Python datetime

        :param sort: Object or IEventAccessor Attribute to sort on.
        :type sort: string

        :param sort_reverse: Change the order of the sorting.
        :type sort_reverse: boolean

        COPIATO DA plone.app.event 3.2.10 perché nella 3.2.13 è cambiato e si
        rompe con i parametri che gli passiamo. Visto che la logica ci andava
        bene così, non stiamo a metterci mano.

        """

        assert ret_mode is not RET_MODE_BRAINS  # nosec

        exp_result = []
        for it in events:
            obj = it.getObject() if getattr(it, "getObject", False) else it
            if IEventRecurrence.providedBy(obj):
                occurrences = [
                    _obj_or_acc(occ, ret_mode)
                    for occ in IRecurrenceSupport(obj).occurrences(start, end)
                ]
            elif IEvent.providedBy(obj):
                occurrences = [_obj_or_acc(obj, ret_mode)]
            else:
                # No IEvent based object. Could come from a collection.
                continue
            exp_result += occurrences
        if sort:
            exp_result.sort(key=lambda x: _get_compare_attr(x, sort))
        if sort_reverse:
            exp_result.reverse()
        return exp_result

    def _get_image_scales(self, context):
        """Get image scales for a content object."""
        scales = queryMultiAdapter(
            (context, self.request),
            IImageScalesAdapter,
        )
        return scales() if scales else {}

    def _get_related_places(self, event_obj):
        """Extract related places (luoghi_correlati) from event object.

        Returns a list of dicts with 'name' and 'url' keys.
        """
        related_places = []
        try:
            # Try to get the field from the behavior
            if hasattr(event_obj, "luoghi_correlati"):
                relations = event_obj.luoghi_correlati
                if relations:
                    for relation in relations:
                        target = relation.to_object
                        if target:
                            related_places.append(
                                {
                                    "name": target.title or target.id,
                                    "url": target.absolute_url(),
                                }
                            )
        except (AttributeError, TypeError):
            # Field doesn't exist or relation access fails
            pass
        return related_places

    def _get_parent_event(self, event_obj):
        """Get parent event info if this event is a child of another event.

        Returns a dict with 'name' and 'url' keys, or None if no parent.
        """
        try:
            parent = event_obj.aq_parent
            if parent and parent.portal_type == "Event":
                return {
                    "name": parent.title or parent.id,
                    "url": parent.absolute_url(),
                }
        except (AttributeError, TypeError):
            pass
        return None


class ScadenziarioSearchPost(BaseService):
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
            sort_order = "descending" if sort_order == "descending" else "ascending"

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
        if not IPloneSiteRoot.providedBy(self.context) and SUPPORT_NOT_UUID_QUERIES:
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
            if query_for_catalog["end"].get("range", "") != "min":
                # per esempio, è impostato il filtro "con fine evento da domani".
                # se impostiamo un'end (la data  di domani), poi nella generazione delle ricorrenze,
                # vengono scartati tutti gli eventi che hanno una data di inizio nel futuro
                # (https://github.com/plone/plone.event/blob/master/plone/event/recurrence.py#L141)
                # perché la data della ricorrenza è maggiore di "until", che è quello che qui inviamo come end.
                end = query_for_catalog["end"]["query"]
        expanded_events = self.expand_events(events, 3, start, end)

        all_results = not_events + expanded_events
        brains_grouped = {}
        for brain in all_results:
            if not safe_hasattr(brain, "start") or not brain.start:
                continue
            brains_grouped.setdefault(brain.start.strftime("%Y/%m/%d"), []).append(
                brain
            )
        keys = list(brains_grouped.keys())
        if sort_order == "descending":
            keys.sort(reverse=True)
        else:
            keys.sort()

        return {"@id": self.request.get("URL"), "items": keys}


class ScadenziarioDayPost(BaseService):
    def reply(self):
        data = json_body(self.request)
        query = data.get("query", None)
        sort_on = data.get("sort_on", None)
        sort_order = data.get("sort_order", None)

        if query is None:
            raise Exception("No query supplied")

        if sort_order not in {"descending", "ascending"}:
            sort_order = "ascending"

        # Convert query to catalog query with DateTime objects
        query_for_catalog = queryparser.parseFormquery(
            self.context, query, sort_on=sort_on, sort_order=sort_order
        )
        query_for_catalog["start"]["query"][0] = DateTime(
            query_for_catalog["start"]["query"][0]
        )
        query_for_catalog["start"]["query"][1] = DateTime(
            query_for_catalog["start"]["query"][1]
        )

        # Execute the catalog query
        results = self.context.portal_catalog(query_for_catalog)

        # Separate events from other content types
        not_events = [x for x in results if x.portal_type != "Event"]
        events = [x for x in results if x.portal_type == "Event"]

        # Extract start/end dates from query
        start = end = None
        if "start" in query_for_catalog:
            start = query_for_catalog["start"]["query"][0]
        if "end" in query_for_catalog:
            end = query_for_catalog["start"]["query"][1]

        # Expand recurring events
        expanded_events = self.expand_events(events, 3, start, end)

        # Filter events to only those on the requested day
        start_date = start.strftime("%Y/%m/%d")
        correct_events = [
            x
            for x in expanded_events
            if start_date == x.start.strftime("%Y/%m/%d")  # noqa: E501
        ]

        # Combine all results
        all_results = not_events + correct_events

        # Group results by date
        brains_grouped = {}
        for brain in all_results:
            if not safe_hasattr(brain, "start") or not brain.start:
                continue
            date_key = brain.start.strftime("%Y/%m/%d")
            brains_grouped.setdefault(date_key, []).append(brain)

        # Build response with enhanced data
        results_to_be_returned = {}
        for date_key in sorted(brains_grouped.keys()):
            results_to_be_returned[date_key] = []
            for brain in brains_grouped[date_key]:
                item_data = self._build_item_data(brain)
                results_to_be_returned[date_key].append(item_data)

        return {
            "@id": self.request.get("URL"),
            "items": results_to_be_returned,
        }

    def _build_item_data(self, brain):
        """Build the data dictionary for a single item.

        Handles both EventAccessor/EventOccurrenceAccessor and brain results.
        """
        if isinstance(brain, (EventAccessor, EventOccurrenceAccessor)):
            return self._build_event_accessor_item(brain)
        else:
            return self._build_brain_item(brain)

    def _build_event_accessor_item(self, brain):
        """Build item data from EventAccessor or EventOccurrenceAccessor."""
        # Get the actual object based on occurrence type
        if brain.context.portal_type == "Occurrence":
            event_obj = brain.context.aq_parent
            url = brain.url[:-10]  # Remove "/@@view" suffix
        else:
            event_obj = brain.context
            url = brain.url

        # Get image scales
        image_scales = self._get_image_scales(event_obj)

        # Build base item data
        item_data = {
            "@id": url,
            "id": brain.id,
            "title": brain.title,
            "text": brain.description,
            "start": brain.start.isoformat(),
            "type": self.context.translate("Event"),
            "category": brain.subjects,
            "image_scales": image_scales,
        }

        # Add related places and parent event info
        self._add_relations_data(item_data, event_obj)

        return item_data

    def _build_brain_item(self, brain):
        """Build item data from a catalog brain (non-event)."""
        return {
            "@id": brain.getURL(),
            "id": brain.getId,
            "title": brain.Title,
            "text": brain.Description,
            "start": brain.start.isoformat(),
            "type": self.context.translate(brain.portal_type),
            "category": brain.subject,
        }

    def _add_relations_data(self, item_data, event_obj):
        """Add related places and parent event info to item data."""
        # Add related places (luoghi_correlati)
        related_places = self._get_related_places(event_obj)
        if related_places:
            item_data["luoghi_correlati"] = related_places

        # Add parent event info (rassegna)
        parent_event = self._get_parent_event(event_obj)
        if parent_event:
            item_data["parent_event"] = parent_event
