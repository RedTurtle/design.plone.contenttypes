# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from plone import api


def eventoCreateHandler(evento, event):
    """
    Complete content type evento setup on added event, generating
    missing folders, fields, etc.

    @param evento: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    if "multimedia" not in evento.keys():
        galleria = api.content.create(
            container=evento,
            type="Document",
            title="Multimedia",
            id="multimedia",
        )
        # select  constraints
        constraintsGalleria = ISelectableConstrainTypes(galleria)
        constraintsGalleria.setConstrainTypesMode(1)
        constraintsGalleria.setLocallyAllowedTypes(("Image", "Link"))

        api.content.transition(obj=galleria, transition="publish")

    if "sponsor_evento" not in evento.keys():
        sponsor = api.content.create(
            container=evento,
            type="Document",
            title="Sponsor Evento",
            id="sponsor_evento",
        )
        constraintsSponsor = ISelectableConstrainTypes(sponsor)
        constraintsSponsor.setConstrainTypesMode(1)
        constraintsSponsor.setLocallyAllowedTypes(("Link",))

        api.content.transition(obj=sponsor, transition="publish")

    if "documenti" not in evento.keys():
        documenti = api.content.create(
            container=evento,
            type="Document",
            title="Documenti",
            id="documenti",
        )
        constraintsDocumenti = ISelectableConstrainTypes(documenti)
        constraintsDocumenti.setConstrainTypesMode(1)
        constraintsDocumenti.setLocallyAllowedTypes(("File",))

        api.content.transition(obj=documenti, transition="publish")
