from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def servizioCreateHandler(servizio, event):
    '''
    Complete content type Servizio setup on added event, generating 
    missing folders, fields, etc.

    @param servizio: Content item

    @param event: Event that triggers the method (onAdded event)
    '''

    luoghi = api.content.create(
        type='Folder',
        title='Luoghi',
        container=servizio
    )

    sedi = api.content.create(
        type='Folder',
        title='Sedi',
        container=servizio
    )

    luoghiConstraints = ISelectableConstrainTypes(luoghi)
    luoghiConstraints.setConstrainTypesMode(1)
    luoghiConstraints.setLocallyAllowedTypes(('Venue',))
    sediConstraints = ISelectableConstrainTypes(sedi)
    sediConstraints.setConstrainTypesMode(1)
    sediConstraints.setLocallyAllowedTypes(('Venue',))