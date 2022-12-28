# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.utils import get_settings_for_language
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger(__name__)


class BaseVocabulary(object):
    def __call__(self, context):

        values = get_settings_for_language(field=self.field)
        if not values:
            return SimpleVocabulary([])

        terms = [SimpleTerm(value=x, token=x, title=x) for x in values]
        terms.insert(
            0,
            SimpleTerm(value="", token="", title="-- seleziona un valore --"),
        )

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class LeadImageDimension(BaseVocabulary):
    field = "lead_image_dimension"

    def __call__(self, context):

        values = api.portal.get_registry_record(
            self.field, interface=IDesignPloneSettings, default=[]
        )
        if not values:
            return SimpleVocabulary([])

        terms = []
        for value in values:
            token, title = value.split("|")
            terms.append(SimpleTerm(value=token, token=token, title=title))
        return SimpleVocabulary(terms)


LeadImageDimensionFactory = LeadImageDimension()
