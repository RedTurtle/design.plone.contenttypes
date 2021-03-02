# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.namedfile import field
from plone.supermodel import model
from zope import schema


class IMessaggio(model.Schema):
    """ Marker interface for Messaggio
    """

    data_messaggio = schema.Date(
        title=_(u"data_messaggio", default=u"Data del messaggio"),
        required=True,
    )

    # "Titolo del messaggio" e "Descrizione" vengono lasciati in titolo e
    # descrizione di Plone

    # TODO: aggiungere tassonomia delle tipologie di azioni richieste al
    # cittadino
    azioni_richieste = schema.Choice(
        title=_(u"azioni_richieste", default=u"Azioni richieste"),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    azioni_pratica = schema.Choice(
        title=_(u"azioni_pratica", default=u"Azioni"),
        # vocabolario di riferimento sara' la tassonomia "Lista azioni pratica"
        vocabulary="design.plone.contenttypes.ListaAzioniPratica",
        required=True,
    )

    pratica_associata = schema.TextLine(
        title=_(u"pratica_associata", default=u"Pratica associata"),
        required=True,
    )

    data_scadenza_procedura = schema.Date(
        title=_(
            u"data_scadenza_procedura",
            default=u"Data di scadenza della procedura",
        ),
        required=False,
    )

    # TODO: inserire tassonomia contenente le tipologie di documenti
    tipologia_documento = schema.Choice(
        title=_(u"tipologia_documento", default=u"Tipologia documento"),
        required=False,
        vocabulary="design.plone.contenttypes.Mockup",
        missing_value=(),
    )

    documenti_allegati = field.NamedFile(
        title=_(u"documenti_allegati", default=u"Documenti allegati"),
        required=False,
    )
