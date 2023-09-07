# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes import AGID_VERSION
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


TAGS_MAPPING = {
    "V2": [
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
    ],
    "V3": [
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
    ],
}


@implementer(IVocabularyFactory)
class TagsVocabulary(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = TAGS_MAPPING.get(AGID_VERSION, []) or TAGS_MAPPING["V3"]

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
