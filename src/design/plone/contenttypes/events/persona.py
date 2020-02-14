from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def personaCreateHandler(persona, event):
    '''
    Complete content type Persona setup on added event, generating
    missing folders, fields, etc.

    @param persona: Content item

    @param event: Event that triggers the method (onAdded event)
    '''

    galleria = api.content.create(
        type='Document',
        title='Foto attività politica',
        container=persona
    )

    altre_cariche = api.content.create(
        type='Document',
        title='Altre cariche',
        container=persona
    )

    galleryConstraints = ISelectableConstrainTypes(galleria)
    galleryConstraints.setConstrainTypesMode(1)
    galleryConstraints.setLocallyAllowedTypes(('Image',))
    sideJobsConstraints = ISelectableConstrainTypes(altre_cariche)
    sideJobsConstraints.setConstrainTypesMode(1)
    sideJobsConstraints.setLocallyAllowedTypes(('Image',))
