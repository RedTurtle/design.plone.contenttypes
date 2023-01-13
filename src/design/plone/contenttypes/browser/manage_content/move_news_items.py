from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from plone import api
from plone.memoize import ram
from Products.Five import BrowserView

from plone.app.contenttypes import _

import time
import logging
import pkg_resources


JS_TEMPLATE = (
    "{portal_url}/++plone++design.plone.contenttypes/js/{name}.js?v={version}"  # noqa
)

logger = logging.getLogger(__name__)


class View(BrowserView):
    def __call__(self, *args, **kwargs):
        self.move_data()
        return super().__call__(*args, **kwargs)

    def move_data(self):
        if self.request.form.get("move", ""):
            path = self.request.form.get("to_path")
            if path:
                move_to = api.content.get(path)
                if not move_to:
                    self.context.plone_utils.addPortalMessage(
                        _("Indicated path is not valid"), "error"
                    )
                    return

                for name, value in self.request.form.items():
                    if value != "on":
                        continue

                    item = api.content.get(UID=name)

                    if item:
                        api.content.move(item, move_to)

                self.context.plone_utils.addPortalMessage(
                    _("Items moved with success"), "info"
                )
            else:
                self.context.plone_utils.addPortalMessage(
                    _("The path was not indicated"), "warning"
                )

    def news_results(self):
        news_type = self.request.form.get("news_type", "")
        path = self.request.form.get("path", "")
        query = {"portal_type": "News Item"}

        if news_type:
            query["tipologia_notizia"] = news_type
        if path:
            query["path"] = path

        return api.portal.get_tool("portal_catalog")(**query)

    def news_types(self):
        return getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_notizia"
        )(self.context)

    @ram.cache(lambda *args: time.time() // (60 * 60))
    def get_version(self):
        return pkg_resources.get_distribution("design.plone.contenttypes").version

    def get_resource_js(self, name="move_content"):
        return JS_TEMPLATE.format(
            portal_url=api.portal.get().absolute_url(),
            name=name,
            version=self.get_version(),
        )
