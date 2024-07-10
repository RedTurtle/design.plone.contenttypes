# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.taxonomy.interfaces import ITaxonomy
from copy import deepcopy
from design.plone.contenttypes import _
from logging import getLogger
from plone import api
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.interface.interfaces import ComponentLookupError

import json


logger = getLogger(__name__)


class View(BrowserView):
    """This view is needed to change the news type on the existent content"""

    def __call__(self, *args, **kwargs):
        self.substitute_news_type()
        return super().__call__(*args, **kwargs)

    def news_types(self):
        try:
            taxonomy = getUtility(
                ITaxonomy, name="collective.taxonomy.tipologia_notizia"
            )
        except ComponentLookupError:
            self.context.plone_utils.addPortalMessage(
                _("Il vocabolario dei valori non è stato trovato"), "error"
            )
            return

        return taxonomy.makeVocabulary(self.request.get("LANGUAGE"))

    def news_types_in_catalog(self):
        types = [news.tipologia_notizia for news in self.news]
        types = list(set(types))
        return types

    def substitute_news_type(self):
        # the only way to get all the tipologia_notizia value is to query news
        # objects not the brains. Taxonomy doesn't index values not present in
        # the taxonomy vocabulary so we have a lot of brain withou tipologia_notizia
        self.brains = api.content.find(portal_type="News Item")
        self.news = [brain.getObject() for brain in self.brains]

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

        for news in self.news:
            if news.tipologia_notizia == old_news_type:
                news.tipologia_notizia = news_new_type
                news.reindexObject(idxs=["tipologia_notizia"])

        # update listings
        for brain in api.portal.get_tool("portal_catalog")():
            item = aq_base(brain.getObject())

            if getattr(item, "blocks", {}):
                blocks = deepcopy(item.blocks)

                if blocks:
                    if isinstance(blocks, str):
                        blocks = json.loads(blocks)
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
