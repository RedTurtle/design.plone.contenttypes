# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class PeopleVocabulary(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        portal_catalog = api.portal.get_tool("portal_catalog")
        results = portal_catalog.searchResults(portal_type="Persona")

        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]
        # create a list of SimpleTerm items:
        terms = []
        for result in results:
            brain = result.getObject()
            uid = brain.UID()
            terms.append(SimpleTerm(value=uid, token=uid, title=brain.title))
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


PeopleVocabularyFactory = PeopleVocabulary()


@implementer(IVocabularyFactory)
class RuoliPersona(object):
    """ """

    def __call__(self, context):
        portal_catalog = api.portal.get_tool("portal_catalog")
        unique_values = portal_catalog.uniqueValuesFor("ruolo")
        terms = []
        for unique_value in unique_values:
            terms.append(
                SimpleTerm(value=unique_value, token=unique_value, title=unique_value)
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


RuoliPersonaFactory = RuoliPersona()
