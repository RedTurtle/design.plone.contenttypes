# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def unitaOrganizzativaCreateHandler(unitaOrganizzativa, event):
    '''
    Complete content type UnitaOrganizzativa setup on added event, generating
    missing folders, fields, etc.

    @param unitaOrganizzativa: Content item

    @param event: Event that triggers the method (onAdded event)
    '''
    allegati = api.content.create(
        type='Document', title='Allegati', container=unitaOrganizzativa
    )

    allegatiConstraints = ISelectableConstrainTypes(allegati)
    allegatiConstraints.setConstrainTypesMode(1)
    allegatiConstraints.setLocallyAllowedTypes(('File',))
