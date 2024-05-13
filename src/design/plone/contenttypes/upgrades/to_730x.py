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
        FOLDER_ID = "altri-documenti"
        if FOLDER_ID not in persona.keys():
            child = api.content.create(
                container=persona,
                type="Document",
                title="Altri documenti",
                id=FOLDER_ID,
            )
            create_default_blocks(context=child)
        else:
            child = persona[FOLDER_ID]

        child.exclude_from_search = True
        child.reindexObject(idxs=["exclude_from_search"])
        # select constraints
        constraintsChild = ISelectableConstrainTypes(child)
        constraintsChild.setConstrainTypesMode(1)
        constraintsChild.setLocallyAllowedTypes(
            (
                "File",
                "Documento",
                "Link",
            )
        )
        if api.content.get_state(persona) == "published":
            if api.content.get_state(child) != "published":
                with api.env.adopt_roles(["Reviewer"]):
                    api.content.transition(obj=child, transition="publish")
