from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from Products.Five.browser import BrowserView
from plone import api

from design.plone.contenttypes import _


class View(BrowserView):
    """This view is needed to change the news type on the existent content"""

    def __call__(self, *args, **kwargs):
        self.substitute_news_type()
        return super().__call__(*args, **kwargs)

    def news_types(self):
        return getUtility(
            IVocabularyFactory, "design.plone.vocabularies.tipologie_notizia"
        )(self.context)

    def news_types_in_catalog(self):
        return api.portal.get_tool("portal_catalog").uniqueValuesFor(
            "tipologia_notizia"
        )

    def substitute_news_type(self):
        if not self.request.form.get("substitute", ""):
            return

        old_news_type = self.request.form.get("news_type_in_catalog", "")
        news_new_type = self.request.form.get("news_type_portal", "")

        if not old_news_type or not news_new_type:
            self.context.plone_utils.addPortalMessage(_("Not enaught data"), "error")
            return

        if (
            not news_new_type in self.news_types()
            or not old_news_type in self.news_types_in_catalog()
        ):
            self.context.plone_utils.addPortalMessage(_("Bad data was send"), "error")

        news_to_update = [
            i.getObject()
            for i in api.portal.get_tool("portal_catalog")(
                tipologia_notizia=old_news_type
            )
        ]

        for news in news_to_update:
            news.tipologia_notizia = news_new_type
            news.reindexObject(idxs=["tipologia_notizia"])

        return
