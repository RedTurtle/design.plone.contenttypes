# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def documentoCreateHandler(documento, event):
    """
    Complete content type Documento setup on added event, generating
    missing folders, fields, etc.

    @param documento: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    allegati = api.content.create(
        type="Document", title="Allegati", container=documento
    )

    galleria = api.content.create(
        type="Document", title="Galleria", container=documento
    )

    attachedConstraints = ISelectableConstrainTypes(allegati)
    attachedConstraints.setConstrainTypesMode(1)
    attachedConstraints.setLocallyAllowedTypes(("File",))
    galleryConstraints = ISelectableConstrainTypes(galleria)
    galleryConstraints.setConstrainTypesMode(1)
    galleryConstraints.setLocallyAllowedTypes(("Image",))
