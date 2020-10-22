# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def documentCreateHandler(document, event):
    """
    @param document: Content item

    @param event: Event that triggers the method (onAdded event)

    Se viene creato dentro ad una cartella modulistica, allora al suo interno
    si possono creare solo Documenti.
    """

    if event.newParent.portal_type == "CartellaModulistica":
        documentConstraints = ISelectableConstrainTypes(document)
        documentConstraints.setConstrainTypesMode(1)
        documentConstraints.setLocallyAllowedTypes(("Documento",))
