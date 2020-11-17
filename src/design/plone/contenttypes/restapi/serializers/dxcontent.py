# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from plone.restapi.serializer.dxcontent import (
    SerializeToJson as BaseSerializer,
)
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseFolderSerializer,
)


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IDesignPloneContenttypesLayer)
class SerializeToJson(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(SerializeToJson, self).__call__(
            version=version, include_items=include_items
        )
        ttool = api.portal.get_tool("portal_types")
        if self.context.portal_type == "News Item":
            result["design_italia_meta_type"] = translate(
                self.context.tipologia_notizia,
                domain=_._domain,
                context=self.request,
            )
        else:
            result["design_italia_meta_type"] = translate(
                ttool[self.context.portal_type].Title(), context=self.request
            )
        return result


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IDesignPloneContenttypesLayer)
class SerializeFolderToJson(BaseFolderSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(SerializeFolderToJson, self).__call__(
            version=version, include_items=include_items
        )
        result["@id"] = self.context.absolute_url()
        ttool = api.portal.get_tool("portal_types")
        if self.context.portal_type == "News Item":
            result["design_italia_meta_type"] = translate(
                self.context.tipologia_notizia,
                domain=_._domain,
                context=self.request,
            )
        else:
            result["design_italia_meta_type"] = translate(
                ttool[self.context.portal_type].Title(), context=self.request
            )
        if "items_total" not in result:
            # siamo in un sotto-elemento di quello richiesto dalla query.
            #  ritorniamo il numero di elementi totale, senza doverli ritornare
            # effettivamente.
            result[
                "items_total"
            ] = self.context.getFolderContents().actual_result_count
        return result
