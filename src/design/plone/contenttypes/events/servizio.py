# -*- coding: utf-8 -*-
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def servizioCreateHandler(servizio, event):
    """
    Complete content type Servizio setup on added event, generating
    missing folders, fields, etc.

    @param servizio: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    for folder in [
        {"id": "modulistica", "title": "Modulistica", "contains": ("File", "Link")},
        {"id": "allegati", "title": "Allegati", "contains": ("File", "Link")},
    ]:
        if folder["id"] not in servizio.keys():
            child = api.content.create(
                type="Document", title=folder["title"], container=servizio
            )
            create_default_blocks(context=child)

            childConstraints = ISelectableConstrainTypes(child)
            childConstraints.setConstrainTypesMode(1)
            childConstraints.setLocallyAllowedTypes(folder["contains"])
