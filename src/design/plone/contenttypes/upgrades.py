# -*- coding: utf-8 -*-
from plone import api
from copy import deepcopy
from plone.app.upgrade.utils import installOrReinstallProduct

import logging
import json

logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"


def update_profile(context, profile):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile)


def update_types(context):
    update_profile(context, "typeinfo")


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_registry(context):
    update_profile(context, "plone.app.registry")


def update_catalog(context):
    update_profile(context, "catalog")


def update_controlpanel(context):
    update_profile(context, "controlpanel")


def remap_fields(mapping):
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    tot = len(brains)
    logger.info("Trovati {} elementi da sistemare.".format(tot))
    # remap fields
    for brain in brains:
        item = brain.getObject()
        for old, new in mapping.items():
            value = getattr(item, old, None)
            if value:
                setattr(item, new, value)
                setattr(item, old, None)
                logger.info(
                    "- {url}: {old} -> {new}".format(
                        url=brain.getURL(), old=old, new=new
                    )
                )
                delattr(item, old)


def to_1001(context):

    update_types(context)

    # cleanup event behaviors
    portal_types = api.portal.get_tool(name="portal_types")
    behaviors = portal_types["Event"].behaviors
    to_remove = [
        "design.plone.contenttypes.behavior.luoghi_correlati",
        "design.plone.contenttypes.behavior.argomenti_evento",
        "design.plone.contenttypes.behavior.additional_help_infos_evento",
    ]
    portal_types["Event"].behaviors = tuple(
        [x for x in behaviors if x not in to_remove]
    )

    mapping = {
        # "descrizione_destinatari": "a_chi_si_rivolge",
        "canale_fisico": "dove_rivolgersi_extra",
        "canale_fisico_prenotazione": "prenota_appuntamento",
        "fasi_scadenze": "tempi_e_scadenze",
        "sedi_e_luoghi": "dove_rivolgersi",
        "box_aiuto": "ulteriori_informazioni",
        "riferimento_telefonico_luogo": "telefono",
        "riferimento_mail_luogo": "email",
    }
    remap_fields(mapping=mapping)


def to_1003(context):

    update_types(context)

    mapping = {
        "unita_amministrativa_responsabile": "unita_amministrative_responsabili",  # noqa
        "sedi": "sede",
        "contatto_reperibilita": "reperibilita",
        "evento_supportato_da": "supportato_da",
    }
    remap_fields(mapping=mapping)


def to_1005(context):
    def fix_index(blocks):
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("query", []):
                    if (
                        query["i"] == "argomenti_correlati"
                        or query["i"] == "tassonomia_argomenti"
                    ):  # noqa
                        query["i"] = "argomenti"
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            fix_index(blocks)
            item.blocks = blocks
    logger.info("** Reindexing items that refers to an argument **")
    for brain in api.portal.get_tool("portal_catalog")():
        item = brain.getObject()
        if getattr(item.aq_base, "tassonomia_argomenti", []):
            logger.info(" - {}".format(brain.getURL()))
            item.reindexObject(idxs=["argomenti"])


def to_1006(context):
    def fix_index(blocks):
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("query", []):
                    if (
                        query["i"] == "argomenti_correlati"
                        or query["i"] == "tassonomia_argomenti"
                        or query["i"] == "argomenti"
                    ):  # noqa
                        query["i"] = "argomenti"
                        query["v"] = [
                            x.Title for x in api.content.find(UID=query["v"])
                        ]
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            fix_index(blocks)
            item.blocks = blocks


def to_1007(context):
    for brain in api.content.find(portal_type="Persona"):
        item = brain.getObject()
        if item.email:
            item.email = [item.email]
        if item.telefono:
            item.telefono = [item.telefono]


def to_1008(context):
    installOrReinstallProduct(api.portal.get(), "redturtle.bandi")


def to_1009(context):
    def fix_index(blocks):
        """
        revert to tassonomia_argomenti
        """
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("query", []):
                    if query["i"] == "argomenti":
                        query["i"] = "tassonomia_argomenti"
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            fix_index(blocks)
            item.blocks = blocks
    logger.info("** Reindexing items that refers to an argument **")
    for brain in api.portal.get_tool("portal_catalog")():
        item = brain.getObject()
        if getattr(item.aq_base, "tassonomia_argomenti", []):
            logger.info(" - {}".format(brain.getURL()))
            item.reindexObject(idxs=["tassonomia_argomenti"])


def to_1010(context):
    pc = api.portal.get_tool(name="portal_catalog")
    pc.manage_reindexIndex(ids=['event_location'])
