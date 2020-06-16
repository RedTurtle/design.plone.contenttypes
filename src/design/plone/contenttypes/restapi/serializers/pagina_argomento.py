# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseSerializer,
)
from design.plone.contenttypes.interfaces.pagina_argomento import (
    IPaginaArgomento,
)
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.component import getUtility, queryUtility
from zope.intid.interfaces import IIntIds
from zc.relation.interfaces import ICatalog


def get_intid(obj):
    """Return the intid of an object from the intid-catalog"""
    intids = queryUtility(IIntIds)
    if intids is None:
        return
    # check that the object has an intid, otherwise there's nothing to be done
    try:
        return intids.getId(obj)
    except KeyError:
        # The object has not been added to the ZODB yet
        return


def get_relations(obj, attribute=None, backrefs=False, kw={}):
    """Get any kind of references and backreferences"""

    int_id = get_intid(obj)

    if not int_id:
        return []

    relation_catalog = getUtility(ICatalog)
    if not relation_catalog:
        return []

    query = {**kw}
    if attribute:
        # Constrain the search for certain relation-types.
        query["from_attribute"] = attribute

    if backrefs:
        query["to_id"] = int_id
    else:
        query["from_id"] = int_id

    results = relation_catalog.findRelations(query)
    relations = {}
    for x in results:
        el = x.from_object
        if el:
            pt = el.portal_type
            if not isinstance(relations.get(pt, None), list):
                relations[pt] = []

            relations[pt].append(el)

    return relations


def get_related_contenttype(relations, portal_type, limit=None):

    if not relations.get(portal_type, None):
        return []
    if limit:
        return [
            {
                "title": x.Title() or "",
                "description": x.Description() or "",
                "@id": x.absolute_url() or "",
            }
            for x in relations[portal_type][:limit]
        ]
    return [
        {
            "title": x.Title() or "",
            "description": x.Description() or "",
            "@id": x.absolute_url() or "",
        }
        for x in relations[portal_type]
    ]


@implementer(ISerializeToJson)
@adapter(IPaginaArgomento, Interface)
class PaginaArgomentoSerializer(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(PaginaArgomentoSerializer, self).__call__(
            version=None, include_items=True
        )

        relations = get_relations(
            self.context, "tassonomia_argomenti", backrefs=True
        )

        result["related_uo"] = get_related_contenttype(
            relations, "UnitaOrganizzativa"
        )
        result["related_news"] = get_related_contenttype(
            relations, "News Item", 4
        )
        result["related_services"] = get_related_contenttype(
            relations, "Servizio"
        )
        result["related_docs"] = get_related_contenttype(
            relations, "Documento"
        )

        return result
