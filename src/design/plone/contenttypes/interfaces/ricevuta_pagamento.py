# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.namedfile import field
from plone.supermodel import model
from zope import schema


class IRicevutaPagamento(model.Schema):
    """Marker interface for RicevutaPagamento"""

    numero_protocollo = schema.Id(
        title=_("numero_protocollo", default="Numero protocollo"),
        required=True,
    )

    stampa_ricevuta = field.NamedFile(
        title=_("stampa_ricevuta", default="Stampa ricevuta"), required=True
    )

    data_pagamento = schema.Date(
        title=_("data_pagamento", default="Data pagamento"), required=True
    )

    importo_pagato = schema.TextLine(
        title=_("importo_pagato", default="Importo pagato"), required=True
    )

    modalita_pagamento = schema.TextLine(
        title=_("modalita_pagamento", default="Modalità pagamento"),
        required=True,
    )

    # TODO: aggiungere tassonomia e vocabolario rilevante
    servizio_origine = schema.Choice(
        title=_("servizio_origine_ricevuta", default="Servizio che origina la pratica"),
        # vocabolario di riferimento sara' il servizio che genera il task e
        # permette di soddisfarlo
        vocabulary="design.plone.contenttypes.Mockup",
        required=False,
    )

    pratica_associata = field.NamedFile(
        title=_("pratica_associata_ricevuta", default="Pratica associata al pagamento"),
        required=True,
    )

    # TODO: capire se ci sono altri esiti oltre ai banali "accettato",
    # "rifiutato", "in attesa di conferma",
    # e costruire di conseguenza un vocabolario adeguato
    esito = schema.Choice(
        title=_("esito", default="Esito"),
        vocabulary="design.plone.contenttypes.Mockup",
        required=True,
    )

    allegato = field.NamedFile(title=_("allegato", default="Allegato"), required=False)
