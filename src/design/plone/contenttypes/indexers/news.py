# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from plone.app.contenttypes.interfaces import INewsItem


@indexer(INewsItem)
def news_people(context, **kw):
    people = context.a_cura_di_persone
    return [
        persona.UID()
        for persona in filter(bool, [x.to_object for x in people])
    ]


@indexer(INewsItem)
def news_uo(context, **kw):
    unita_organizzative = context.a_cura_di
    return [
        unita_organizzativa.UID()
        for unita_organizzativa in filter(
            bool, [x.to_object for x in unita_organizzative]
        )
    ]


@indexer(INewsItem)
def news_service(context, **kw):
    servizi = context.servizi_correlati
    return [
        servizio.UID()
        for servizio in filter(bool, [x.to_object for x in servizi])
    ]


@indexer(INewsItem)
def news_venue(context, **kw):
    luoghi = context.luoghi_correlati
    return [
        luogo.UID() for luogo in filter(bool, [x.to_object for x in luoghi])
    ]
