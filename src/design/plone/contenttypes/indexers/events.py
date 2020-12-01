# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from plone.app.contenttypes.interfaces import IEvent


@indexer(IEvent)
def event_location(context, **kw):
    """
    """
    luoghi_correlati = [x.to_object for x in context.luoghi_correlati]
    luoghi_correlati = filter(bool, luoghi_correlati)
    luoghi_correlati_title = [x.UID() for x in luoghi_correlati]
    return luoghi_correlati_title
