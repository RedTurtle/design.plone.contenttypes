from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import SearchableText_blocks
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
    cds = None

    def is_anonymous(self):
        return api.user.is_anonymous()

    def information_dict(self, servizio):
        return {
            "title": getattr(servizio, "title"),
            "description": getattr(servizio, "description", None),
            "condizioni_di_servizio": getattr(servizio, "condizioni_di_servizio", None),
            "tassonomia_argomenti": getattr(servizio, "tassonomia_argomenti", None),
            "a_chi_si_rivolge": text_in_block(
                getattr(servizio, "a_chi_si_rivolge", None)
            ),
            "come_si_fa": text_in_block(getattr(servizio, "come_si_fa", None)),
            "cosa_si_ottiene": text_in_block(
                getattr(servizio, "cosa_si_ottiene", None)
            ),
            "canale_fisico": getattr(servizio, "canale_fisico", None),
            "cosa_serve": text_in_block(getattr(servizio, "cosa_serve", None)),
            "tempi_e_scadenze": text_in_block(
                getattr(servizio, "tempi_e_scadenze", None)
            ),
            "ufficio_responsabile": getattr(servizio, "ufficio_responsabile", None),
            "contact_info": getattr(servizio, "contact_info", None),
        }

    def get_servizi(self):
        if self.is_anonymous():
            return []
        pc = api.portal.get_tool("portal_catalog")
        brains = pc(portal_type="Servizio")
        results = {}
        for brain in brains:
            servizio = brain.getObject()
            # if safe_hasattr(servizio, "condizioni_di_servizio") and getattr(
            #     servizio, "condizioni_di_servizio"
            # ):
            #     continue

            # Se chiediamo di vedere anche le condizioni di servizio, lo teniamo
            self.cds = self.request.get("condizioni_di_servizio", None)
            information_dict = self.information_dict(servizio)
            if not self.cds:
                del information_dict["condizioni_di_servizio"]

            if all(information_dict.values()):
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
                        "title": information_dict.get("title") and FLAG or "",
                        "description": information_dict.get("description")
                        and FLAG
                        or "",
                        "condizioni_di_servizio": information_dict.get(
                            "condizioni_di_servizio"
                        )
                        and FLAG
                        or "",
                        "tassonomia_argomenti": information_dict.get(
                            "tassonomia_argomenti"
                        )
                        and FLAG
                        or "",
                        "a_chi_si_rivolge": information_dict.get("a_chi_si_rivolge")
                        and FLAG
                        or "",
                        "come_si_fa": information_dict.get("come_si_fa") and FLAG or "",
                        "cosa_si_ottiene": information_dict.get("cosa_si_ottiene")
                        and FLAG
                        or "",
                        "canale_fisico": information_dict.get("canale_fisico")
                        and FLAG
                        or "",
                        "cosa_serve": information_dict.get("cosa_serve") and FLAG or "",
                        "tempi_e_scadenze": information_dict.get("tempi_e_scadenze")
                        and FLAG
                        or "",
                        "ufficio_responsabile": information_dict.get(
                            "ufficio_responsabile"
                        )
                        and FLAG
                        or "",
                        "contact_info": information_dict.get("contact_info")
                        and FLAG
                        or "",
                    },
                }
            )
        results = dict(sorted(results.items()))
        for key in results:
            results[key]["children"].sort(key=lambda x: x["title"])

        return results
