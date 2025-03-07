# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from design.plone.contenttypes.interfaces.documento import IDocumento
from design.plone.contenttypes.restapi.serializers.dxcontent import (
    SerializeFolderToJson,
)
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


@implementer(ISerializeToJson)
@adapter(IDocumento, Interface)
class DocumentoSerializer(SerializeFolderToJson):
    def get_services(self):
        """ """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        services = []
        for attr in ["altri_documenti"]:
            relations = catalog.findRelations(
                dict(
                    to_id=intids.getId(aq_inner(self.context)),
                    from_attribute=attr,
                )
            )

            for rel in relations:
                obj = intids.queryObject(rel.from_id)
                if (
                    obj is not None
                    and checkPermission("zope2.View", obj)  # noqa
                    and obj.portal_type == "Servizio"  # noqa
                ):
                    summary = getMultiAdapter(
                        (obj, getRequest()), ISerializeToJsonSummary
                    )()
                    services.append(summary)
        return sorted(services, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        if "b_size" not in self.request.form:
            self.request.form["b_size"] = 200
        result = super(DocumentoSerializer, self).__call__(
            version=version, include_items=include_items
        )
        # Una via alternativa era l'injection di fullobject nella request ma
        # mi pare una cosa cattiva da fare
        brain_moduli = [
            x for x in self.context.getFolderContents() if x.portal_type != "Document"
        ]
        result["moduli_del_documento"] = []
        for brain in brain_moduli:
            modulo = brain.getObject()
            result["moduli_del_documento"].append(
                getMultiAdapter((modulo, self.request), ISerializeToJson)()
            )
        result["servizi_collegati"] = self.get_services()

        types = result["@components"]["types"]
        # if we don't have expand in request we don't have a list but this:
        if isinstance(types, list):
            for cttype in result["@components"]["types"]:
                if cttype["id"] == "File":
                    cttype["addable"] = False
                    cttype["immediately_addable"] = False
        return result
