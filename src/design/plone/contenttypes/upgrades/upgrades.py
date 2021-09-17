# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.volto.blocksfield.field import BlocksField
from copy import deepcopy
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.upgrades.draftjs_converter import to_draftjs
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.app.upgrade.utils import installOrReinstallProduct
from plone.dexterity.utils import iterSchemata
from redturtle.bandi.interfaces.settings import IBandoSettings
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import getFields

import logging
import json
import six

logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"

# standard upgrades #


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_types(context):
    update_profile(context, "typeinfo")


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


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


# custom ones #


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
    for brain in api.content.find(object_provides="plone.restapi.behaviors.IBlocks"):
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
                        query["v"] = [x.Title for x in api.content.find(UID=query["v"])]
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(object_provides="plone.restapi.behaviors.IBlocks"):
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
    for brain in api.content.find(object_provides="plone.restapi.behaviors.IBlocks"):
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
    pc.manage_reindexIndex(ids=["event_location"])


def to_1013(context):
    def fix_template_name(blocks):
        """
        revert to tassonomia_argomenti
        """
        found = False
        for block in blocks.values():
            if (
                block.get("@type", "") == "listing"
                and block.get("template", "") == "imageGallery"
            ):
                block["template"] = "photogallery"
                found = True
        return found

    # fix root
    logger.info('Changing listing block template from "imageGallery" to "photogallery')
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    to_update = fix_template_name(portal_blocks)
    fixed_items = []
    if to_update:
        portal.blocks = json.dumps(portal_blocks)
        fixed_items.append("Root")
    i = 0
    brains = api.content.find(object_provides="plone.restapi.behaviors.IBlocks")
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            to_update = fix_template_name(blocks)
            if to_update:
                item.blocks = blocks
                fixed_items.append(brain.getPath())

    logger.info("Finish")
    if fixed_items:
        logger.info("Updated items:")
        for fixed in fixed_items:
            logger.info("- {}".format(fixed))
    else:
        logger.info("No items affected.")


def to_1014(context):
    update_types(context)
    portal_types = api.portal.get_tool(name="portal_types")
    portal_types["Bando"].behaviors = tuple(
        [
            x
            for x in portal_types["Bando"].behaviors
            if x != "design.plone.contenttypes.behavior.argomenti"
        ]
    )


def to_1015(context):
    update_types(context)

    # cleanup trasparenza behavior from CTs
    portal_types = api.portal.get_tool(name="portal_types")
    service_behaviors = portal_types["Servizio"].behaviors
    to_remove = [
        "design.plone.contenttypes.behavior.trasparenza",
    ]
    portal_types["Servizio"].behaviors = tuple(
        [x for x in service_behaviors if x not in to_remove]
    )
    persona_behaviors = portal_types["Persona"].behaviors
    portal_types["Persona"].behaviors = tuple(
        [x for x in persona_behaviors if x not in to_remove]
    )


def to_1016(context):
    section_ids = ["amministrazione", "servizi", "novita", "documenti-e-dati"]
    sections = []
    portal = api.portal.get()
    for id in section_ids:
        item = portal.get(id, None)
        if item:
            sections.append({"title": item.title, "linkUrl": [item.UID()]})
    settings = [{"rootPath": "/", "items": sections}]
    api.portal.set_registry_record(
        "search_sections",
        json.dumps(settings),
        interface=IDesignPloneSettings,
    )


def to_2000(context):
    # remove volto.blocks behavior from news and events and add new one
    update_types(context)
    portal_types = api.portal.get_tool(name="portal_types")
    for ptype in ["News Item", "Event"]:
        portal_types[ptype].behaviors = tuple(
            [x for x in portal_types[ptype].behaviors if x != "volto.blocks"]
        )
    portal_types["Pagina Argomento"].behaviors = tuple(
        [
            x
            for x in portal_types["Pagina Argomento"].behaviors
            if x != "design.plone.contenttypes.behavior.additional_help_infos"
        ]
    )
    # now copy values in new fields
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    tot = len(brains)
    i = 0
    logger.info("### START CONVERSION FIELDS RICHTEXT -> DRAFTJS ###")
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item = brain.getObject()
        if brain.portal_type in ["Event", "News Item"]:
            blocks = getattr(item, "blocks", {})
            blocks_layout = getattr(item, "blocks_layout", {"items": []})["items"]
            if not blocks:
                continue
            title_uid = ""
            new_blocks = {}
            for uid, block in blocks.items():
                if block.get("@type", "") == "title":
                    title_uid = uid
                else:
                    new_blocks[uid] = block
            item.descrizione_estesa = {
                "blocks": new_blocks,
                "blocks_layout": {
                    "items": [x for x in blocks_layout if x != title_uid]
                },
            }
            item.blocks = None
            item.blocks_layout = None
        for schema in iterSchemata(item):
            for name, field in getFields(schema).items():
                if not isinstance(field, BlocksField):
                    continue
                value = field.get(item)
                if not value:
                    continue
                if isinstance(value, six.string_types):
                    value = "<p>{}</p>".format(value)
                elif isinstance(value, RichTextValue):
                    value = value.raw
                else:
                    continue
                if value == "<p><br></p>":
                    value = ""
                try:
                    new_value = to_draftjs(value)
                except Exception as e:
                    logger.error(
                        "[NOT MIGRATED] - {}: {}".format(brain.getPath(), name)
                    )
                    raise e
                setattr(item, name, new_value)


