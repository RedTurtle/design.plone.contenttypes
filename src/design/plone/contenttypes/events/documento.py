# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from design.plone.contenttypes.utils import create_default_blocks


def documentoCreateHandler(documento, event):
    """
    Complete content type Documento setup on added event, generating
    missing folders, fields, etc.

    @param documento: Content item

    @param event: Event that triggers the method (onAdded event)
    """
    if "multimedia" in documento.keys():
        # we are copying or moving it
        return

    documentoConstraints = ISelectableConstrainTypes(documento)
    documentoConstraints.setConstrainTypesMode(1)
    documentoConstraints.setLocallyAllowedTypes(("Document",))

    # create support folder
    multimedia = api.content.create(
        type="Document", title="Multimedia", container=documento
    )
    create_default_blocks(context=multimedia)

    multimediaConstraints = ISelectableConstrainTypes(multimedia)
    multimediaConstraints.setConstrainTypesMode(1)
    multimediaConstraints.setLocallyAllowedTypes(("Image",))

    documentoConstraints = ISelectableConstrainTypes(documento)
    documentoConstraints.setConstrainTypesMode(1)
    documentoConstraints.setLocallyAllowedTypes(("Modulo", "Link"))
