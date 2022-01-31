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
class TemiDataset(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(
                "agricoltura_pesca_silvicoltura_e_prodotti_alimentari",
                _("Agricoltura, pesca, silvicoltura e prodotti alimentari"),
            ),
            VocabItem("economia_e_finanze", _("Economia e Finanze")),
            VocabItem(
                "istruzione_cultura_e_sport",
                _("Istruzione, cultura e sport"),
            ),
            VocabItem("energia", _("Energia")),
            VocabItem("ambiente", _("Ambiente")),
            VocabItem("governo_e_settore_pubblico", _("Governo e settore pubblico")),
            VocabItem("salute", _("Salute")),
            VocabItem("tematiche_internazionali", _("Tematiche internazionali")),
            VocabItem(
                "giustizia_sistema_giuridico_e_sicurezza_pubblica",
                _("Giustizia, sistema giuridico e sicurezza pubblica"),
            ),
            VocabItem("regioni_e_citta", _("Regioni e città")),
            VocabItem("popolazione_e_societa", _("Popolazione e società")),
            VocabItem("scienza_e_tecnologia", _("Scienza e tecnologia")),
        ]

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


TemiDatasetFactory = TemiDataset()
