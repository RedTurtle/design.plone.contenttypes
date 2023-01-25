# -*- coding: utf-8 -*-
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def incaricoCreateHandler(incarico, event):
    """
    Complete content type incarico setup on added event, generating
    missing folders, fields, etc.

    @param incarico: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    FOLDERS = [
        {"id": "compensi-file", "title": "Compensi", "contains": ("File",)},
        {
            "id": "importi-di-viaggio-e-o-servizi",
            "title": "Importi di viaggio e/o servizi",
            "contains": ("File",),
        },
    ]
    for folder in FOLDERS:
        if folder["id"] in incarico:
            continue
        suboject = api.content.create(
            type="Document", id=folder["id"], title=folder["title"], container=incarico
        )
        create_default_blocks(context=suboject)
        subobjectConstraints = ISelectableConstrainTypes(suboject)
        subobjectConstraints.setConstrainTypesMode(1)
        subobjectConstraints.setLocallyAllowedTypes(folder["contains"])


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
