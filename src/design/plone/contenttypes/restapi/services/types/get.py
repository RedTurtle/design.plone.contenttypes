# -*- coding: utf-8 -*-
from plone.restapi.services.types.get import TypesGet as BaseGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
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
        if "properties" in result:
            if "country" in result["properties"]:
                if not result["properties"]["country"].get("default", ""):
                    result["properties"]["country"]["default"] = "380"
            if "city" in result["properties"]:
                if not result["properties"]["city"].get("default", ""):
                    result["properties"]["city"]["default"] = "Roma"
            if "street" in result["properties"]:
                if not result["properties"]["street"].get("default", ""):
                    result["properties"]["street"]["default"] = "Via Liszt, 21"
            if "geolocation" in result["properties"]:
                if not result["properties"]["geolocation"].get("default", {}):
                    result["properties"]["geolocation"]["default"] = {
                        "latitude": 41.8337833,
                        "longitude": 12.4677863,
                    }

        return result
