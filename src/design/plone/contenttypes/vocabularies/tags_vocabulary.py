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
            VocabItem("accesso_all_informazione", _("Accesso all'informazione")),
            VocabItem("acqua", _("Acqua")),
            VocabItem("agricoltura", _("Agricoltura")),
            VocabItem("animale_domestico", _("Animale domestico")),
            VocabItem("aria", _("Aria")),
            VocabItem("assistenza_agli_anziani", _("Assistenza agli invalidi")),
            VocabItem("assistenza_sociale", _("Assistenza sociale")),
            VocabItem("associazioni", _("Associazioni")),
            VocabItem("bilancio", _("Bilancio")),
            VocabItem("commercio_all_ingresso", _("Commercio all'ingrosso")),
            VocabItem("commercio_al_minuto", _("Commercio al minuto")),
            VocabItem("commercio_ambulante", _("Commercio ambulante")),
            VocabItem("comunicazione_istituzionale", _("Comunicazione istituzionale")),
            VocabItem("comunicazione_politica", _("Comunicazione politica")),
            VocabItem("concordi", _("Concorsi")),
            VocabItem("covid_19", _("Covid - 19")),
            VocabItem("elezioni", _("Elezioni")),
            VocabItem("energie_rinnovabili", _("Energie rinnovabili")),
            VocabItem("estero", _("Estero")),
            VocabItem("foreste", _("Foreste")),
            VocabItem("formazione_professionale", _("Formazione professionale")),
            VocabItem("gemellaggi", _("Gemellaggi")),
            VocabItem("gestione_rifiuti", _("Gestione rifiuti")),
            VocabItem("giustizia", _("Giustizia")),
            VocabItem("igiene_pubblica", _("Igiene pubblica")),
            VocabItem("immigrazione", _("Immigrazione")),
            VocabItem("imposte", _("Imposte")),
            VocabItem("imprese", _("Imprese")),
            VocabItem("inquinamento", _("Inquinamento")),
            VocabItem("integrazione_sociale", _("Integrazione sociale")),
            VocabItem("isolamento_termico", _("Isolamento termico")),
            VocabItem("istruzione", _("Istruzione")),
            VocabItem("lavoro", _("Lavoro")),
            VocabItem("matrimonio", _("Matrimonio")),
            VocabItem("mercato", _("Mercato")),
            VocabItem("mobilita_sostenibile", _("Mobilità sostenibile")),
            VocabItem("morte", _("Morte")),
            VocabItem("nascita", _("Nascita")),
            VocabItem("parcheggi", _("Parcheggi")),
            VocabItem("patrimonio_culturale", _("Patrimonio culturale")),
            VocabItem("pesca", _("Pesca")),
            VocabItem("piano_di_sviluppo", _("Piano di sviluppo")),
            VocabItem("pista_ciclabile", _("Pista ciclabile")),
            VocabItem("politica_commerciale", _("Politica commerciale")),
            VocabItem("polizia", _("Polizia")),
            VocabItem("prodotti_alimentari", _("Prodotti alimentari")),
            VocabItem("protezione_civile", _("Protezione civile")),
            VocabItem("residenza", _("Residenza")),
            VocabItem("risposta_alle_emergenze", _("Risposta alle emergenze")),
            VocabItem("sistema_giuridico", _("Sistema giuridico")),
            VocabItem("spazio_verde", _("Spazio Verde")),
            VocabItem("sport", _("Sport")),
            VocabItem("sviluppo_sostenibile", _("Sviluppo sostenibile")),
            VocabItem("tassa_sui_servizi", _("Tassa sui servizi")),
            VocabItem("tempo_libero", _("Tempo libero")),
            VocabItem("trasparenza_amministrativa", _("Trasparenza amministrativa")),
            VocabItem("trasporto_pubblico", _("Trasporto pubblico")),
            VocabItem("turismo", _("Turismo")),
            VocabItem("urbanizzazione", _("Urbanizzazione")),
            VocabItem("viaggi", _("Viaggi")),
            VocabItem("zone_pedonali", _("Zone pedonali")),
            VocabItem("ztl", _("ZTL")),
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
