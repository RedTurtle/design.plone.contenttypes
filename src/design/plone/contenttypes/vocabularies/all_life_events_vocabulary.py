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
class AllLifeEventsVocabulary(object):
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(
                u"L1.0",
                _(
                    u"Iscrizione scuola/università e/o richiesta borsa di studio"
                ),
            ),
            VocabItem(u"L2.0", _(u"Invalidità")),
            VocabItem(
                u"L3.0",
                _(u"Ricerca di lavoro, avvio nuovo lavoro, disoccupazione"),
            ),
            VocabItem(u"L4.0", _(u"Pensionamento")),
            VocabItem(u"L5.0", _(u"Richiesta o rinnovo patente")),
            VocabItem(u"L6.0", _(u"Registrazione/possesso veicolo")),
            VocabItem(u"L7.0", _(u"Accesso al trasporto pubblico")),
            VocabItem(
                u"L8.0",
                _(
                    u"Compravendita/affitto casa/edifici/terreni, costruzione o ristrutturazione casa/edificio	"
                ),
            ),
            VocabItem(u"L9.0", _(u"Cambio di residenza/domicilio")),
            VocabItem(
                u"L11.0",
                _(
                    u"Richiesta passaporto, visto e assistenza viaggi internazionali"
                ),
            ),
            VocabItem(
                u"L12.0", _(u"Nascita di un bambino, richiesta adozioni")
            ),
            VocabItem(u"L13.0", _(u"Matrimonio e/o cambio stato civile")),
            VocabItem(u"L14.0", _(u"Morte ed eredità")),
            VocabItem(u"L15.0", _(u"Prenotazione e disdetta visite/esami"),),
            VocabItem(u"L16.0", _(u"Denuncia crimini")),
            VocabItem(
                u"L17.0",
                _(
                    u"Dichiarazione dei redditi, versamento e riscossione tributi/imposte e contributi"
                ),
            ),
            VocabItem(u"L18.0", _(u"Accesso luoghi della cultura")),
            VocabItem(
                u"L19.0",
                _(u"Possesso, cura, smarrimento animale da compagnia"),
            ),
            VocabItem(
                u"B1.0",
                _(
                    u"Iscrizione scuola/università e/o richiesta borsa di studio"
                ),
            ),
            VocabItem(u"B2.0", _(u"Avvio impresa")),
            VocabItem(u"B3.0", _(u"Avvio nuova attività professionale")),
            VocabItem(u"B4.0", _(u"Richiesta licenze/permessi/certificati")),
            VocabItem(u"B5.0", _(u"Registrazione impresa transfrontalier")),
            VocabItem(u"B6.0", _(u"Avvio/registrazione filiale")),
            VocabItem(u"B7.0", _(u"Finanziamento impresa")),
            VocabItem(u"B8.0", _(u"Gestione personale")),
            VocabItem(u"B9.0", _(u"Pagamento tasse, iva e dogane")),
            VocabItem(u"B10.0", _(u"Notifiche autorità")),
            VocabItem(
                u"B11.0", _(u"Chiusura impresa e attività professionale")
            ),
            VocabItem(u"B12.0", _(u"Chiusura filiale")),
            VocabItem(u"B13.0", _(u"Ristrutturazione impresa")),
            VocabItem(u"B14.0", _(u"Vendita impresa")),
            VocabItem(u"B15.0", _(u"Bancarotta"),),
            VocabItem(
                u"B16.0",
                _(
                    u"Partecipazione ad appalti pubblici nazionali e trasfrontalieri"
                ),
            ),
        ]

        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = []
        for item in sorted(items, key=lambda k: k.value):
            terms.append(
                SimpleTerm(
                    value=item.token, token=str(item.token), title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


AllLifeEventsVocabularyFactory = AllLifeEventsVocabulary()
