# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def praticaCreateHandler(pratica, event):
    """
    Complete content type Pratica setup on added event, generating
    missing folders, fields, etc.

    @param pratica: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    allegati = api.content.create(type="Folder", title="Allegati", container=pratica)

    allegatiConstraints = ISelectableConstrainTypes(allegati)
    allegatiConstraints.setConstrainTypesMode(1)
    allegatiConstraints.setLocallyAllowedTypes(("File",))
