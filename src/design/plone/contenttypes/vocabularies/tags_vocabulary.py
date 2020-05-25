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
class TagsVocabulary(object):
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(u"anziano", _(u"Anziano")),
            VocabItem(u"fanciullo", _(u"Fanciullo")),
            VocabItem(u"giovane", _(u"Giovane")),
            VocabItem(u"famiglia", _(u"Famiglia")),
            VocabItem(u"studente", _(u"Studente")),
            VocabItem(u"associazione", _(u"Associazione")),
            VocabItem(u"istruzione", _(u"Istruzione")),
            VocabItem(u"abitazione", _(u"Abitazione")),
            VocabItem(u"animale-domestico", _(u"Animale domestico")),
            VocabItem(u"integrazione-sociale", _(u"Integrazione sociale")),
            VocabItem(u"protezione-sociale", _(u"Protezione sociale")),
            VocabItem(u"comunicazione", _(u"Comunicazione")),
            VocabItem(u"urbanistica-edilizia", _(u"Urbanistica ed edilizia")),
            VocabItem(
                u"formazione-professionale", _(u"Formazione professionale")
            ),
            VocabItem(
                u"condizioni-organizzazione-lavoro",
                _(u"Condizioni e organizzazione del lavoro"),
            ),
            VocabItem(u"trasporto", _(u"Trasporto")),
            VocabItem(u"matrimonio", _(u"Matrimonio")),
            VocabItem(u"elezione", _(u"Elezione")),
            VocabItem(u"tempo-libero", _(u"Tempo libero")),
            VocabItem(u"cultura", _(u"Cultura")),
            VocabItem(u"immigrazione", _(u"Immigrazione")),
            VocabItem(u"inquinamento", _(u"Inquinamento")),
            VocabItem(u"area-parcheggio", _(u"Area di parcheggio")),
            VocabItem(u"traffico-urbano", _(u"Traffico urbano")),
            VocabItem(u"acqua", _(u"Acqua")),
            VocabItem(u"gestione-rifiuti", _(u"Gestione dei rifiuti")),
            VocabItem(u"salute", _(u"Salute")),
            VocabItem(u"sicurezza-pubblica", _(u"Sicurezza pubblica")),
            VocabItem(
                u"sicurezza-internazionale", _(u"Sicurezza internazionale")
            ),
            VocabItem(u"spazio-verde", _(u"Spazio verde")),
            VocabItem(u"sport", _(u"Sport")),
            VocabItem(u"trasporto-stradale", _(u"Trasporto stradale")),
            VocabItem(u"turismo", _(u"Turismo")),
            VocabItem(u"energia", _(u"Energia")),
            VocabItem(
                u"informatica-trattamento-dati",
                _(u"Informatica e trattamento dei dati"),
            ),
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
                    value=item.token, token=str(item.token), title=item.value
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


TagsVocabularyFactory = TagsVocabulary()
