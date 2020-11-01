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

    # constraintsEvento = ISelectableConstrainTypes(evento)
    # constraintsEvento.setConstrainTypesMode(1)
    # constraintsEvento.setLocallyAllowedTypes(("Event", "Document"))

    galleria = api.content.create(
        container=evento, type="Document", title="Multimedia", id="multimedia"
    )

    sponsor = api.content.create(
        container=evento,
        type="Document",
        title="Sponsor Evento",
        id="sponsor_evento",
    )

    documenti = api.content.create(
        container=evento, type="Document", title="Documenti", id="documenti"
    )

    # select  constraints
    constraintsGalleria = ISelectableConstrainTypes(galleria)
    constraintsGalleria.setConstrainTypesMode(1)
    constraintsGalleria.setLocallyAllowedTypes(("Image", "Link"))

    constraintsSponsor = ISelectableConstrainTypes(sponsor)
    constraintsSponsor.setConstrainTypesMode(1)

    constraintsSponsor.setLocallyAllowedTypes(("Link",))

    constraintsDocumenti = ISelectableConstrainTypes(documenti)
    constraintsDocumenti.setConstrainTypesMode(1)
    constraintsDocumenti.setLocallyAllowedTypes(("File",))

    # constraintsEvento.setLocallyAllowedTypes(("Event",))

    # add publish automation during creation
    api.content.transition(obj=galleria, transition="publish")
    api.content.transition(obj=sponsor, transition="publish")
    api.content.transition(obj=documenti, transition="publish")
