# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes

import logging

logger = logging.getLogger(__name__)


def unitaOrganizzativaCreateHandler(unitaOrganizzativa, event):
    """
    Complete content type UnitaOrganizzativa setup on added event, generating
    missing folders, fields, etc.

    @param unitaOrganizzativa: Content item

    @param event: Event that triggers the method (onAdded event)
    """
    if "allegati" in unitaOrganizzativa.keys():
        return
    try:
        allegati = api.content.create(
            type="Document", title="Allegati", container=unitaOrganizzativa
        )
    except AttributeError as e:
        # problems with tests in design.plone.policy
        logger.exception(e)
        return

    allegatiConstraints = ISelectableConstrainTypes(allegati)
    allegatiConstraints.setConstrainTypesMode(1)
    allegatiConstraints.setLocallyAllowedTypes(("File",))
