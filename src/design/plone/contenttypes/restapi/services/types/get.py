# -*- coding: utf-8 -*-
from plone.restapi.services.types.get import TypesGet as BaseGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from design.plone.contenttypes.controlpanels.geolocation_defaults import (
    IGeolocationDefaults,
)
from zope.i18n import translate
from plone import api
from design.plone.contenttypes import _


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
    "Event": [
        "default",
        "date_evento",
        "partecipanti",
        "luogo",
        "costi",
        "contatti",
        "informazioni",
        "correlati",
        "categorization",
        "dates",
        "settings",
        "layout",
        "ownership",
    ],
    "News Item": [
        "default",
        "correlati",
        "categorization",
        "dates",
        "ownership",
        "settings",
        "layout",
    ],
    "Persona": [
        "default",
        "informazioni",
        "correlati",
        "categorization",
        "settings",
        "ownership",
        "dates",
    ],
    "Servizio": [
        "default",
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
        "dove",
        "informazioni",
        "correlati",
        "settings",
        "ownership",
        "dates",
        "categorization",
    ],
    "Venue": ["default", "dove", "contatti", "informazioni", "categorization"],
}


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
    def customize_persona_schema(self, result):
        msgid = _(u"Nome e Cognome", default="Nome e cognome")
        result["properties"]["title"]["title"] = translate(
            msgid, context=self.request
        )
        return result

    def reply(self):
        result = super(TypesGet, self).reply()

        if "fieldsets" in result:
            result["fieldsets"] = self.reorder_fieldsets(
                original=result["fieldsets"]
            )

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

        # be careful: result could be dict or list. If list it will not
        # contains title. And this is ok for us.
        pt = self.request.PATH_INFO.split("/")[-1]

        if "title" in result and pt == "Persona":
            result = self.customize_persona_schema(result)
        return result

    def reorder_fieldsets(self, original):
        pt = self.request.PATH_INFO.split("/")[-1]
        order = FIELDSETS_ORDER.get(pt, [])
        if not order:
            # no match
            return original
        actual = [x["id"] for x in original]
        if set(order) != set(actual):
            # list mismatch
            raise FieldsetsMismatchError(
                "Fieldset mismatch for {}. expected: {} get: {}".format(
                    pt, order, actual
                )
            )
        new = []
        for id in order:
            for fieldset in original:
                if fieldset["id"] == id:
                    new.append(fieldset)
        if not new:
            # no match
            new = original
        return new
