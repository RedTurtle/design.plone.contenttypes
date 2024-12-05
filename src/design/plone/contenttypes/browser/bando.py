"""
This is a customization for original view. in design.plone.contenttypes
we allow folder deepening to contain also Modulo CT and we need to
handle it properly

I know it would be better to refactor redturtle.bandi to make
retrieveContentsOfFolderDeepening smaller and have "mini" methods
to retrieve information. This will be done maybe in future
"""

from design.plone.contenttypes.behaviors.multi_file import IMultiFileSchema
from plone import api
from plone.restapi.interfaces import IFieldSerializer
from redturtle.bandi.browser.bando import BandoView as BaseBandoView
from redturtle.bandi.browser.bando import IBandoView
from zope.component import queryMultiAdapter
from zope.interface import implementer

try:
    from plone.restapi.serializer.utils import uid_to_url
    from plone.restapi.serializer.converters import json_compatible

    HAS_PLONERESTAPI = True
except ImportError:
    HAS_PLONERESTAPI = False


fields = [
    "file_principale",
    "formato_alternativo_1",
    "formato_alternativo_2",
]


@implementer(IBandoView)
class BandoView(BaseBandoView):
    def retrieveContentsOfFolderDeepening(self, path_dfolder):
        """Retrieves all objects contained in Folder Deppening"""

        values = []
        brains = self.context.portal_catalog(
            path={"query": path_dfolder, "depth": 1},
            sort_on="getObjPositionInParent",
        )
        siteid = api.portal.get().getId()
        for brain in brains:
            if not brain.getPath() == path_dfolder and not brain.exclude_from_nav:
                effective = brain.effective
                if effective.year() == 1969:
                    # content not yet published
                    effective = None
                dictfields = dict(
                    title=brain.Title,
                    description=brain.Description,
                    url=brain.getURL(),
                    path=brain.getPath(),
                    effective=effective,
                    modified=brain.modified,
                )
                if brain.Type == "Link":
                    dictfields["url"] = brain.getRemoteUrl
                    # resolve /resolveuid/... to url
                    # XXX: ma qui non funziona perchè il path è /Plone/resolveuid/...
                    # mentre la regex di uid_to_url si aspetta /resolveuid/... o
                    # ../resolveuid/...
                    # dictfields["url"] = uid_to_url(dictfields["url"])
                    # XXX: bug di Link ? in remoteUrl per i link interni nei brain
                    # c'è il path completo (con /Plone) invece che una url
                    # probabilmente legato al fatto che i link ora sono creati via
                    # api e non da interfaccia Plone (?)
                    if dictfields["url"].startswith(f"/{siteid}"):
                        dictfields["url"] = dictfields["url"][len(siteid) + 1 :]
                        if HAS_PLONERESTAPI:
                            dictfields["url"] = uid_to_url(dictfields["url"])
                elif brain.Type == "File":
                    obj_file = brain.getObject().file
                    if obj_file:
                        dictfields[
                            "url"
                        ] = f"{brain.getURL()}/@@download/file/{obj_file.filename}"  # noqa E501
                        obj_size = obj_file.size
                        dictfields["filesize"] = self.getSizeString(obj_size)
                elif brain.Type == "Modulo":
                    obj = brain.getObject()
                    for field in fields:
                        field_obj = IMultiFileSchema[field]
                        serializer = queryMultiAdapter(
                            (field_obj, obj, self.request), IFieldSerializer
                        )
                        value = serializer()
                        dictfields[field] = value

                # else:
                #     dictfields["url"] = brain.getURL() + "/view"
                dictfields["content-type"] = brain.mime_type
                # icon = getMultiAdapter((self.context, self.request, obj), IContentIcon)
                # dictfields['icon'] = icon.html_tag()
                dictfields["type"] = brain.Type

                if HAS_PLONERESTAPI:
                    dictfields = json_compatible(dictfields)
                values.append(dictfields)

        return values
