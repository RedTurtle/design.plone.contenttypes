# -*- coding: utf-8 -*-
from plone.supermodel import model
from plone.app.textfield import RichText
from zope import schema
from design.plone.contenttypes import _


class IPratica(model.Schema):
    """ Marker interface for Pratica
    """

    numero_protocollo = schema.TextLine(
        title=_(u'numero_protocollo', default=u'Numero protocollo'),
        required=True,
    )

    ufficio_riferimento = schema.Choice(
        title=_(u'ufficio_riferimento', default=u'Ufficio di riferimento'),
        # vocabolario di riferimento sara' la lista degli uffici di riferimento
        vocabulary='design.plone.contenttypes.Mockup',
        required=False,
    )

    # questo viene gestito dal workflow di Plone ma fa riferimento ad una
    # tassonomia "Lista stati di una pratica"
    stato_pratica = schema.TextLine(
        title=_(u'stato_pratica', default=u'Stato della pratica'),
        required=True,
    )

    # TODO: aggiungere tassonomia e vocabolario rilevante
    servizio_origine = schema.Choice(
        title=_(
            u'servizio_origine_pratica', default=u'Servizio che origina la pratica'
        ),
        # vocabolario di riferimento sara' il servizio che genera il task e
        # permette di soddisfarlo
        vocabulary='design.plone.contenttypes.Mockup',
        required=False,
    )

    contenuto = RichText(
        title=_(u'contenuto', default=u'Contenuto'), required=True
    )

    contatti = RichText(
        title=_(u'contatti', default=u'Contatti'), required=True
    )

    azioni_utente = schema.Choice(
        title=_(u'azioni_utente', default=u'Azioni utente'),
        # vocabolario di riferimento sara' la tassonomia "Lista azioni pratica"
        vocabulary='design.plone.contenttypes.ListaAzioniPratica',
        required=True,
    )
