# -*- coding: utf-8 -*-
from design.plone.contenttypes.events.common import SUBFOLDERS_MAPPING
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes

import logging
import transaction


logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_catalog(context):
    update_profile(context, "catalog")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


def update_types(context):
    update_profile(context, "typeinfo")


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
    brains = context.portal_catalog(**{"portal_type": "Event"})
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
    mapping = [
        folder for folder in mapping.get("content") if folder["id"] == "modulistica"
    ][
        0
    ]  # noqa
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


def to_7306(context):
    logger.info("Enable plone.constraintypes behavior and filter types")

    portal_types = api.portal.get_tool(name="portal_types")
    behavior = "plone.constraintypes"
    for ct in ["Persona", "Incarico"]:
        portal_type = portal_types.get(ct, None)
        if portal_type:
            portal_type.filter_content_types = True
            behaviors = list(portal_type.behaviors)
            if behavior not in behaviors:
                behaviors.append(behavior)
                portal_type.behaviors = tuple(behaviors)


def to_7307(context):
    logger.info("Update registry")
    update_registry(context)
    logger.info("Add new effectivestart (DateRecurringIndex) index")

    class extra:
        recurdef = "recurrence"
        until = ""

    name = "effectivestart"
    catalog = api.portal.get_tool(name="portal_catalog")
    catalog.addIndex(name, "DateRecurringIndex", extra=extra())
    logger.info("Catalog DateRecurringIndex {} created.".format(name))


def to_7308(context):
    logger.info("Reindex Events")
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc(portal_type="Event")
    tot = len(brains)
    for i, brain in enumerate(brains):
        if i % 15 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        brain.getObject().reindexObject(idxs=["effectivestart"])
