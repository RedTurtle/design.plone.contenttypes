# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import installOrReinstallProduct
from design.plone.contenttypes.events.common import SUBFOLDERS_MAPPING
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from design.plone.contenttypes.events.common import createStructure
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


def to_7309(context):
    logger.info("Uninstall eea.api.taxonomy")
    ps = api.portal.get_tool(name="portal_setup")
    ps.runAllImportStepsFromProfile(
        "profile-design.plone.contenttypes:remove_eea_api_taxonomy"
    )
    ps.unsetLastVersionForProfile("eea.api.taxonomy:default")
    logger.info("Install blocksfield")
    installOrReinstallProduct(api.portal.get(), "collective.volto.blocksfield")


def to_7310(context):
    logger.info("Enable kitconcept.seo behavior to File")
    portal_types = api.portal.get_tool(name="portal_types")
    behavior = "kitconcept.seo"
    for ct in ["File"]:
        portal_type = portal_types.get(ct, None)
        if portal_type:
            behaviors = list(portal_type.behaviors)
            if behavior not in behaviors:
                behaviors.append(behavior)
                portal_type.behaviors = tuple(behaviors)


def to_7311(context):
    allowed = list(context.portal_types["Documento"].allowed_content_types)
    if "File" not in allowed:
        allowed.append("File")
        context.portal_types["Documento"].allowed_content_types = tuple(allowed)
    logger.info("Update ct documento addables")


def to_7312(context):
    """
    Only add metadata if missing. We don't want to force reindexing.
    """
    pc = api.portal.get_tool(name="portal_catalog")
    for column in ["image_caption", "preview_caption"]:
        if column not in pc.schema():
            pc.addColumn(column)


def to_7313(context):
    logger.info("Update registry")
    context.runImportStepFromProfile(
        "profile-design.plone.contenttypes:to_7313", "plone.app.registry", False
    )

    logger.info("Add new effectiveend (DateRecurringIndex) index")

    class extra:
        recurdef = "recurrence"
        until = ""

    name = "effectiveend"
    catalog = api.portal.get_tool(name="portal_catalog")

    if "effectiveend" not in catalog.indexes():
        catalog.addIndex(name, "DateRecurringIndex", extra=extra())
        logger.info("Catalog DateRecurringIndex {} created.".format(name))

    logger.info("Reindex Events")
    brains = catalog(portal_type="Event")
    tot = len(brains)
    for i, brain in enumerate(brains):
        if i % 15 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        brain.getObject().reindexObject(idxs=["effectiveend"])


def to_7314(context):
    logger.info("Add new folder to Persona CT")
    mapping1 = {
        "content": [
            {
                "id": "dichiarazione-insussistenza-cause-di-inconferibilita-e-incompatibilita",  # noqa
                "title": "Dichiarazione insussistenza cause di inconferibilità e"
                " incompatibilità",
                "allowed_types": ("File",),
            },
        ]
    }
    mapping2 = {
        "content": [
            {
                "id": "emolumenti-complessivi-percepiti-a-carico-della-finanza-pubblica",  # noqa
                "title": "Emolumenti complessivi percepiti a carico della finanza"
                " pubblica",
                "allowed_types": ("File",),
            },
        ]
    }
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc(portal_type="Persona")
    for brain in brains:
        persona = brain.getObject()
        actual_contraints = ISelectableConstrainTypes(persona)
        actual_constrain_type = actual_contraints.getConstrainTypesMode()
        # devo poter aggiungere
        actual_contraints.setConstrainTypesMode(0)
        if (
            "dichiarazione-insussistenza-cause-di-inconferibilita-e-incompatibilita"
            not in persona.keys()
        ):
            createStructure(persona, mapping1)
            logger.info("Add dichiarazione insussistenza for {}".format(persona.title))
        if (
            "emolumenti-complessivi-percepiti-a-carico-della-finanza-pubblica"
            not in persona.keys()
        ):
            createStructure(persona, mapping2)
            logger.info("Add emolumenti complessivi for {}".format(persona.title))
        # reimposto il valore precedente del constraintypes
        actual_contraints.setConstrainTypesMode(actual_constrain_type)
