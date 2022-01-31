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
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem("anziano", _("Anziano")),
            VocabItem("fanciullo", _("Fanciullo")),
            VocabItem("giovane", _("Giovane")),
            VocabItem("famiglia", _("Famiglia")),
            VocabItem("studente", _("Studente")),
            VocabItem("associazione", _("Associazione")),
            VocabItem("istruzione", _("Istruzione")),
            VocabItem("abitazione", _("Abitazione")),
            VocabItem("animale-domestico", _("Animale domestico")),
            VocabItem("integrazione-sociale", _("Integrazione sociale")),
            VocabItem("protezione-sociale", _("Protezione sociale")),
            VocabItem("comunicazione", _("Comunicazione")),
            VocabItem("urbanistica-edilizia", _("Urbanistica ed edilizia")),
            VocabItem("formazione-professionale", _("Formazione professionale")),
            VocabItem(
                "condizioni-organizzazione-lavoro",
                _("Condizioni e organizzazione del lavoro"),
            ),
            VocabItem("trasporto", _("Trasporto")),
            VocabItem("matrimonio", _("Matrimonio")),
            VocabItem("elezione", _("Elezione")),
            VocabItem("tempo-libero", _("Tempo libero")),
            VocabItem("cultura", _("Cultura")),
            VocabItem("immigrazione", _("Immigrazione")),
            VocabItem("inquinamento", _("Inquinamento")),
            VocabItem("area-parcheggio", _("Area di parcheggio")),
            VocabItem("traffico-urbano", _("Traffico urbano")),
            VocabItem("acqua", _("Acqua")),
            VocabItem("gestione-rifiuti", _("Gestione dei rifiuti")),
            VocabItem("salute", _("Salute")),
            VocabItem("sicurezza-pubblica", _("Sicurezza pubblica")),
            VocabItem("sicurezza-internazionale", _("Sicurezza internazionale")),
            VocabItem("spazio-verde", _("Spazio verde")),
            VocabItem("sport", _("Sport")),
            VocabItem("trasporto-stradale", _("Trasporto stradale")),
            VocabItem("turismo", _("Turismo")),
            VocabItem("energia", _("Energia")),
            VocabItem(
                "informatica-trattamento-dati",
                _("Informatica e trattamento dei dati"),
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
                SimpleTerm(value=item.token, token=str(item.token), title=item.value)
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


TagsVocabularyFactory = TagsVocabulary()
