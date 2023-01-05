# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone import api
from plone.restapi.interfaces import ISerializeToJsonSummary
from redturtle.volto.restapi.serializer.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from design.plone.contenttypes.interfaces.incarico import IIncarico
from zope.component import adapter
from zope.component import getMultiAdapter, getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy import PATH_SEPARATOR
from plone.restapi.serializer.converters import json_compatible
import re


RESOLVEUID_RE = re.compile(".*?/resolve[Uu]id/([^/]*)/?(.*)$")


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IDesignPloneContenttypesLayer)
class DefaultJSONSummarySerializer(BaseSerializer):
    def __call__(self, force_all_metadata=False):
        res = super().__call__(force_all_metadata=force_all_metadata)
        metadata_fields = self.metadata_fields()
        if self.context.portal_type == "Persona":
            res["incarichi"] = self.get_incarichi()
        if self.context.portal_type == "Bando":
            if "bando_state" in metadata_fields or self.show_all_metadata_fields:
                res["bando_state"] = self.get_bando_state()

        if "geolocation" in metadata_fields or self.show_all_metadata_fields:
            # backward compatibility for some block templates
            if "geolocation" not in res:
                res["geolocation"] = None
                latitude = res.get("latitude", 0)
                longitude = res.get("longitude", 0)
                if latitude and longitude:
                    res["geolocation"] = {"latitude": latitude, "longitude": longitude}

        res["id"] = self.context.id

        # meta_type
        res["design_italia_meta_type"] = self.get_design_meta_type()

        # tassonomia argomenti
        if "tassonomia_argomenti" in res:
            if res["tassonomia_argomenti"]:
                res["tassonomia_argomenti"] = self.expand_tassonomia_argomenti()

        if self.is_get_call():
            res["has_children"] = self.has_children()

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
        if self.context.portal_type == "News Item":
            # return translate(
            #     self.context.tipologia_notizia,
            #     domain="design.plone.contenttypes",
            #     context=self.request,
            # )
            return self.context.tipologia_notizia
        else:
            return translate(
                ttool[self.context.portal_type].Title(), context=self.request
            )

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

    # TODO: use tipo incarico from taxonomy when taxonomies are ready
    # instead of CT title
    def get_incarichi(self):
        try:
            obj = self.context.getObject()
        except AttributeError:
            obj = self.context

        return ", ".join([x.to_object.title for x in obj.incarichi])


@implementer(ISerializeToJsonSummary)
@adapter(IIncarico, IDesignPloneContenttypesLayer)
class IncaricoDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, force_all_metadata=False):
        res = super().__call__(force_all_metadata=force_all_metadata)
        taxonomy = getUtility(ITaxonomy, name="collective.taxonomy.tipologia_incarico")
        taxonomy_voc = taxonomy.makeVocabulary(self.request.get("LANGUAGE"))
        if "taxonomy_tipologia_incarico" not in res:
            res["taxonomy_tipologia_incarico"] = taxonomy_voc.inv_data.get(
                self.context.taxonomy_tipologia_incarico
            ).replace(PATH_SEPARATOR, "")
        if "data_inizio_incarico" not in res:
            res["data_inizio_incarico"] = json_compatible(
                self.context.data_inizio_incarico
            )
        if "compensi" not in res:
            res["compensi"] = json_compatible(self.context.compensi)
        return res
