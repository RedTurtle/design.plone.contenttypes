# -*- coding: utf-8 -*-
from design.plone.contenttypes.restapi.serializers.dxcontent import (
    SerializeFolderToJson,
)
from design.plone.contenttypes.interfaces.documento import IDocumento
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IDocumento, Interface)
class DocumentoSerializer(SerializeFolderToJson):
    def __call__(self, version=None, include_items=True):
        if "b_size" not in self.request.form:
            self.request.form["b_size"] = 200
        return super(DocumentoSerializer, self).__call__(
            version=version, include_items=include_items
        )
