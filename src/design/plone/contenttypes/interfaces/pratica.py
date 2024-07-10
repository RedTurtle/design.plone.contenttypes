# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.supermodel import model
from zope import schema


class IPratica(model.Schema):
    """Marker interface for Pratica"""

    numero_protocollo = schema.TextLine(
        title=_("numero_protocollo", default="Numero protocollo"),
        required=True,
    )

    ufficio_riferimento = schema.Choice(
        title=_("ufficio_riferimento", default="Ufficio di riferimento"),
        # vocabolario di riferimento sara' la lista degli uffici di riferimento
        vocabulary="design.plone.contenttypes.Mockup",
        required=False,
    )

    # questo viene gestito dal workflow di Plone ma fa riferimento ad una
    # tassonomia "Lista stati di una pratica"
    stato_pratica = schema.TextLine(
        title=_("stato_pratica", default="Stato della pratica"),
        required=True,
    )

    # TODO: aggiungere tassonomia e vocabolario rilevante
    servizio_origine = schema.Choice(
        title=_(
            "servizio_origine_pratica",
            default="Servizio che origina la pratica",
        ),
        # vocabolario di riferimento sara' il servizio che genera il task e
        # permette di soddisfarlo
        vocabulary="design.plone.contenttypes.Mockup",
        required=False,
    )

    contenuto = BlocksField(title=_("contenuto", default="Contenuto"), required=True)

    contatti = BlocksField(title=_("contatti", default="Contatti"), required=True)

    azioni_utente = schema.Choice(
        title=_("azioni_utente", default="Azioni utente"),
        # vocabolario di riferimento sara' la tassonomia "Lista azioni pratica"
        vocabulary="design.plone.contenttypes.ListaAzioniPratica",
        required=True,
    )
