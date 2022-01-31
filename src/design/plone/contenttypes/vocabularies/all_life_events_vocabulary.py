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
    """ """

    def __call__(self, context):
        """
        Vocabolario attualmente inutile. Lasciato per memoria storica e per
        non rifare il lavoro se ce lo chiedessero in futuro.
        """
        items = [
            (
                "L1.0",
                _("Iscrizione scuola/università e/o richiesta borsa di studio"),
            ),
            ("L2.0", _("Invalidità")),
            (
                "L3.0",
                _("Ricerca di lavoro, avvio nuovo lavoro, disoccupazione"),
            ),
            ("L4.0", _("Pensionamento")),
            ("L5.0", _("Richiesta o rinnovo patente")),
            ("L6.0", _("Registrazione/possesso veicolo")),
            ("L7.0", _("Accesso al trasporto pubblico")),
            (
                "L8.0",
                _(
                    "Compravendita/affitto casa/edifici/terreni, costruzione o ristrutturazione casa/edificio	"
                ),
            ),
            ("L9.0", _("Cambio di residenza/domicilio")),
            (
                "L11.0",
                _("Richiesta passaporto, visto e assistenza viaggi internazionali"),
            ),
            ("L12.0", _("Nascita di un bambino, richiesta adozioni")),
            ("L13.0", _("Matrimonio e/o cambio stato civile")),
            ("L14.0", _("Morte ed eredità")),
            ("L15.0", _("Prenotazione e disdetta visite/esami")),
            ("L16.0", _("Denuncia crimini")),
            (
                "L17.0",
                _(
                    "Dichiarazione dei redditi, versamento e riscossione tributi/imposte e contributi"
                ),
            ),
            ("L18.0", _("Accesso luoghi della cultura")),
            ("L19.0", _("Possesso, cura, smarrimento animale da compagnia")),
            (
                "B1.0",
                _("Iscrizione scuola/università e/o richiesta borsa di studio"),
            ),
            ("B2.0", _("Avvio impresa")),
            ("B3.0", _("Avvio nuova attività professionale")),
            ("B4.0", _("Richiesta licenze/permessi/certificati")),
            ("B5.0", _("Registrazione impresa transfrontalier")),
            ("B6.0", _("Avvio/registrazione filiale")),
            ("B7.0", _("Finanziamento impresa")),
            ("B8.0", _("Gestione personale")),
            ("B9.0", _("Pagamento tasse, iva e dogane")),
            ("B10.0", _("Notifiche autorità")),
            ("B11.0", _("Chiusura impresa e attività professionale")),
            ("B12.0", _("Chiusura filiale")),
            ("B13.0", _("Ristrutturazione impresa")),
            ("B14.0", _("Vendita impresa")),
            ("B15.0", _("Bancarotta")),
            (
                "B16.0",
                _("Partecipazione ad appalti pubblici nazionali e trasfrontalieri"),
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
