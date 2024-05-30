# -*- coding: utf-8 -*-
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseFolderSerializer,
)
from plone.restapi.serializer.dxcontent import SerializeToJson as BaseSerializer
from zope.component import adapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer


class MetaTypeSerializer(object):
    def get_design_meta_type(self):
        ttool = api.portal.get_tool("portal_types")
        tipologia_notizia = getattr(self.context, "tipologia_notizia", "")
        if self.context.portal_type == "News Item" and tipologia_notizia:
            taxonomy = getUtility(
                ITaxonomy, name="collective.taxonomy.tipologia_notizia"
            )
            taxonomy_voc = taxonomy.makeVocabulary(self.request.get("LANGUAGE"))
            if isinstance(tipologia_notizia, list):
                token = tipologia_notizia[0]
            else:
                token = tipologia_notizia
            title = taxonomy_voc.inv_data.get(token, None)

            if title and title.startswith(PATH_SEPARATOR):
                return title.replace(PATH_SEPARATOR, "", 1)
        return translate(ttool[self.context.portal_type].Title(), context=self.request)


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IDesignPloneContenttypesLayer)
class SerializeToJson(BaseSerializer, MetaTypeSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(SerializeToJson, self).__call__(
            version=version, include_items=include_items
        )
        result["design_italia_meta_type"] = self.get_design_meta_type()
        return result


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IDesignPloneContenttypesLayer)
class SerializeFolderToJson(BaseFolderSerializer, MetaTypeSerializer):
    def __call__(self, version=None, include_items=True):

        result = super(SerializeFolderToJson, self).__call__(
            version=version, include_items=include_items
        )
        result["@id"] = self.context.absolute_url()
        result["design_italia_meta_type"] = self.get_design_meta_type()

        if "items_total" not in result:
            # siamo in un sotto-elemento di quello richiesto dalla query.
            #  ritorniamo il numero di elementi totale, senza doverli ritornare
            # effettivamente.
            result["items_total"] = self.context.getFolderContents().actual_result_count
        return result
