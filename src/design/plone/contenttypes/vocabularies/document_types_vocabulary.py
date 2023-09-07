# -*- coding: utf-8 -*-

# from plone import api
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
class DocumentTypesVocabulary(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem("documenti_albo_pretorio", _("Documenti albo pretorio")),
            VocabItem("modulistica", _("Modulistica")),
            VocabItem(
                "documento_funzionamento_interno",
                _("Documento funzionamento interno"),
            ),
            VocabItem("atto_normativo", _("Atto normativo")),
            VocabItem("accordo_tra_enti", _("Accordo tra enti")),
            VocabItem(
                "documento_attivita_politica",
                _("Documento attivita politica"),
            ),
            VocabItem(
                "documento_tecnico_di_supporto",
                _("Documento (tecnico) di supporto"),
            ),
            VocabItem("istanza", _("Istanza")),
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
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


DocumentTypesVocabularyFactory = DocumentTypesVocabulary()
