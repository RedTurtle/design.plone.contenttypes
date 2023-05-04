from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import SearchableText_blocks
from Products.Five import BrowserView
from zope.interface import implementer
from plone.volto.interfaces import IVoltoSettings


FLAG = '<i class="fa-solid fa-check"></i>'


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

    def get_canale_accesso_info(self, servizio):
        canale_fisico = getattr(servizio, "canale_fisico", None)
        canale_digitale = text_in_block(getattr(servizio, "canale_digitale", None))
        canale_digitale_link = getattr(servizio, "canale_digitale_link", None)
        if canale_digitale and canale_digitale_link and canale_fisico:
            return "D e F"
        elif canale_digitale and canale_digitale_link:
            return "D"
        elif canale_fisico:
            return "F"
        # elif canale_digitale or canale_digitale_link:
        #     return "&frac12;D"
        return None

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
            "canale_accesso": self.get_canale_accesso_info(servizio),
            "cosa_serve": text_in_block(getattr(servizio, "cosa_serve", None)),
            "tempi_e_scadenze": text_in_block(
                getattr(servizio, "tempi_e_scadenze", None)
            ),
            "ufficio_responsabile": getattr(servizio, "ufficio_responsabile", None),
        }

    def plone2volto(self, url):
        navroot_url = self.portal_state().navigation_root_url(self.context)
        frontend_domain = api.portal.get_registry_record('frontend_domain', interface=IVoltoSettings, default=u'bar')
        # frontend_domain = api.portal.get_registry_record('volto.frontend_domain', interface=IVoltoSettings, default=u'bar')
        if frontend_domain and url.startswith(navroot_url):
            return url.replace(navroot_url, frontend_domain, 1)
        return url

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
                    "url": self.plone2volto(parent.absolute_url()),
                    "children": [],
                }

            results[parent.title]["children"].append(
                {
                    "title": servizio.title,
                    "url": self.plone2volto(servizio.absolute_url()),
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
                        "canale_accesso": information_dict.get("canale_accesso") or "",
                        "cosa_serve": information_dict.get("cosa_serve") and FLAG or "",
                        "tempi_e_scadenze": information_dict.get("tempi_e_scadenze")
                        and FLAG
                        or "",
                        "ufficio_responsabile": information_dict.get(
                            "ufficio_responsabile"
                        )
                        and FLAG
                        or "",
                    },
                }
            )

        results = dict(sorted(results.items()))
        for key in results:
            results[key]["children"].sort(key=lambda x: x["title"])
        return results
