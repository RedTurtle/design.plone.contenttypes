# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
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
class Mockup(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem("sony-a7r-iii", _("Sony Aplha 7R III")),
            VocabItem("canon-5d-iv", _("Canon 5D IV")),
            VocabItem("pippo", _("Pippo")),
            VocabItem("pluto", _("Pluto")),
            VocabItem("paperino", _("Paperino")),
            VocabItem("giovanni", _("Giovanni")),
        ]

        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(value=item.token, token=str(item.token), title=item.value)
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


MockupFactory = Mockup()
