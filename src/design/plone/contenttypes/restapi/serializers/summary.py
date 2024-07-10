# -*- coding: utf-8 -*-
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.interfaces.dataset import IDataset
from design.plone.contenttypes.interfaces.documento import IDocumento
from design.plone.contenttypes.interfaces.incarico import IIncarico
from design.plone.contenttypes.interfaces.persona import IPersona
from design.plone.contenttypes.interfaces.pratica import IPratica
from design.plone.contenttypes.interfaces.punto_di_contatto import IPuntoDiContatto
from plone import api
from plone.app.contenttypes.interfaces import IEvent
from plone.app.contenttypes.interfaces import INewsItem
from plone.base.interfaces import IImageScalesAdapter
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from Products.CMFPlone.utils import safe_hasattr
from Products.ZCatalog.interfaces import ICatalogBrain
from redturtle.volto.restapi.serializer.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFieldsInOrder

import logging
import re


RESOLVEUID_RE = re.compile(".*?/resolve[Uu]id/([^/]*)/?(.*)$")
logger = logging.getLogger(__name__)


def get_taxonomy_information(field_name, context, res):
    """
    Get the proper values for taxonomy fields
    """
    request = getRequest()
    taxonomy = getUtility(ITaxonomy, name=f"collective.taxonomy.{field_name}")
    taxonomy_voc = taxonomy.makeVocabulary(request.get("LANGUAGE"))

    # il summary di un fullobject torna un value
    # il summary di un brain torna una lista (collective.taxonomy ha motivi per
    # fare così).

    # se abbiamo il summary di un fullobject o il summary di un brain non importa
    # ritorna quello che avevi in pancia, se non avevi nulla.

    # Hai quel campo compilato? Ti trasformo come serve al frontend
    if ICatalogBrain.providedBy(context):
        fullterms = []
        # delle volte posso avere il brain senza quel dato
        if field_name not in res:
            res[field_name] = getattr(context, field_name, None) or []
        for token in res[field_name]:
            title = taxonomy_voc.inv_data.get(token, None)
            if title and title.startswith(PATH_SEPARATOR):
                title = title.replace(PATH_SEPARATOR, "", 1)
            fullterms.append({"token": token, "title": title})
        res[field_name] = fullterms
    else:
        value = getattr(context, field_name, None)

        def get_fullterms(token):
            if not token:
                return None
            title = taxonomy_voc.inv_data.get(token, None)
            if title and title.startswith(PATH_SEPARATOR):
                title = title.replace(PATH_SEPARATOR, "", 1)
            return {
                "token": token,
                "title": title,
            }

        if isinstance(value, list):
            res[field_name] = [get_fullterms(token) for token in value]
        elif isinstance(value, str):
            res[field_name] = get_fullterms(value)

    return res


def get_taxonomy_information_by_type(res, context):
    portal_type = res.get("portal_type", None) or res.get("@type")
    portal_type_mapping = {
        "News Item": ("tipologia_notizia",),
        "Event": ("tipologia_evento",),
        "Venue": ("tipologia_luogo",),
        "Dataset": (
            "temi_dataset",
            "tipologia_frequenza_aggiornamento",
            "tipologia_licenze",
        ),
        "Documento": (
            "tipologia_documenti_albopretorio",
            "tipologia_documento",
            "tipologia_licenze",
            "person_life_events",
            "business_events",
        ),
        "Pratica": ("tipologia_stati_pratica",),
        "UnitaOrganizzativa": ("tipologia_organizzazione",),
        "Incarico": ("tipologia_incarico",),
        "Servizio": ("person_life_events", "business_events"),
    }
    for field_name in portal_type_mapping.get(portal_type, []):
        get_taxonomy_information(field_name, context, res)

    return res


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
        if self.context.portal_type == "Persona":
            res["incarichi"] = self.get_incarichi()
        if self.context.portal_type == "Bando":
            if "tipologia_bando" not in res:
                res["tipologia_bando"] = getattr(self.context, "tipologia_bando", "")
            if "bando_state" in metadata_fields or self.show_all_metadata_fields:
                res["bando_state"] = self.get_bando_state()
        if self.context.portal_type == "Event":
            res["start"] = json_compatible(self.context.start)

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

        get_taxonomy_information_by_type(res, self.context)

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
            # plone.app.contentlisting 3.0.5 sembra fissare un accessor che ci
            # fa arrivare uno scale senza image_field.
            # avremmo questo problema una volta passati a plone 6.0.11
            elif res.get("image_scales") and not res.get("image_field"):
                if "preview_image" in res["image_scales"]:
                    res["image_field"] = "preview_image"
                elif "image" in res["image_scales"]:
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
        if self.context.portal_type == "News Item":
            tipologia_notizia = getattr(self.context, "tipologia_notizia", "")
            if tipologia_notizia:
                taxonomy = getUtility(
                    ITaxonomy, name="collective.taxonomy.tipologia_notizia"
                )
                taxonomy_voc = taxonomy.makeVocabulary(self.request.get("LANGUAGE"))
                if isinstance(tipologia_notizia, list):
                    token = tipologia_notizia[0]
                else:
                    token = tipologia_notizia
                title = taxonomy_voc.inv_data.get(token, None)
                if title:
                    if title.startswith(PATH_SEPARATOR):
                        title = title.replace(PATH_SEPARATOR, "", 1)
                    return title
        if self.context.portal_type in ttool:
            return translate(
                ttool[self.context.portal_type].Title(), context=self.request
            )
        else:
            return self.context.portal_type

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

        incarichi = []
        for incarico in obj.incarichi_persona:
            if not incarico.to_object:
                continue

            if not api.user.has_permission("View", obj=incarico.to_object):
                continue
            incarichi.append(incarico.to_object.title)
        return ", ".join(incarichi)


