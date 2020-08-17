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


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
    def customize_persona_schema(self, result):
        msgid = _(u"Nome e Cognome", default="Nome e cognome")
        result["properties"]["title"]["title"] = translate(
            msgid, context=self.request
        )
        if "fieldsets" in result:
            ids = [x["id"] for x in result["fieldsets"]]
            correlati_index = ids.index("correlati")
            categorization_index = ids.index("categorization")
            result["fieldsets"].insert(
                correlati_index + 1,
                result["fieldsets"].pop(categorization_index),
            )
        return result

    def reply(self):
        result = super(TypesGet, self).reply()

        if "fieldsets" in result:
            ids = [x["id"] for x in result["fieldsets"]]
            if "correlati" in ids:
                #  move correlati before categorization
                default_index = ids.index("default")
                correlati_index = ids.index("correlati")
                result["fieldsets"].insert(
                    default_index + 1, result["fieldsets"].pop(correlati_index)
                )
            if "testata" in ids:
                #  move testata after default
                default_index = ids.index("default")
                testata_index = ids.index("testata")
                result["fieldsets"].insert(
                    default_index + 1, result["fieldsets"].pop(testata_index)
                )
            if "default" in ids:
                # move sedi after geolocation
                idx = ids.index("default")
                if (
                    "sedi" in result["fieldsets"][idx]["fields"]
                    and "geolocation" in result["fieldsets"][idx]["fields"]
                ):
                    geo_index = result["fieldsets"][idx]["fields"].index(
                        "geolocation"
                    )
                    sedi_index = result["fieldsets"][idx]["fields"].index(
                        "sedi"
                    )
                    result["fieldsets"][idx]["fields"].insert(
                        geo_index,
                        result["fieldsets"][idx]["fields"].pop(sedi_index),
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
        # be careful: result could be dict or list. If list it will not contains
        # title. And this is ok for us.
        if "title" in result and result["title"] == "Persona":
            result = self.customize_persona_schema(result)
        return result
