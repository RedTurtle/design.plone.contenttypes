# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.namedfile import field
from plone.supermodel import model
from zope import schema


class IMessaggio(model.Schema):
    """Marker interface for Messaggio"""

    data_messaggio = schema.Date(
        title=_("data_messaggio", default="Data del messaggio"),
        required=True,
    )

    # "Titolo del messaggio" e "Descrizione" vengono lasciati in titolo e
    # descrizione di Plone

    # TODO: aggiungere tassonomia delle tipologie di azioni richieste al
    # cittadino
    azioni_richieste = schema.Choice(
        title=_("azioni_richieste", default="Azioni richieste"),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    azioni_pratica = schema.Choice(
        title=_("azioni_pratica", default="Azioni"),
        # vocabolario di riferimento sara' la tassonomia "Lista azioni pratica"
        vocabulary="design.plone.contenttypes.ListaAzioniPratica",
        required=True,
    )

    pratica_associata = schema.TextLine(
        title=_("pratica_associata", default="Pratica associata"),
        required=True,
    )

    data_scadenza_procedura = schema.Date(
        title=_(
            "data_scadenza_procedura",
            default="Data di scadenza della procedura",
        ),
        required=False,
    )

    documenti_allegati = field.NamedFile(
        title=_("documenti_allegati", default="Documenti allegati"),
        required=False,
    )
