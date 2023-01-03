# -*- coding: utf-8 -*-
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class ArgomentiVocabulary(object):
    """ """

    def __call__(self, context):
        values = set(
            [x.Title for x in api.content.find(portal_type="Pagina Argomento")]
        )
        values = sorted(list(values))
        terms = [SimpleTerm(value="", token="", title="-- seleziona un valore --")]
        for value in values:
            terms.append(SimpleTerm(value=value, token=value, title=value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class ArgomentiUIDVocabulary(object):
    """ """

    def __call__(self, context):
        arguments = api.content.find(
            portal_type="Pagina Argomento", sort_on="sortable_title"
        )
        terms = [SimpleTerm(value="", token="", title="-- seleziona un valore --")]
        for x in arguments:
            terms.append(SimpleTerm(value=x.UID, token=x.UID, title=x.Title))

        return SimpleVocabulary(terms)


ArgomentiVocabularyFactory = ArgomentiVocabulary()
ArgomentiUIDVocabularyFactory = ArgomentiUIDVocabulary()
