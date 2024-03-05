# -*- coding: utf-8 -*-
from plone import api


def modify_incarico(obj, event):
    """
    Se cambio il titolo dell'incarico devo verificare se l'incarico è quello che
    viene puntato dalla persona. Nel caso sia quello, devo reindicizzare il
    ruolo della persona perché potrebbe essere cambiato.
    """
    idxs = ["ruolo"]
    persona = api.relation.get(target=obj, relationship="incarichi_persona")
    if not persona:
        return
    if not persona[0].isBroken():
        persona[0].from_object.reindexObject(idxs=idxs)
