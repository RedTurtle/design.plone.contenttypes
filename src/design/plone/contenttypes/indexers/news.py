from plone.indexer.decorator import indexer
from plone.app.contenttypes.interfaces import INewsItem

@indexer(INewsItem)
def news_people(context, **kw):
    people = context.a_cura_di_persone
    return [persona.UID() for persona in\
            filter(bool, [x.to_object for x in people])]
