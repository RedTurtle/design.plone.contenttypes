# from plone import api
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def eventoCreateHandler(evento, event):
    '''
    Complete content type evento setup on added event, generating 
    missing folders, fields, etc.

    @param evento: Content item

    @param event: Event that triggers the method (onAdded event)
    '''

    # galleria = api.content.create(
    #     type='Folder',
    #     title='Galleria immagini',
    #     container=evento
    # )

    # documenti = api.content.create(
    #     type='Folder',
    #     title='Documenti',
    #     container=evento
    # )

    # galleryConstraints = ISelectableConstrainTypes(galleria)
    # galleryConstraints.setConstrainTypesMode(1)
    # galleryConstraints.setLocallyAllowedTypes(('Image',))
    # documentsConstraints = ISelectableConstrainTypes(documenti)
    # documentsConstraints.setConstrainTypesMode(1)
    # documentsConstraints.setLocallyAllowedTypes(('File',))

    galleria = _createObjectByType("Folder", evento, 'galleria')
    galleria.title = 'Galleria'
    galleria.reindexObject(idxs=['Title'])
    constraintsGalleria = ISelectableConstrainTypes(galleria)
    constraintsGalleria.setConstrainTypesMode(1)
    # scegliere le restrizioni
    constraintsGalleria.setLocallyAllowedTypes(('Image',))

    documenti = _createObjectByType("Folder", evento, 'documenti')
    documenti.title = 'Documenti'
    documenti.reindexObject(idxs=['Title'])
    constraintsDocumenti = ISelectableConstrainTypes(documenti)
    constraintsDocumenti.setConstrainTypesMode(1)
    # scegliere le restrizioni
    constraintsDocumenti.setLocallyAllowedTypes(('File',))
