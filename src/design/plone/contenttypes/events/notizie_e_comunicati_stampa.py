# -*- coding: utf-8 -*-
from design.plone.contenttypes.utils import create_default_blocks
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from plone import api


def notiziaCreateHandler(notizia, event):
    """
    Complete content type notizia setup on added event, generating
    missing folders, fields, etc.

    @param notizia: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    if "multimedia" not in notizia.keys():
        multimedia = api.content.create(
            type="Document",
            title="Multimedia",
            container=notizia,
            exclude_from_search=True,
        )
        create_default_blocks(context=multimedia)
        constraintsMultimedia = ISelectableConstrainTypes(multimedia)
        constraintsMultimedia.setConstrainTypesMode(1)
        constraintsMultimedia.setLocallyAllowedTypes(("Link", "Image"))

    if "documenti-allegati" not in notizia.keys():
        documenti = api.content.create(
            type="Document",
            title="Documenti allegati",
            container=notizia,
            exclude_from_search=True,
        )
        create_default_blocks(context=documenti)
        constraintsDocumenti = ISelectableConstrainTypes(documenti)
        constraintsDocumenti.setConstrainTypesMode(1)
        constraintsDocumenti.setLocallyAllowedTypes(("File", "Image"))
