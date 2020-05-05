# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def personaCreateHandler(persona, event):
    """
    Complete content type Persona setup on added event, generating
    missing folders, fields, etc.

    @param persona: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    FOLDERS = [
        {
            "id": "gallery",
            "title": "Foto e attività politica",
            "contains": ("Image",),
        },
        {"id": "compensi", "title": "Compensi", "contains": ("File",)},
        {
            "id": "importi_viaggio_servizi",
            "title": "Importi di viaggio e/o servizi",
            "contains": ("File",),
        },
        {
            "id": "situazione_patrimoniale",
            "title": "Situazione patrimoniale",
            "contains": ("File",),
        },
        {
            "id": "dichiarazione_redditi",
            "title": "Dichiarazione dei redditi",
            "contains": ("File",),
        },
        {
            "id": "spese_elettorali",
            "title": "Spese elettorali",
            "contains": ("File",),
        },
        {
            "id": "variazione_situazione_patrimoniale",
            "title": "Variazione situazione patrimoniale",
            "contains": ("File",),
        },
        {
            "id": "altre_cariche",
            "title": "Altre cariche",
            "contains": ("File",),
        },
    ]
    for folder in FOLDERS:
        if folder["id"] in persona:
            continue
        suboject = api.content.create(
            type="Document", title=folder["title"], container=persona
        )
        subobjectConstraints = ISelectableConstrainTypes(suboject)
        subobjectConstraints.setConstrainTypesMode(1)
        subobjectConstraints.setLocallyAllowedTypes(folder["contains"])
