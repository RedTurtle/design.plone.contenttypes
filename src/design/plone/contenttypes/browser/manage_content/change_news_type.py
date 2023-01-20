from Acquisition import aq_base
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from Products.Five.browser import BrowserView
from plone import api

from copy import deepcopy
from logging import getLogger

from design.plone.contenttypes import _


logger = getLogger(__name__)


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

        if not old_news_type:
            self.context.plone_utils.addPortalMessage(
                _("The old type field was not populated"), "error"
            )
            return

        if not news_new_type:
            self.context.plone_utils.addPortalMessage(
                _("The new type field was not populated"), "error"
            )
            return

        if news_new_type not in self.news_types():
            self.context.plone_utils.addPortalMessage(
                _("The new News Type was not found between available values"), "error"
            )
            return

        if old_news_type not in self.news_types_in_catalog():
            self.context.plone_utils.addPortalMessage(
                _("The old News Type was not found between available values"), "error"
            )
            return

        for news in api.portal.get_tool("portal_catalog")(
            tipologia_notizia=old_news_type
        ):
            news = news.getObject()
            news.tipologia_notizia = news_new_type
            news.reindexObject(idxs=["tipologia_notizia"])

        # update listings
        for brain in api.portal.get_tool("portal_catalog")():
            item = aq_base(brain.getObject())

            if getattr(item, "blocks", {}):
                blocks = deepcopy(item.blocks)

                if blocks:
                    for block in blocks.values():
                        if block.get("@type", "") == "listing":
                            for query in block.get("querystring", {}).get("query", []):
                                if query["i"] == "tipologia_notizia":
                                    new_values = []
                                    for v in query["v"]:
                                        if v == old_news_type:
                                            v = news_new_type
                                        new_values.append(v)

                                    query["v"] = new_values

                                    logger.info(f"Updated listing {block}")

                    item.blocks = blocks

        self.context.plone_utils.addPortalMessage(
            _("The News Types was changed with success"), "info"
        )
