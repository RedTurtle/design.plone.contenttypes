# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite


class ReferencesVocabulary(object):

    INDEX = ""

    def get_all_index_values(self):
        index = self.catalog._catalog.getIndex(self.INDEX)
        return list(index.uniqueValues())

    def __call__(self, registry=None):
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog", None)
        if self.catalog is None:
            return SimpleVocabulary([])
        values = self.get_all_index_values()
        brains = self.catalog(UID=values)
        terms = []
        for brain in brains:
            terms.append(SimpleTerm(brain.UID, brain.UID, safe_unicode(brain.Title)))
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class EventLocationVocabulary(ReferencesVocabulary):

    INDEX = "event_location"


@implementer(IVocabularyFactory)
class OfficeLocationVocabulary(ReferencesVocabulary):

    INDEX = "ufficio_responsabile"


@implementer(IVocabularyFactory)
class UOLocationVocabulary(ReferencesVocabulary):

    INDEX = "uo_location"


EventLocationVocabularyFactory = EventLocationVocabulary()
OfficeLocationVocabularyFactory = OfficeLocationVocabulary()
UOLocationVocabularyFactory = UOLocationVocabulary()
