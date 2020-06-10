# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseSerializer,
)
from design.plone.contenttypes.interfaces.pagina_argomento import (
    IPaginaArgomento,
)
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from Acquisition import aq_inner
from zope.component import getUtility, queryUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
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
    import pdb

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
    pdb.set_trace()
    return results


def get_related_news(catalog, argomento):

    limit = 4
    query = {
        "portal_type": ["News Item"],
        "sort_on": "effective",
        "sort_order": "descending",
        "sort_limit": limit,
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)[:limit]
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "effective": x.effective and x.effective.__str__() or "",
            "@id": x.getURL() or "",
            "typology": x.tipologia_notizia or "",
        }
        for x in brains
    ]


def get_related_servizio(catalog, argomento):

    query = {
        "portal_type": ["Servizio"],
        "sort_on": "sortable_title",
        "sort_order": "ascending",
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "@id": x.getURL() or "",
        }
        for x in brains
    ]


def get_related_uo(catalog, argomento):
    import pdb

    pdb.set_trace()
    query = {
        # "portal_type": ["Unita organizzativa"],
        # "sort_on": "sortable_title",
        # "sort_order": "ascending",
        # "tassonomia_argomenti": argomento,
    }
    return get_relations(argomento, "tassonomia_argomenti", **query)

    # brains = catalog(**query)
    # return [
    #     {
    #         "title": x.Title or "",
    #         "description": x.Description or "",
    #         "@id": x.getURL() or "",
    #     }
    #     for x in brains
    # ]


def get_related_doc(catalog, argomento):

    query = {
        "portal_type": ["Documento"],
        "sort_on": "sortable_title",
        "sort_order": "ascending",
        "tassonomia_argomenti": argomento,
    }
    brains = catalog(**query)
    return [
        {
            "title": x.Title or "",
            "description": x.Description or "",
            "@id": x.getURL() or "",
        }
        for x in brains
    ]


@implementer(ISerializeToJson)
@adapter(IPaginaArgomento, Interface)
class PaginaArgomentoSerializer(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(PaginaArgomentoSerializer, self).__call__(
            version=None, include_items=True
        )
        # ptypes = api.portal.get_tool("portal_types")
        # behaviours_argomenti = ptypes["Pagina Argomento"].behaviors
        # result["is_using_blokcs"] = "volto.blocks" in behaviours_argomenti
        # if result["is_using_blocks"]:
        #     # don't waste your time: if we are using block, we don't need other
        #     # info
        #     return True

        catalog = api.portal.get_tool("portal_catalog")
        import pdb

        pdb.set_trace()
        result["related_news"] = get_related_news(catalog, self.context)
        result["related_services"] = get_related_servizio(
            catalog, self.context
        )

        result["related_uo"] = get_related_uo(catalog, self.context)

        result["related_docs"] = get_related_doc(catalog, self.context)

        return result
