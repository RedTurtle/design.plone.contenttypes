# -*- coding: utf-8 -*-
# from plone import api
# from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def documentoPersonaleCreateHandler(documento_personale, event):
    """
    Complete content type Documento Personale setup on added event, generating
    missing folders, fields, etc.

    @param documento_personale: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    # galleria = api.content.create(
    #     type='Folder', title='Immagini', container=documento_personale
    # )

    # documenti_allegati = api.content.create(
    #     type='Folder',
    #     title='Documenti allegati',
    #     container=documento_personale,
    # )

    # allegati = api.content.create(
    #     type='Folder', title='Allegati', container=documento_personale
    # )

    # galleryConstraints = ISelectableConstrainTypes(galleria)
    # galleryConstraints.setConstrainTypesMode(1)
    # galleryConstraints.setLocallyAllowedTypes(('Image',))
    # documentsConstraints = ISelectableConstrainTypes(documenti_allegati)
    # documentsConstraints.setConstrainTypesMode(1)
    # documentsConstraints.setLocallyAllowedTypes(('File',))
    # attachedConstraints = ISelectableConstrainTypes(allegati)
    # attachedConstraints.setConstrainTypesMode(1)
    # attachedConstraints.setLocallyAllowedTypes(('File', 'Folder'))
