# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.utils import create_default_blocks
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from plone import api


def eventoCreateHandler(evento, event):
    """
    Complete content type evento setup on added event, generating
    missing folders, fields, etc.

    @param evento: Content item

    @param event: Event that triggers the method (onAdded event)
    """
    if not IDesignPloneContenttypesLayer.providedBy(evento.REQUEST):
        return
    if "multimedia" not in evento.keys():
        galleria = api.content.create(
            container=evento,
            type="Document",
            title="Multimedia",
            id="multimedia",
            exclude_from_search=True,
        )
        create_default_blocks(context=galleria)

        # select  constraints
        constraintsGalleria = ISelectableConstrainTypes(galleria)
        constraintsGalleria.setConstrainTypesMode(1)
        constraintsGalleria.setLocallyAllowedTypes(("Image", "Link"))

        with api.env.adopt_roles(["Reviewer"]):
            api.content.transition(obj=galleria, transition="publish")

    if "sponsor_evento" not in evento.keys():
        sponsor = api.content.create(
            container=evento,
            type="Document",
            title="Sponsor Evento",
            id="sponsor_evento",
            exclude_from_search=True,
        )
        create_default_blocks(context=sponsor)

        constraintsSponsor = ISelectableConstrainTypes(sponsor)
        constraintsSponsor.setConstrainTypesMode(1)
        constraintsSponsor.setLocallyAllowedTypes(("Link",))

        with api.env.adopt_roles(["Reviewer"]):
            api.content.transition(obj=sponsor, transition="publish")

    if "documenti" not in evento.keys():
        documenti = api.content.create(
            container=evento,
            type="Document",
            title="Documenti",
            id="documenti",
            exclude_from_search=True,
        )
        create_default_blocks(context=documenti)

        constraintsDocumenti = ISelectableConstrainTypes(documenti)
        constraintsDocumenti.setConstrainTypesMode(1)
        constraintsDocumenti.setLocallyAllowedTypes(("File",))

        with api.env.adopt_roles(["Reviewer"]):
            api.content.transition(obj=documenti, transition="publish")
