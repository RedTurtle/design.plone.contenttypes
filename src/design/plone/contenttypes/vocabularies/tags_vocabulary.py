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


TAGS_MAPPING = [
    ("accesso_all_informazione", _("Accesso all'informazione")),
    ("acqua", _("Acqua")),
    ("agricoltura", _("Agricoltura")),
    ("animale_domestico", _("Animale domestico")),
    ("aria", _("Aria")),
    ("assistenza_agli_anziani", _("Assistenza agli invalidi")),
    ("assistenza_sociale", _("Assistenza sociale")),
    ("associazioni", _("Associazioni")),
    ("bilancio", _("Bilancio")),
    ("commercio_all_ingresso", _("Commercio all'ingrosso")),
    ("commercio_al_minuto", _("Commercio al minuto")),
    ("commercio_ambulante", _("Commercio ambulante")),
    ("comunicazione_istituzionale", _("Comunicazione istituzionale")),
    ("comunicazione_politica", _("Comunicazione politica")),
    ("concordi", _("Concorsi")),
    ("covid_19", _("Covid - 19")),
    ("elezioni", _("Elezioni")),
    ("energie_rinnovabili", _("Energie rinnovabili")),
    ("estero", _("Estero")),
    ("foreste", _("Foreste")),
    ("formazione_professionale", _("Formazione professionale")),
    ("gemellaggi", _("Gemellaggi")),
    ("gestione_rifiuti", _("Gestione rifiuti")),
    ("giustizia", _("Giustizia")),
    ("igiene_pubblica", _("Igiene pubblica")),
    ("immigrazione", _("Immigrazione")),
    ("imposte", _("Imposte")),
    ("imprese", _("Imprese")),
    ("inquinamento", _("Inquinamento")),
    ("integrazione_sociale", _("Integrazione sociale")),
    ("isolamento_termico", _("Isolamento termico")),
    ("istruzione", _("Istruzione")),
    ("lavoro", _("Lavoro")),
    ("matrimonio", _("Matrimonio")),
    ("mercato", _("Mercato")),
    ("mobilita_sostenibile", _("Mobilità sostenibile")),
    ("morte", _("Morte")),
    ("nascita", _("Nascita")),
    ("parcheggi", _("Parcheggi")),
    ("patrimonio_culturale", _("Patrimonio culturale")),
    ("pesca", _("Pesca")),
    ("piano_di_sviluppo", _("Piano di sviluppo")),
    ("pista_ciclabile", _("Pista ciclabile")),
    ("politica_commerciale", _("Politica commerciale")),
    ("polizia", _("Polizia")),
    ("prodotti_alimentari", _("Prodotti alimentari")),
    ("protezione_civile", _("Protezione civile")),
    ("residenza", _("Residenza")),
    ("risposta_alle_emergenze", _("Risposta alle emergenze")),
    ("sistema_giuridico", _("Sistema giuridico")),
    ("spazio_verde", _("Spazio Verde")),
    ("sport", _("Sport")),
    ("sviluppo_sostenibile", _("Sviluppo sostenibile")),
    ("tassa_sui_servizi", _("Tassa sui servizi")),
    ("tempo_libero", _("Tempo libero")),
    ("trasparenza_amministrativa", _("Trasparenza amministrativa")),
    ("trasporto_pubblico", _("Trasporto pubblico")),
    ("turismo", _("Turismo")),
    ("urbanizzazione", _("Urbanizzazione")),
    ("viaggi", _("Viaggi")),
    ("zone_pedonali", _("Zone pedonali")),
    ("ztl", _("ZTL")),
]


@implementer(IVocabularyFactory)
class TagsVocabulary(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [VocabItem(token=token, value=value) for token, value in TAGS_MAPPING]

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
