# -*- coding: utf-8 -*-
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes

import logging


logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"


def to_7301(context):
    brains = api.content.find(portal_type="Persona")
    for brain in brains:
        persona = brain.getObject()
        child = api.content.create(
            container=persona,
            type="Document",
            title="Altri allegati",
            id="altri-allegati",
        )
        create_default_blocks(context=child)
        child.exclude_from_search = True
        child.reindexObject(idxs=["exclude_from_search"])
        # select constraints
        constraintsChild = ISelectableConstrainTypes(child)
        constraintsChild.setConstrainTypesMode(1)
        constraintsChild.setLocallyAllowedTypes(
            (
                "File",
                "Image",
                "Link",
            )
        )
        if api.content.get_state(persona) == "published":
            with api.env.adopt_roles(["Reviewer"]):
                api.content.transition(obj=child, transition="publish")
