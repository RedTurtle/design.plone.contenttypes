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
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(
                u"agricoltura_pesca_silvicoltura_e_prodotti_alimentari",
                _(u"Agricoltura, pesca, silvicoltura e prodotti alimentari"),
            ),
            VocabItem(u"economia_e_finanze", _(u"Economia e Finanze")),
            VocabItem(
                u"istruzione_cultura_e_sport",
                _(u"Istruzione, cultura e sport"),
            ),
            VocabItem(u"energia", _(u"Energia")),
            VocabItem(u"ambiente", _(u"Ambiente")),
            VocabItem(
                u"governo_e_settore_pubblico", _(u"Governo e settore pubblico")
            ),
            VocabItem(u"salute", _(u"Salute")),
            VocabItem(
                u"tematiche_internazionali", _(u"Tematiche internazionali")
            ),
            VocabItem(
                u"giustizia_sistema_giuridico_e_sicurezza_pubblica",
                _(u"Giustizia, sistema giuridico e sicurezza pubblica"),
            ),
            VocabItem(u"regioni_e_citta", _(u"Regioni e città")),
            VocabItem(u"popolazione_e_societa", _(u"Popolazione e società")),
            VocabItem(u"scienza_e_tecnologia", _(u"Scienza e tecnologia")),
        ]

        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token, token=str(item.token), title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


TemiDatasetFactory = TemiDataset()
