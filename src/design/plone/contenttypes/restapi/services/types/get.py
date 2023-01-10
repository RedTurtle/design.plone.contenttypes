# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes.controlpanels.geolocation_defaults import (
    IGeolocationDefaults,
)
from plone import api
from plone.restapi.services.types.get import TypesGet as BaseGet
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class FieldsetsMismatchError(Exception):
    """Exception thrown when we try to reorder fieldsets, but the order list is
    different from the fieldsets returned from Plone
    """


FIELDSETS_ORDER = {
    "Document": [
        "default",
        "testata",
        "settings",
        "correlati",
        "categorization",
        "dates",
        "ownership",
        "layout",
    ],
    "Documento": [
        "default",
        "descrizione",
        "informazioni",
        "settings",
        "correlati",
        "categorization",
        "dates",
        "ownership",
    ],
    "Event": [
        "default",
        "cose",
        "luogo",
        "date_e_orari",
        "costi",
        "contatti",
        "informazioni",
        "correlati",
        "categorization",
        "dates",
        "settings",
        "ownership",
    ],
    "Incarico": [
        "default",
        "informazioni_compensi",
        "date_e_informazioni",
    ],
    "News Item": [
        "default",
        "dates",
        "correlati",
        "categorization",
        "settings",
        "ownership",
    ],
    "Modulo": [
        "default",
        "settings",
        "correlati",
        "categorization",
        "dates",
        "ownership",
    ],
    "Pagina Argomento": [
        "default",
        "informazioni",
        "correlati",
        "categorization",
        "dates",
        "settings",
        "layout",
        "ownership",
    ],
    "Persona": [
        "default",
        "ruolo",
        "contatti",
        "documenti",
        "informazioni",
        "correlati",
        "categorization",
        "dates",
        "ownership",
        "settings",
    ],
    "PuntoDiContatto": [
        "default",
    ],
    "Servizio": [
        "default",
        "cose",
        "a_chi_si_rivolge",
        "accedi_al_servizio",
        "cosa_serve",
        "costi_e_vincoli",
        "tempi_e_scadenze",
        "casi_particolari",
        "contatti",
        "documenti",
        "link_utili",
        "informazioni",
        "correlati",
        "categorization",
        "settings",
        "ownership",
        "dates",
    ],
    "UnitaOrganizzativa": [
        "default",
        "cosa_fa",
        "struttura",
        "persone",
        "contatti",
        "correlati",
        "categorization",
        "informazioni",
        "settings",
        "ownership",
        "dates",
    ],
    "Venue": [
        "default",
        "descrizione",
        "accesso",
        "dove",
        "orari",
        "contatti",
        "informazioni",
        "settings",
        "correlati",
        "categorization",
    ],
}


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
    def customize_document_schema(self, result):
        fields = ["image", "image_caption", "preview_image", "preview_caption"]
        for fieldset in result.get("fieldsets", []):
            if fieldset.get("id", "") == "testata":
                fieldset["fields"] = fields + fieldset["fields"]
            if fieldset.get("id", "") == "default":
                fieldset["fields"] = [x for x in fieldset["fields"] if x not in fields]
        return result

    def customize_persona_schema(self, result):
        if "title" in result["properties"]:
            msgid = _("Nome e Cognome", default="Nome e cognome")
            result["properties"]["title"]["title"] = translate(
                msgid, context=self.request
            )
        return result

    def customize_venue_schema(self, result):
        """
        Unico modo per spostare il campo "notes"
        """
        result.get("required").append("description")
        result.get("required").append("image")
        result.get("required").append("street")
        result.get("required").append("city")
        result.get("required").append("zip_code")
        result.get("required").append("geolocation")

        if "properties" in result:
            if "country" in result["properties"]:
                if not result["properties"]["country"].get("default", ""):
                    result["properties"]["country"]["default"] = {
                        "title": "Italia",
                        "token": "380",
                    }
            if "city" in result["properties"]:
                if not result["properties"]["city"].get("default", ""):
                    result["properties"]["city"][
                        "default"
                    ] = api.portal.get_registry_record(
                        "city", interface=IGeolocationDefaults
                    )
            if "zip_code" in result["properties"]:
                if not result["properties"]["zip_code"].get("default", ""):
                    result["properties"]["zip_code"][
                        "default"
                    ] = api.portal.get_registry_record(
                        "zip_code", interface=IGeolocationDefaults
                    )

            if "street" in result["properties"]:
                if not result["properties"]["street"].get("default", ""):
                    result["properties"]["street"][
                        "default"
                    ] = api.portal.get_registry_record(
                        "street", interface=IGeolocationDefaults
                    )

            if "geolocation" in result["properties"]:
                if not result["properties"]["geolocation"].get("default", {}):
                    result["properties"]["geolocation"]["default"] = eval(
                        api.portal.get_registry_record(
                            "geolocation", interface=IGeolocationDefaults
                        )
                    )

        for fieldset in result["fieldsets"]:
            if fieldset.get("id") == "default" and "notes" in fieldset["fields"]:
                fieldset["fields"].remove("notes")
            if fieldset.get("id") == "dove" and "notes" not in fieldset["fields"]:
                fieldset["fields"].append("notes")

        return result

    def customize_versioning_fields_fieldset(self, result):
        """
        Unico modo per spostare i campi del versioning.
        Perché changeNotes ha l'order after="*" che vince su tutto.
        """
        versioning_fields = ["versioning_enabled", "changeNote"]
        for field in versioning_fields:
            found = False
            for fieldset in result["fieldsets"]:
                if fieldset.get("id") == "default" and field in fieldset["fields"]:
                    found = True
                    fieldset["fields"].remove(field)
                if fieldset.get("id") == "settings" and found:
                    fieldset["fields"].append(field)

        return result

    def customize_servizio_schema(self, result):
        result.get("required").append("description")
        return result

    def customize_uo_schema(self, result):
        result.get("required").append("description")
        versioning_fields = ["contact_info"]
        for field in versioning_fields:
            for fieldset in result["fieldsets"]:
                if fieldset.get("id") == "contatti" and field in fieldset["fields"]:
                    fieldset["fields"].remove(field)
                    fieldset["fields"].insert(0, field)
        return result

    def customize_news_schema(self, result):
        result.get("required").append("description")
        if self.context.portal_type == "News Item":
            # we are in a news and not in container
            review_state = self.context.portal_workflow.getInfoFor(
                self.context, "review_state"
            )
            if review_state == "published":
                result.get("required").append("effective")

        return result

    def customize_documento_schema(self, result):
        result.get("required").append("description")
        return result

    def reply(self):
        result = super(TypesGet, self).reply()

        if "fieldsets" in result:
            result["fieldsets"] = self.reorder_fieldsets(original=result["fieldsets"])
        pt = self.request.PATH_INFO.split("/")[-1]

        # be careful: result could be dict or list. If list it will not
        # contains title. And this is ok for us.
        pt = self.request.PATH_INFO.split("/")[-1]

        if "title" in result:
            if pt == "Persona":
                result = self.customize_persona_schema(result)
            if pt == "Venue":
                result = self.customize_venue_schema(result)
            if pt == "Document":
                result = self.customize_document_schema(result)
            if pt == "Servizio":
                result = self.customize_servizio_schema(result)
            if pt == "UnitaOrganizzativa":
                result = self.customize_uo_schema(result)
            if pt == "News Item":
                result = self.customize_news_schema(result)
            if pt == "Documento":
                result = self.customize_documento_schema(result)
            result = self.customize_versioning_fields_fieldset(result)
        return result

    def get_order_by_type(self, portal_type):
        return [x for x in FIELDSETS_ORDER.get(portal_type, [])]

    def reorder_fieldsets(self, original):
        pt = self.request.PATH_INFO.split("/")[-1]
        order = self.get_order_by_type(portal_type=pt)
        if not order:
            # no match
            return original
        original_fieldsets = [x["id"] for x in original]

        for fieldset_id in original_fieldsets:
            # if some fieldsets comes from additional addons (not from the
            # base ones), then append them to the order list.
            if fieldset_id not in order:
                order.append(fieldset_id)

        # create a new fieldsets list with the custom order
        new = []
        for id in order:
            for fieldset in original:
                if fieldset["id"] == id:
                    new.append(fieldset)
        if not new:
            # no match
            return original
        return new