def to_2002(context):
    """Per l'aggiornamento del vocabolario tipologie_persona, sistemiamo
    tutti quelli già presenti.
    """
    type_mapping = {
        "altro": "Altro tipo",
        "politica": "Politica",
        "amministrativa": "Amministrativa",
    }
    logger.info("Fixing 'Tipologia Persona'...")
    fixed_total = 0
    for brain in api.content.find(portal_type="Persona"):
        item = brain.getObject()
        if item.tipologia_persona in type_mapping:
            item.tipologia_persona = type_mapping[item.tipologia_persona]
            fixed_total += 1
        commit()
    logger.info("Fixing 'Tipologia Persona': DONE")
    logger.info("Updated {} objects".format(fixed_total))


def to_3000(context):
    """ """
    update_registry(context)
    update_controlpanel(context)
    multilanguage = [
        "tipologie_notizia",
        "tipologie_unita_organizzativa",
        "tipologie_documento",
        "tipologie_persona",
    ]
    simple = ["lead_image_dimension", "search_sections"]
    old_entry = "design.plone.contenttypes.controlpanels.vocabularies.IVocabulariesControlPanel.{}"  # noqa
    for field in simple:
        value = api.portal.get_registry_record(old_entry.format(field))
        api.portal.set_registry_record(field, value, interface=IDesignPloneSettings)

    for field in multilanguage:
        try:
            value = api.portal.get_registry_record(old_entry.format(field))
            api.portal.set_registry_record(
                field,
                json.dumps({"it": value}),
                interface=IDesignPloneSettings,
            )
        except Exception:
            continue

    context.runAllImportStepsFromProfile("profile-design.plone.contenttypes:to_3000")


def to_3101(context):
    intids = getUtility(IIntIds)
    logger.info("Fixing Documento references...")
    fixed_total = 0
    for brain in api.content.find(portal_type="Documento"):
        item = brain.getObject()
        for rel in getattr(item, "servizi_collegati", []):
            service = rel.to_object
            if service:
                service.altri_documenti.append(RelationValue(intids.getId(item)))
                notify(ObjectModifiedEvent(service))
                logger.info("Fixed item {}".format("/".join(service.getPhysicalPath())))

        if getattr(item, "servizi_collegati", []):
            delattr(item, "servizi_collegati")
            notify(ObjectModifiedEvent(item))
            fixed_total += 1
            logger.info("Fixed item {}".format("/".join(item.getPhysicalPath())))

    logger.info("Fixing 'Documento': DONE")
    logger.info("Updated {} objects Documento".format(fixed_total))


def to_3102(context):
    update_types(context)

    # cleanup trasparenza behavior from CTs
    portal_types = api.portal.get_tool(name="portal_types")
    to_remove = [
        "design.plone.contenttypes.behavior.trasparenza",
    ]
    for key, value in portal_types.items():
        ct_behaviors = getattr(value, "behaviors", None)
        if ct_behaviors is not None:
            portal_types[key].behaviors = tuple(
                [x for x in ct_behaviors if x not in to_remove]
            )


def to_volto13(context):  # noqa: C901
    # convert listing blocks with new standard

    logger.info("### START CONVERSION TO VOLTO 13: default => simpleCard ###")

    def fix_listing(blocks, url):
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                if block.get("template", False) and not block.get("variation", False):
                    # import pdb

                    # pdb.set_trace()
                    logger.error("- {}".format(url))
                if block.get("template", False) and block.get("variation", False):
                    logger.error("- {}".format(url))
                if block.get("variation", "") == "default":
                    block["variation"] = "simpleCard"
                    logger.info("- {}".format(url))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_listing(portal_blocks, portal.absolute_url())
    portal.blocks = json.dumps(portal_blocks)

    # fix blocks in contents
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item = aq_base(brain.getObject())
        if getattr(item, "blocks", {}):
            blocks = deepcopy(item.blocks)
            if blocks:
                fix_listing(blocks, brain.getURL())
                item.blocks = blocks
        for schema in iterSchemata(item):
            # fix blocks in blocksfields
            for name, field in getFields(schema).items():
                if name == "blocks":
                    blocks = deepcopy(item.blocks)
                    if blocks:
                        fix_listing(blocks, brain.getURL())
                        item.blocks = blocks
                elif isinstance(field, BlocksField):
                    value = deepcopy(field.get(item))
                    if not value:
                        continue
                    if isinstance(value, str):
                        if value == "":
                            setattr(
                                item,
                                name,
                                {"blocks": {}, "blocks_layout": {"items": []}},
                            )
                            continue
                    try:
                        blocks = value.get("blocks", {})
                    except AttributeError:
                        logger.warning(
                            "[RICHTEXT] - {} (not converted)".format(brain.getURL())
                        )
                    if blocks:
                        fix_listing(blocks, brain.getURL())
                        setattr(item, name, value)


