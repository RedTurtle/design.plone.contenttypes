# -*- coding: utf-8 -*-
from design.plone.contenttypes.utils import create_default_blocks
from design.plone.contenttypes.events.common import SUBFOLDERS_MAPPING
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
import transaction
import logging


logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_catalog(context):
    update_profile(context, "catalog")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


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


def to_7302(context):
    update_catalog(context)
    brains = api.content.find(portal_type="Event")
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        event = brain.getObject()
        event.reindexObject(idxs=["rassegna"])


def to_7303(context):
    update_registry(context)
    logger.info("Update registry")


def to_7304(context):
    brains = context.portal_catalog()
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
            transaction.commit()
        doc = brain.getObject()
        doc.reindexObject(idxs=["parent"])


def to_7305(context):
    mapping = SUBFOLDERS_MAPPING["Servizio"]
    mapping = [folder for folder in mapping if folder["id"] == "modulistica"][0]
    brains = api.content.find(portal_type="Servizio")
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
            transaction.commit()
        servizio = brain.getObject()
        FOLDER_ID = "modulistica"
        if FOLDER_ID not in servizio.keys():
            continue
        child = servizio[FOLDER_ID]
        constraintsChild = ISelectableConstrainTypes(child)
        constraintsChild.setConstrainTypesMode(1)
        constraintsChild.setLocallyAllowedTypes(mapping["allowed_types"])
