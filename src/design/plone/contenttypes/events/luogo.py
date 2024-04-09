# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFPlone.utils import _createObjectByType


def luogoCreateHandler(luogo, event):
    """
    Complete content type luogo setup on added event, generating
    missing folders, fields, etc.

    @param luogo: Content item

    @param event: Event that triggers the method (onAdded event)
    """
    folder_id = "multimedia"
    if folder_id in luogo:
        return
    folder = _createObjectByType("Folder", luogo, "multimedia")
    folder.title = "Multimedia"
    folder.exclude_from_search = True
    folder.reindexObject(idxs=["Title", "exclude_from_search"])
    constraints = ISelectableConstrainTypes(folder)
    constraints.setConstrainTypesMode(1)
    constraints.setLocallyAllowedTypes(
        (
            "Image",
            "Link",
        )
    )

    # non dovrebbe essere cancellabile