def to_3400(context):  # noqa: C901
    logger.info("### START CONVERSION BLOCKS: newsHome -> highlitedContent ###")

    def fix_block(blocks, url):
        for block in blocks.values():
            if block.get("@type", "") == "newsHome":
                block["@type"] = "highlitedContent"

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_block(portal_blocks, portal.absolute_url())
    portal.blocks = json.dumps(portal_blocks)

    # fix blocks in contents
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item = aq_base(brain.getObject())
        if getattr(item, "blocks", {}):
            blocks = deepcopy(item.blocks)
            if blocks:
                fix_block(blocks, brain.getURL())
                item.blocks = blocks
        for schema in iterSchemata(item):
            # fix blocks in blocksfields
            for name, field in getFields(schema).items():
                if name == "blocks":
                    blocks = deepcopy(item.blocks)
                    if blocks:
                        fix_block(blocks, brain.getURL())
                        item.blocks = blocks
                elif isinstance(field, BlocksField):
                    value = deepcopy(field.get(item))
                    if not value:
                        continue
                    if isinstance(value, str):
                        if value == "":
                            setattr(
                                item,
                                name,
                                {"blocks": {}, "blocks_layout": {"items": []}},
                            )
                            continue
                    try:
                        blocks = value.get("blocks", {})
                    except AttributeError:
                        logger.warning(
                            "[RICHTEXT] - {} (not converted)".format(brain.getURL())
                        )
                    if blocks:
                        fix_block(blocks, brain.getURL())
                        setattr(item, name, value)


def to_3401(context):  # noqa: C901
    logger.info("File type can now be added inside a CartellaModulistica")
    update_types(context)


def to_3500(context):
    logger.info("Add new index and reindex UO")
    update_catalog(context)

    # remove unused index
    catalog = api.portal.get_tool(name="portal_catalog")
    if "office_venue" in catalog.indexes():
        catalog.manage_delIndex("office_venue")

    # reindex
    brains = api.content.find(portal_type="UnitaOrganizzativa")
    tot = len(brains)
    logger.info("Found {} UO.".format(tot))
    i = 0
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        uo = brain.getObject()
        uo.reindexObject(idxs=["uo_location", "tipologia_organizzazione"])


def to_3501(context):
    logger.info("Reindex UO for new SearchableText fields")

    brains = api.content.find(portal_type="UnitaOrganizzativa")
    tot = len(brains)
    logger.info("Found {} UO.".format(tot))
    i = 0
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        uo = brain.getObject()
        uo.reindexObject(idxs=["SearchableText"])


def to_3600(context):
    logger.info("Enable kitconcept.seo behavior")
    types_list = [
        "UnitaOrganizzativa",
        "Bando",
        "Subsite",
        "Venue",
        "Persona",
        "Event",
        "News Item",
        "Document",
        "Documento",
        "Servizio",
        "CartellaModulistica",
        "Pagina Argomento",
    ]
    portal_types = api.portal.get_tool(name="portal_types")
    for ct_type in types_list:
        if "kitconcept.seo" not in portal_types[ct_type].behaviors:
            portal_types[ct_type].behaviors += ("kitconcept.seo",)
            logger.info("Enabled kitconcept.seo on: {}".format(ct_type))

    logger.info("Bandi customizations")
    update_catalog(context)
    api.portal.set_registry_record("default_ente", (), interface=IBandoSettings)

    portal_types = api.portal.get_tool(name="portal_types")
    portal_types["Bando Folder Deepening"].allowed_content_types = (
        "Modulo",
        "File",
        "Link",
    )
    portal_types["Bando"].default_view = "view"
    portal_types["Bando"].view_methods = ("view",)

    logger.info("Reindex SearchableText")
    pc = api.portal.get_tool(name="portal_catalog")
    pc.reindexIndex("SearchableText", context.REQUEST)

    logger.info("Reindex Bandi")
    i = 0
    brains = api.content.find(portal_type="Bando")
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        bando = brain.getObject()
        bando.reindexObject(idxs=["ufficio_responsabile_bando", "Subject_bando"])


def to_3700(context):
    logger.info("Set show_modified_default as True")

    api.portal.set_registry_record(
        "show_modified_default", True, interface=IDesignPloneSettings
    )
