# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityItem


@indexer(IDexterityContainer)
@indexer(IDexterityItem)
def tassonomia_argomenti(context, **kw):
    import pdb

    pdb.set_trace()
    # return getattr(context, "tassonomia_argomenti", None)
    tassonomie = context.tassonomia_argomenti
    return [
        tassonomia.UID()
        for tassonomia in filter(bool, [x.to_object for x in tassonomie])
    ]
