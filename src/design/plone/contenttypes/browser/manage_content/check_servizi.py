from plone import api
from Products.Five import BrowserView
from Products.CMFPlone.utils import safe_hasattr


class CheckServizi(BrowserView):
    def is_anonymous(self):
        return api.user.is_anonymous()

    def get_servizi(self):
        if self.is_anonymous():
            return []
        pc = api.portal.get_tool("portal_catalog")
        brains = pc(portal_type="Servizio")
        results = {}
        for brain in brains:
            servizio = brain.getObject()
            if safe_hasattr(servizio, "condizioni_di_servizio") and getattr(
                servizio, "condizioni_di_servizio"
            ):
                continue
            parent = servizio.aq_inner.aq_parent
            if parent.title not in results:
                results[parent.title] = {
                    "url": parent.absolute_url().replace("/api/", "/"),
                    "children": [],
                }
            results[parent.title]["children"].append(
                {
                    "title": servizio.title,
                    "url": servizio.absolute_url().replace("/api/", "/"),
                }
            )
        results = dict(sorted(results.items()))
        for key in results:
            results[key]["children"].sort(key=lambda x: x["title"])

        return results
