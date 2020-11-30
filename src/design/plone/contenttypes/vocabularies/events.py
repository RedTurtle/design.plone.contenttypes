# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from plone.app.vocabularies.catalog import KeywordsVocabulary


@implementer(IVocabularyFactory)
class EventLocationVocabulary(KeywordsVocabulary):

    keyword_index = 'event_location'


EventLocationVocabularyFactory = EventLocationVocabulary()
