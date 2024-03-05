from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone.restapi.interfaces import IZCatalogCompatibleQuery
from plone.restapi.search.query import ZCatalogCompatibleQueryAdapter as BaseAdapter
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from plone import api


@implementer(IZCatalogCompatibleQuery)
@adapter(Interface, IDesignPloneContenttypesLayer)
class ZCatalogCompatibleQueryAdapter(BaseAdapter):
    """ """

    def __call__(self, query):
        """
        Do not show excluded from search items when anonymous are performing
        some catalog searches
        """
        result = super().__call__(query=query)

        if api.user.is_anonymous():
            result["exclude_from_search"] = False

        return result
