# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone import api
from plone.app.contenttypes.interfaces import ILink
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.outputfilters.browser.resolveuid import uuidToURL
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJsonSummary
from redturtle.volto.restapi.serializer.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer
import re

RESOLVEUID_RE = re.compile(".*?/resolve[Uu]id/([^/]*)/?(.*)$")


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IDesignPloneContenttypesLayer)
class DefaultJSONSummarySerializer(BaseSerializer):
    def __call__(self):
        res = super().__call__()
        query = self.request.form
        if not query:
            # maybe its a POST request
            query = json_body(self.request)
        metadata_fields = query.get("metadata_fields", [])

        if self.context.portal_type == "Link":
            res["remoteUrl"] = self.get_remote_url()
        if self.context.portal_type == "Persona":
            res["ruolo"] = self.context.ruolo
        if self.context.portal_type == "Bando":
            if "_all" in metadata_fields or "bando_state" in metadata_fields:
                res["bando_state"] = self.get_bando_state()

        if "_all" in metadata_fields or "geolocation" in metadata_fields:
            # backward compatibility for some block templates
            if "geolocation" not in res:
                res["geolocation"] = {}
                if res.get("latitude", ""):
                    res["geolocation"]["latitude"] = res["latitude"]
                if res.get("longitude", ""):
                    res["geolocation"]["longitude"] = res["longitude"]

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
            return translate(
                self.context.tipologia_notizia,
                domain="design.plone.contenttypes",
                context=self.request,
            )
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
        E' il metodo più safe per ottenere lo stato del bando, anche se non il più veloce
        """
        bando = self.context.getObject()
        view = api.content.get_view("bando_view", context=bando, request=self.request)
        return view.getBandoState()

    def get_remote_url(self):
        if ILink.providedBy(self.context):
            value = getattr(self.context, "remoteUrl", "")
        else:
            value = self.context.getRemoteUrl
        if not value:
            return ""
        path = replace_link_variables_by_paths(context=self.context, url=value)
        match = RESOLVEUID_RE.match(path)
        if match:
            uid, suffix = match.groups()
            return uuidToURL(uid)
        else:
            portal = getMultiAdapter(
                (self.context, self.context.REQUEST), name="plone_portal_state"
            ).portal()
            ref_obj = portal.restrictedTraverse(path, None)
            if ref_obj:
                return ref_obj.absolute_url()
        return value
