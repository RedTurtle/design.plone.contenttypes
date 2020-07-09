# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.namedfile import field
from plone.supermodel import model
from zope import schema


class IRicevutaPagamento(model.Schema):
    """ Marker interface for RicevutaPagamento
    """

    numero_protocollo = schema.Id(
        title=_(u'numero_protocollo', default=u'Numero protocollo'),
        required=True,
    )

    stampa_ricevuta = field.NamedFile(
        title=_(u'stampa_ricevuta', default=u'Stampa ricevuta'), required=True
    )

    data_pagamento = schema.Date(
        title=_(u'data_pagamento', default=u'Data pagamento'), required=True
    )

    importo_pagato = schema.TextLine(
        title=_(u'importo_pagato', default=u'Importo pagato'), required=True
    )

    modalita_pagamento = schema.TextLine(
        title=_(u'modalita_pagamento', default=u'Modalità pagamento'),
        required=True,
    )

    # TODO: aggiungere tassonomia e vocabolario rilevante
    servizio_origine = schema.Choice(
        title=_(
            u'servizio_origine_ricevuta', default=u'Servizio che origina la pratica'
        ),
        # vocabolario di riferimento sara' il servizio che genera il task e
        # permette di soddisfarlo
        vocabulary='design.plone.contenttypes.Mockup',
        required=False,
    )

    pratica_associata = field.NamedFile(
        title=_(
            u'pratica_associata_ricevuta', default=u'Pratica associata al pagamento'
        ),
        required=True,
    )

    # TODO: capire se ci sono altri esiti oltre ai banali "accettato",
    # "rifiutato", "in attesa di conferma",
    # e costruire di conseguenza un vocabolario adeguato
    esito = schema.Choice(
        title=_(u'esito', default=u'Esito'),
        vocabulary='design.plone.contenttypes.Mockup',
        required=True,
    )

    allegato = field.NamedFile(
        title=_(u'allegato', default=u'Allegato'), required=False
    )
