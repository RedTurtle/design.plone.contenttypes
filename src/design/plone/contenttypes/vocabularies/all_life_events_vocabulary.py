# -*- coding: utf-8 -*-

# from plone import api
from design.plone.contenttypes import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18n import translate


@implementer(IVocabularyFactory)
class AllLifeEventsVocabulary(object):
    """
    """

    def __call__(self, context):
        """
        Vocabolario attualmente inutile. Lasciato per memoria storica e per
        non rifare il lavoro se ce lo chiedessero in futuro.
        """
        items = [
            (
                u"L1.0",
                _(
                    u"Iscrizione scuola/università e/o richiesta borsa di studio"
                ),
            ),
            (u"L2.0", _(u"Invalidità")),
            (
                u"L3.0",
                _(u"Ricerca di lavoro, avvio nuovo lavoro, disoccupazione"),
            ),
            (u"L4.0", _(u"Pensionamento")),
            (u"L5.0", _(u"Richiesta o rinnovo patente")),
            (u"L6.0", _(u"Registrazione/possesso veicolo")),
            (u"L7.0", _(u"Accesso al trasporto pubblico")),
            (
                u"L8.0",
                _(
                    u"Compravendita/affitto casa/edifici/terreni, costruzione o ristrutturazione casa/edificio	"
                ),
            ),
            (u"L9.0", _(u"Cambio di residenza/domicilio")),
            (
                u"L11.0",
                _(
                    u"Richiesta passaporto, visto e assistenza viaggi internazionali"
                ),
            ),
            (u"L12.0", _(u"Nascita di un bambino, richiesta adozioni")),
            (u"L13.0", _(u"Matrimonio e/o cambio stato civile")),
            (u"L14.0", _(u"Morte ed eredità")),
            (u"L15.0", _(u"Prenotazione e disdetta visite/esami")),
            (u"L16.0", _(u"Denuncia crimini")),
            (
                u"L17.0",
                _(
                    u"Dichiarazione dei redditi, versamento e riscossione tributi/imposte e contributi"
                ),
            ),
            (u"L18.0", _(u"Accesso luoghi della cultura")),
            (u"L19.0", _(u"Possesso, cura, smarrimento animale da compagnia")),
            (
                u"B1.0",
                _(
                    u"Iscrizione scuola/università e/o richiesta borsa di studio"
                ),
            ),
            (u"B2.0", _(u"Avvio impresa")),
            (u"B3.0", _(u"Avvio nuova attività professionale")),
            (u"B4.0", _(u"Richiesta licenze/permessi/certificati")),
            (u"B5.0", _(u"Registrazione impresa transfrontalier")),
            (u"B6.0", _(u"Avvio/registrazione filiale")),
            (u"B7.0", _(u"Finanziamento impresa")),
            (u"B8.0", _(u"Gestione personale")),
            (u"B9.0", _(u"Pagamento tasse, iva e dogane")),
            (u"B10.0", _(u"Notifiche autorità")),
            (u"B11.0", _(u"Chiusura impresa e attività professionale")),
            (u"B12.0", _(u"Chiusura filiale")),
            (u"B13.0", _(u"Ristrutturazione impresa")),
            (u"B14.0", _(u"Vendita impresa")),
            (u"B15.0", _(u"Bancarotta")),
            (
                u"B16.0",
                _(
                    u"Partecipazione ad appalti pubblici nazionali e trasfrontalieri"
                ),
            ),
        ]
        req = getRequest()

        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = [
            SimpleTerm(
                value=item[0],
                token=item[0],
                title=translate(item[1], context=req),
            )
            for item in sorted(items, key=lambda k: k[1])
        ]
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


AllLifeEventsVocabularyFactory = AllLifeEventsVocabulary()
