from plone.indexer.decorator import indexer
from design.plone.contenttypes.behaviors.argomenti import IArgomenti


@indexer(IArgomenti)
def argomenti_correlati(context, **kw):
    argomenti = context.tassonomia_argomenti
    return [
        argomento.UID()
        for argomento in filter(bool, [x.to_object for x in argomenti])
    ]