@implementer(ISerializeToJsonSummary)
@adapter(IIncarico, IDesignPloneContenttypesLayer)
class IncaricoDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        get_taxonomy_information("tipologia_incarico", self.context, res)
        if "data_inizio_incarico" not in res:
            res["data_inizio_incarico"] = json_compatible(
                self.context.data_inizio_incarico
            )
        else:
            res["data_inizio_incarico"] = json_compatible(None)

        if "data_conclusione_incarico" not in res:
            res["data_conclusione_incarico"] = json_compatible(
                self.context.data_conclusione_incarico
            )
        else:
            res["data_conclusione_incarico"] = json_compatible(None)

        if "data_insediamento" not in res:
            res["data_insediamento"] = json_compatible(self.context.data_insediamento)
        else:
            res["data_insediamento"] = json_compatible(None)

        if "compensi" not in res:
            res["compensi"] = json_compatible(self.context.compensi)
        else:
            res["compensi"] = json_compatible([])

        if "importi_viaggio_servizio" not in res:
            res["importi_viaggio_servizio"] = json_compatible(
                self.context.importi_viaggio_servizio
            )
        else:
            res["importi_viaggio_servizio"] = json_compatible([])

        if safe_hasattr(self.context, "compensi-file"):
            compensi_folder = getattr(self.context, "compensi-file")
            res["compensi_file"] = []
            if api.user.has_permission("View", obj=compensi_folder):
                for brain in getattr(self.context, "compensi-file").getFolderContents():
                    res["compensi_file"].append(
                        getMultiAdapter(
                            (brain, self.request), ISerializeToJsonSummary
                        )()
                    )

        if safe_hasattr(self.context, "importi-di-viaggio-e-o-servizi"):
            importi_folder = getattr(self.context, "importi-di-viaggio-e-o-servizi")
            res["importi_di_viaggio_e_o_servizi"] = []
            if api.user.has_permission("View", obj=importi_folder):
                for brain in importi_folder.getFolderContents():
                    res["importi_di_viaggio_e_o_servizi"].append(
                        getMultiAdapter(
                            (brain, self.request), ISerializeToJsonSummary
                        )()
                    )

        if "atto_di_nomina" not in res:
            res["atto_di_nomina"] = None
            atto = getattr(self.context, "atto_nomina", None)
            if atto and not atto[0].isBroken():
                atto = atto[0].to_object
                res["atto_di_nomina"] = atto.absolute_url()
        return res


@implementer(ISerializeToJsonSummary)
@adapter(IPuntoDiContatto, IDesignPloneContenttypesLayer)
class PuntoDiContattoDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        res["value_punto_contatto"] = self.context.value_punto_contatto
        return res


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


@implementer(ISerializeToJsonSummary)
@adapter(IEvent, IDesignPloneContenttypesLayer)
class EventDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, force_images=True, **kwargs):
        res = super().__call__(force_images=force_images, **kwargs)
        get_taxonomy_information("tipologia_evento", self.context, res)
        return res


@implementer(ISerializeToJsonSummary)
@adapter(INewsItem, IDesignPloneContenttypesLayer)
class NewsDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        get_taxonomy_information("tipologia_notizia", self.context, res)
        return res


@implementer(ISerializeToJsonSummary)
@adapter(IDataset, IDesignPloneContenttypesLayer)
class DatasetDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        get_taxonomy_information("temi_dataset", self.context, res)
        get_taxonomy_information("tipologia_frequenza_aggiornamento", self.context, res)
        get_taxonomy_information("tipologia_licenze", self.context, res)
        return res


@implementer(ISerializeToJsonSummary)
@adapter(IDocumento, IDesignPloneContenttypesLayer)
class DocumentoPubblicoDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        get_taxonomy_information("tipologia_documenti_albopretorio", self.context, res)
        get_taxonomy_information("tipologia_documento", self.context, res)
        get_taxonomy_information("tipologia_licenze", self.context, res)
        get_taxonomy_information("person_life_events", self.context, res)
        get_taxonomy_information("business_events", self.context, res)
        return res


@implementer(ISerializeToJsonSummary)
@adapter(IPratica, IDesignPloneContenttypesLayer)
class PraticaDefaultJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        get_taxonomy_information("tipologia_stati_pratica", self.context, res)
        return res
