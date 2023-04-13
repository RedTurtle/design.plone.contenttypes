from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import SearchableText_blocks
from Products.CMFPlone.utils import safe_hasattr
from Products.Five import BrowserView
from zope.interface import implementer


FLAG = '<i class="fa-solid fa-check"></i>'

FIELDS = [
    "title",
    "description",
    "condizioni_di_servizio",
    "tassonomia_argomenti",
    "a_chi_si_rivolge",
    "come_si_fa",
    "cosa_si_ottiene",
    "canale_fisico",
    "cosa_serve",
    "tempi_e_scadenze",
    "ufficio_responsabile",
    "contact_info",
]


def text_in_block(blocks):
    @implementer(IBlocks)
    class FakeObject(object):
        """
        We use a fake object to use SearchableText Indexer
        """

        def Subject(self):
            return ""

        def __init__(self, blocks, blocks_layout):
            self.blocks = blocks
            self.blocks_layout = blocks_layout
            self.id = ""
            self.title = ""
            self.description = ""

    if not blocks:
        return None

    fakeObj = FakeObject(blocks.get("blocks", ""), blocks.get("blocks_layout", ""))
    return SearchableText_blocks(fakeObj)()


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
                    "data": {
                        "title": getattr(servizio, "title") and FLAG or "",
                        "description": getattr(servizio, "description", None)
                        and FLAG
                        or "",
                        "condizioni_di_servizio": getattr(
                            servizio, "condizioni_di_servizio", None
                        )
                        and FLAG
                        or "",
                        "tassonomia_argomenti": getattr(
                            servizio, "tassonomia_argomenti", None
                        )
                        and FLAG
                        or "",
                        "a_chi_si_rivolge": text_in_block(
                            getattr(servizio, "a_chi_si_rivolge", None)
                        )
                        and FLAG
                        or "",
                        "come_si_fa": text_in_block(
                            getattr(servizio, "come_si_fa", None)
                        )
                        and FLAG
                        or "",
                        "cosa_si_ottiene": text_in_block(
                            getattr(servizio, "cosa_si_ottiene", None)
                        )
                        and FLAG
                        or "",
                        "canale_fisico": getattr(servizio, "canale_fisico", None)
                        and FLAG
                        or "",
                        "cosa_serve": text_in_block(
                            getattr(servizio, "cosa_serve", None)
                        )
                        and FLAG
                        or "",
                        "tempi_e_scadenze": text_in_block(
                            getattr(servizio, "tempi_e_scadenze", None)
                        )
                        and FLAG
                        or "",
                        "ufficio_responsabile": getattr(
                            servizio, "ufficio_responsabile", None
                        )
                        and FLAG
                        or "",
                        "contact_info": getattr(servizio, "contact_info", None)
                        and FLAG
                        or "",
                    },
                }
            )
        results = dict(sorted(results.items()))
        for key in results:
            results[key]["children"].sort(key=lambda x: x["title"])

        return results
