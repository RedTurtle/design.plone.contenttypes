from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def luogoCreateHandler(luogo, event):
    '''
    Complete content type luogo setup on added event, generating 
    missing folders, fields, etc.

    @param luogo: Content item

    @param event: Event that triggers the method (onAdded event)
    '''

    folder = _createObjectByType("Folder", luogo, 'galleria-immagini')
    folder.title = 'Galleria Immagini'
    folder.reindexObject(idxs=['Title'])
    constraints = ISelectableConstrainTypes(folder)
    constraints.setConstrainTypesMode(1)
    constraints.setLocallyAllowedTypes(('Image',))

    # non dovrebbe essere cancellabile
