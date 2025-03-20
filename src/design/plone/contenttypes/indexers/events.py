# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IEvent
from plone.indexer.decorator import indexer
from plone.event.interfaces import IEventAccessor
from plone.event.interfaces import IRecurrenceSupport


@indexer(IEvent)
def event_location(context, **kw):
    """ """
    luoghi_correlati = [x.to_object for x in context.luoghi_correlati]
    luoghi_correlati = filter(bool, luoghi_correlati)
    luoghi_correlati_title = [x.UID() for x in luoghi_correlati]
    return luoghi_correlati_title


@indexer(IEvent)
def rassegna(context, **kw):
    """ """
    children = context.values()
    return "Event" in [child.portal_type for child in children]


@indexer(IEvent)
def effectivestart(obj):
    start = IEventAccessor(obj).start
    if not start:
        raise AttributeError
    return start


@indexer(IEvent)
def effectiveend(obj):
    occurrences = IRecurrenceSupport(obj).occurrences()
    end = obj.end
    for occurrence in list(occurrences):
        if occurrence.end > end:
            end = occurrence.end
    return end
