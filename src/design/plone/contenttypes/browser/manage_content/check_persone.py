from DateTime import DateTime
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.styles import Font
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import SearchableText_blocks
from Products.Five import BrowserView
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.globalrequest import getRequest
from zope.component import getUtility, getMultiAdapter
from zope.intid.interfaces import IIntIds
from zc.relation.interfaces import ICatalog
from zope.security import checkPermission
from plone.restapi.interfaces import ISerializeToJsonSummary

import io


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


class CheckPersone(BrowserView):
    cds = None

    def is_anonymous(self):
        return api.user.is_anonymous()

    def get_relations(self, obj, field):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        relations = catalog.findRelations(
            dict(
                to_id=intids.getId(obj),
                from_attribute=field,
            )
        )
        return relations, intids

    def get_related_objects(self, obj, field):
        """ """
        items = []
        relations, intids = self.get_relations(obj, field)

        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission("zope2.View", obj):
                summary = getMultiAdapter(
                    (obj, getRequest()), ISerializeToJsonSummary
                )()
                items.append(summary)
        return sorted(items, key=lambda k: k["title"])

    def information_dict(self, persona):
        relations = self.get_related_objects(persona, "organizzazione_riferimento")
        return {
            "title": getattr(persona, "title"),
            "has_related_uo": bool(relations),
            "organizzazione_riferimento": relations,
        }

    def plone2volto(self, url):
        portal_url = api.portal.get().absolute_url()
        frontend_domain = api.portal.get_registry_record(
            "volto.frontend_domain", default=""
        )
        if frontend_domain and url.startswith(portal_url):
            return url.replace(portal_url, frontend_domain, 1)
        return url

    def get_persone(self):
        if self.is_anonymous():
            return []
        pc = api.portal.get_tool("portal_catalog")

        # show_inactive ha sempre avuto una gestione... particolare! aggiungo ai
        # kw effectiveRange = DateTime() che è quello che fa Products.CMFPlone
        # nel CatalogTool.py
        query = {
            "portal_type": "Persona",
            # "review_state": "published",
        }
        brains = pc(query, **{"effectiveRange": DateTime()})
        results = {}
        for brain in brains:
            persona = brain.getObject()

            information_dict = self.information_dict(persona)

            import pdb; pdb.set_trace()
            if not information_dict.get('has_related_uo'):
                continue

            parent = persona.aq_inner.aq_parent
            if parent.title not in results:
                results[parent.title] = {
                    "url": self.plone2volto(parent.absolute_url()),
                    "children": [],
                }

            results[parent.title]["children"].append(
                {
                    "title": persona.title,
                    "url": self.plone2volto(persona.absolute_url()),
                    "data": {
                        "title": information_dict.get("title"),
                        "has_related_uo": information_dict.get("has_related_uo")
                        and FLAG
                        or "",
                        "organizzazione_riferimento": information_dict.get(
                            "organizzazione_riferimento"
                        )
                    },
                }
            )

        results = dict(sorted(results.items()))
        for key in results:
            results[key]["children"].sort(key=lambda x: x["title"])
        return results


class DownloadCheckPersone(CheckPersone):
    CT = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def __call__(self):
        HEADER = [
            "Titolo",
            "Ha organizzazioni di riferimento",
            "Unità org. di riferimento",
        ]
        import pdb; pdb.set_trace()

        EMPTY_ROW = [""] * 3

        persone = self.get_persone()
        data = []
        for category in persone:
            data.append([category] + [""] * 2 + [persone[category]["url"]])
            data.append(HEADER)
            for persona in persone[category]["children"]:
                dati_persona = [
                    persona["title"],
                    persona["data"]["description"] and "V" or "",
                    persona["data"]["tassonomia_argomenti"] and "V" or "",

                    persona["url"],
                ]

                data.append(dati_persona)
            data.append(EMPTY_ROW)
            data.append(EMPTY_ROW)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Persone"
        link_font = Font(underline="single", color="0563C1")
        link_fill = PatternFill(fill_type="solid", fgColor="DDDDDD")
        alignment = Alignment(horizontal="center", vertical="top")

        for i, row in enumerate(data, start=1):
            have_url = row[0] != "Titolo" and bool(row[0])
            if have_url:
                url = row.pop()

            sheet.append(row)

            if row[0] == "Titolo":
                for index, cell in enumerate(sheet[i]):
                    cell.fill = link_fill
                    if index != 0:
                        column_letter = get_column_letter(cell.column)
                        sheet.column_dimensions[column_letter].width = 20

            if have_url:
                for index, cell in enumerate(sheet[i]):
                    if index == 0:
                        cell = sheet.cell(row=i, column=1)
                        cell.font = link_font
                        cell.alignment = cell.alignment.copy(wrapText=True)
                        cell.hyperlink = url
                        column_letter = get_column_letter(cell.column)
                        sheet.column_dimensions[column_letter].width = 40
                    else:
                        cell.alignment = alignment

        bytes_io = io.BytesIO()
        workbook.save(bytes_io)
        data = bytes_io.getvalue()
        self.request.response.setHeader("Content-Length", len(data))
        self.request.RESPONSE.setHeader("Content-Type", self.CT)
        self.request.response.setHeader(
            "Content-Disposition",
            "attachment; filename=check_persone.xlsx",
        )
        return data
