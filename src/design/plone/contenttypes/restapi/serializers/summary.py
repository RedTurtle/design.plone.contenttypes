# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.interfaces.persona import IPersona
from plone import api
from plone.base.interfaces import IImageScalesAdapter
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.restapi.interfaces import ISerializeToJsonSummary
from Products.ZCatalog.interfaces import ICatalogBrain
from redturtle.volto.restapi.serializer.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from zope.component import adapter
from zope.component import getMultiAdapter

from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFieldsInOrder

import logging


logger = logging.getLogger(__name__)


def extract_geolocation(context, res):
    """
    Extracts geolocation information from the provided context or res.
    """
    # Check if latitude and longitude are already present in res
    latitude = res.get("latitude", 0)
    longitude = res.get("longitude", 0)

    if latitude and longitude:
        return {"latitude": latitude, "longitude": longitude}

    # Check if context is an ICatalogBrain and has latitude and longitude
    if ICatalogBrain.providedBy(context):
        latitude = context.latitude
        longitude = context.longitude
        if latitude and longitude:
            return {"latitude": latitude, "longitude": longitude}
    else:
        # Check if context has a geolocation attribute with latitude and longitude
        geolocation = getattr(context, "geolocation", None)
        if isinstance(geolocation, Geolocation):
            latitude = geolocation.latitude
            longitude = geolocation.longitude
            if latitude and longitude:
                return {"latitude": latitude, "longitude": longitude}

    return None


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IDesignPloneContenttypesLayer)
class DefaultJSONSummarySerializer(BaseSerializer):
    def __call__(self, force_all_metadata=False, force_images=False):
        res = super().__call__(force_all_metadata=force_all_metadata)
        metadata_fields = self.metadata_fields()
        if self.context.portal_type == "Bando":
            if "tipologia_bando" not in res:
                res["tipologia_bando"] = getattr(self.context, "tipologia_bando", "")
            if "bando_state" in metadata_fields or self.show_all_metadata_fields:
                res["bando_state"] = self.get_bando_state()

        if "geolocation" in metadata_fields or self.show_all_metadata_fields:
            # backward compatibility for some block templates
            if "geolocation" not in res:
                res["geolocation"] = extract_geolocation(self.context, res)

        res["id"] = self.context.id
        res["UID"] = (
            self.context.UID() if callable(self.context.UID) else self.context.UID
        )

        # meta_type
        res["design_italia_meta_type"] = self.get_design_meta_type()
        # tassonomia argomenti
        if "tassonomia_argomenti" in res:
            if res["tassonomia_argomenti"]:
                res["tassonomia_argomenti"] = self.expand_tassonomia_argomenti()

        if self.is_get_call():
            res["has_children"] = self.has_children()

        if force_images:
            # TODO: verificare se non c'è il campo o se il campo è null/vuoto ?
            if not res.get("image_scales") and not res.get("image_field"):
                adapter = queryMultiAdapter(
                    (self.context, self.request), IImageScalesAdapter
                )
                if adapter:
                    scales = adapter()
                    if scales:
                        res["image_scales"] = scales
                    if "preview_image" in scales:
                        res["image_field"] = "preview_image"
                    elif "image" in scales:
                        res["image_field"] = "image"

        return res

    def has_children(self):
        try:
            obj = self.context.getObject()
        except AttributeError:
            obj = self.context
        try:
            if obj.aq_base.keys():
                return True
        except AttributeError:
            return False
        return False

    def is_get_call(self):
        steps = self.request.steps
        if not steps:
            return False
        return steps[-1] == "GET_application_json_"

    def get_design_meta_type(self):
        ttool = api.portal.get_tool("portal_types")
        return translate(ttool[self.context.portal_type].Title(), context=self.request)

    def expand_tassonomia_argomenti(self):
        try:
            obj = self.context.getObject()
        except AttributeError:
            obj = self.context
        arguments = []
        for ref in getattr(obj, "tassonomia_argomenti", []):
            ref_obj = ref.to_object
            if not ref_obj:
                continue
            if not api.user.has_permission("View", obj=ref_obj):
                continue
            arguments.append(
                getMultiAdapter((ref_obj, self.request), ISerializeToJsonSummary)()
            )
        return arguments

    def get_bando_state(self):
        """
        È il metodo più safe per ottenere lo stato del bando
        anche se non il più veloce
        """
        bando = self.context.getObject()
        view = api.content.get_view("bando_view", context=bando, request=self.request)
        return view.getBandoState()


# TODO: questo potrebbe non essere più necessario, vista l'implementazione
# di DefaultJSONSummarySerializer con image_scales e image_field
@implementer(ISerializeToJsonSummary)
@adapter(IPersona, IDesignPloneContenttypesLayer)
class PersonaDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        fields = dict(getFieldsInOrder(IPersona))
        field = fields.get("foto_persona", None)
        if field:
            images_info_adapter = getMultiAdapter(
                (field, self.context, IDesignPloneContenttypesLayer)
            )
            if images_info_adapter:
                res["image_scales"] = {
                    "foto_persona": [images_info_adapter()],
                }
            res["image_field"] = "foto_persona"
        return res
