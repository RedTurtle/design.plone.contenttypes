# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.volto.blocksfield.field import BlocksField
from copy import deepcopy
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.setuphandlers import remove_blocks_behavior
from design.plone.contenttypes.upgrades.draftjs_converter import to_draftjs
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.app.upgrade.utils import installOrReinstallProduct
from plone.base.interfaces.syndication import ISiteSyndicationSettings
from plone.dexterity.utils import iterSchemata
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from redturtle.bandi.interfaces.settings import IBandoSettings
from transaction import commit
from uuid import uuid4
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import getFields
from design.plone.contenttypes.events.common import SUBFOLDERS_MAPPING

import json
import logging
import six


logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"

# standard upgrades #


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_actions(context):
    update_profile(context, "actions")


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


def reindex_catalog(context, idxs):
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    for brain in brains:
        if idxs:
            brain.getObject().reindexObject(idxs=idxs)
        else:
            brain.getObject().reindexObject()


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


def to_2000(context):  # noqa: C901
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
        if (
            hasattr(item, "tipologia_persona")
            and item.tipologia_persona in type_mapping
        ):  # noqa
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
        # "tipologie_documento",
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


def to_3800(context):
    logger.info("Fix Venue addable types")

    portal_types = api.portal.get_tool(name="portal_types")
    portal_types["Venue"].allowed_content_types = (
        "Folder",
        "Image",
        "File",
        "Link",
    )


def to_3900(context):
    logger.info("Add new metadata: ruolo")

    brains = api.content.find(portal_type="Persona")
    for brain in brains:
        persona = brain.getObject()
        persona.reindexObject()


def to_4000(context):
    logger.info("Move ruolo to a choice field")
    ruoli = {"it": [], "en": []}
    brains = api.content.find(portal_type="Persona")
    for brain in brains:
        persona = brain.getObject()
        ruolo = getattr(persona, "ruolo", "")
        lang = brain.language
        if ruolo not in ruoli[lang]:
            ruoli[lang].append(ruolo)

    if api.portal.get_registry_record(
        "ruoli_persona", interface=IDesignPloneSettings, default=None
    ):
        api.portal.set_registry_record(
            "ruoli_persona", json.dumps(ruoli), interface=IDesignPloneSettings
        )


def to_4100(context):
    logger.info("Add constrainttypes behavior to Document")

    portal_types = api.portal.get_tool(name="portal_types")
    document_behaviors = list(portal_types["Document"].behaviors) + [
        "plone.constraintypes"
    ]
    portal_types["Document"].behaviors = tuple(document_behaviors)


def to_4200(context):
    logger.info("Add criteria and indexes to Persona")

    update_catalog(context)
    update_registry(context)

    brains = api.content.find(portal_type="Persona")
    for brain in brains:
        persona = brain.getObject()
        persona.reindexObject(idxs=["data_conclusione_incarico"])


def to_5000(context):
    logger.info("Enable preview_image behavior in all content types")

    portal_types = api.portal.get_tool(name="portal_types")

    for portal_type, fti in portal_types.items():
        behaviors = list(getattr(fti, "behaviors", ()))
        if not behaviors:
            continue
        if portal_type == "Document":
            behaviors = [
                x
                for x in behaviors
                if x not in ["plone.leadimage", "volto.preview_image"]
            ]
            behaviors.extend(["plone.leadimage", "volto.preview_image"])
        else:
            if "plone.leadimage" not in behaviors or "volto.preview_image" in behaviors:
                continue
        behaviors.insert(behaviors.index("plone.leadimage") + 1, "volto.preview_image")
        fti.behaviors = tuple(behaviors)

    logger.info("Move immagine_testata to image")
    catalog = api.portal.get_tool("portal_catalog")
    i = 0
    brains = catalog()
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 500 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        obj = brain.getObject()
        if "image" in obj.keys():
            api.content.rename(obj=obj["image"], new_id="image-1")
        if brain.portal_type == "Document":
            immagine_testata = getattr(obj, "immagine_testata", None)
            if immagine_testata:
                obj.image = immagine_testata
                obj.immagine_testata = None
        catalog.catalog_object(obj)


def to_5001(context):
    catalog = api.portal.get_tool("portal_catalog")
    i = 0
    brains = catalog(portal_type="Pagina Argomento")
    tot = len(brains)
    logger.info("Add icona metadata to {}".format(tot))
    for brain in brains:
        i += 1
        if i % 500 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        obj = brain.getObject()
        catalog.catalog_object(obj)


def to_5002(context):
    """
    Reindex non-folderish items because there were some metadata not updated
    """
    catalog = api.portal.get_tool("portal_catalog")
    i = 0
    brains = catalog(is_folderish=False)
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 500 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        obj = brain.getObject()
        catalog.catalog_object(obj)


def to_5200(context):
    """
    add new behavior for Bando
    """
    portal_types = api.portal.get_tool(name="portal_types")
    fti = portal_types["Bando"]
    behaviors = list(getattr(fti, "behaviors", ()))
    if "design.plone.contenttypes.behavior.update_note" not in behaviors:
        behaviors.append("design.plone.contenttypes.behavior.update_note")
        fti.behaviors = tuple(behaviors)


def to_5210(context):
    logger.info("Enable preview_image behavior in Bandi content types")

    portal_types = api.portal.get_tool(name="portal_types")
    fti = portal_types["Bando"]
    behaviors = list(getattr(fti, "behaviors", ()))
    if "volto.preview_image" not in behaviors:
        behaviors.append("volto.preview_image")
        fti.behaviors = tuple(behaviors)


def to_5220(context):
    """
    Reindex Venues
    """
    logger.info("Reindex SearchableText for Venue items.")
    catalog = api.portal.get_tool("portal_catalog")
    i = 0
    brains = catalog(portal_type="Venue")
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 500 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        obj = brain.getObject()
        obj.reindexObject(idxs=["SearchableText", "object_provides"])


def to_5300(context):
    update_profile(context, "plone-difftool")
    update_profile(context, "repositorytool")

    portal_types = api.portal.get_tool(name="portal_types")
    for portal_type, fti in portal_types.items():
        if portal_type in [
            "CartellaModulistica",
            "Documento",
            "Link",
            "Pagina Argomento",
            "Persona",
            "Servizio",
            "UnitaOrganizzativa",
            "Venue",
        ]:
            behaviors = list(getattr(fti, "behaviors", ()))
            if "plone.versioning" not in behaviors:
                behaviors.append("plone.versioning")
                fti.behaviors = tuple(behaviors)


def to_5310(context):
    """
    Reindex Bandi
    """
    logger.info("Reindex SearchableText for Bandi items.")
    catalog = api.portal.get_tool("portal_catalog")
    i = 0
    brains = catalog(portal_type="Bando")
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 500 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        brain.getObject().reindexObject(idxs=["SearchableText"])


def to_5400(context):
    logger.info('Remove "volto.blocks" behavior from News Item and Event.')
    remove_blocks_behavior(context)


def to_5410(context):
    # cleanup Document behaviors
    portal_types = api.portal.get_tool(name="portal_types")
    behaviors = portal_types["Document"].behaviors
    to_remove = [
        "plone.tableofcontents",
    ]
    portal_types["Document"].behaviors = tuple(
        [x for x in behaviors if x not in to_remove]
    )


def to_5500(context):
    update_registry(context)
    update_catalog(context)

    argomenti_mapping = {
        x.Title: x.UID for x in api.content.find(portal_type="Pagina Argomento")
    }

    def fix_block(blocks, argomenti_mapping):
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("querystring", {}).get("query", []):
                    if query["i"] == "tassonomia_argomenti":
                        new_values = []
                        for v in query["v"]:
                            uid = argomenti_mapping.get(v, "")
                            if uid:
                                new_values.append(uid)
                        query["i"] = "tassonomia_argomenti_uid"
                        query["v"] = new_values
                        logger.info(" - {}".format(brain.getURL()))

    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item_obj = brain.getObject()
        item = aq_base(brain.getObject())

        # reindex argomenti indexes
        if brain.tassonomia_argomenti:
            item_obj.reindexObject(
                idxs=["tassonomia_argomenti", "tassonomia_argomenti_uid"]
            )

        if getattr(item, "blocks", {}):
            blocks = deepcopy(item.blocks)
            if blocks:
                fix_block(blocks, argomenti_mapping)
                item.blocks = blocks
        for schema in iterSchemata(item):
            # fix blocks in blocksfields
            for name, field in getFields(schema).items():
                if name == "blocks":
                    blocks = deepcopy(item.blocks)
                    if blocks:
                        fix_block(blocks, argomenti_mapping)
                        item.blocks = blocks
                elif isinstance(field, BlocksField):
                    value = deepcopy(field.get(item))
                    if not value:
                        continue
                    blocks = value.get("blocks", {})
                    if blocks:
                        fix_block(blocks, argomenti_mapping)
                        setattr(item, name, value)


def to_6000(context):
    """ """
    logger.info(
        "Convert behavior: collective.dexteritytextindexer => plone.textindexer"  # noqa
    )
    portal_types = api.portal.get_tool(name="portal_types")
    for fti in portal_types.values():
        behaviors = []
        for behavior in getattr(fti, "behaviors", ()):
            if behavior == "collective.dexteritytextindexer":
                behavior = "plone.textindexer"
            behaviors.append(behavior)

        fti.behaviors = tuple(behaviors)


def to_6010(context):
    """ """
    update_types(context)
    update_registry(context)
    update_catalog(context)
    update_rolemap(context)


def to_6011(context):
    """ """
    update_types(context)


def migrate_pdc_and_incarico(context):
    # Cannot test rn, blind coding
    update_types(context)
    update_registry(context)
    update_catalog(context)
    update_rolemap(context)
    # "field name in original ct": "field name in new ct"
    type_mapping = {
        "Persona": {
            "PDC": {
                "telefono": "telefono",
                "fax": "fax",
                "email": "email",
                "pec": "pec",
            },  # noqa
            "Incarico": {
                # HOW? Need taxonomies also
                # We could do:
                # persona.ruolo.title = incarico.title
                # persona.items.compensi = incarico.items.compensi?
                "ruolo?": "incarico?",
                # BlobFile to relation with Documento
                "atto_nomina": "atto_nomina",
                "data_conclusione_incarico": "data_conclusione_incarico",
                "data_insediamento": "data_insediamento",
            },
        },
        "UnitaOrganizzativa": {
            "PDC": {
                "telefono": "telefono",
                "fax": "fax",
                "email": "email",
                "pec": "pec",
                "web": "web",
            },
        },
        # TODO: tbc
        "Event": {
            "PDC": {
                "telefono": "telefono",
                "fax": "fax",
                "email": "email",
                "pec": "pec",
            },  # noqa
        },
        # TODO: tbc
        "Venue": {
            "PDC": {
                "riferimento_telefonico_struttura": "telefono",
                "riferimento_fax_struttura": "fax",
                "riferimento_mail_struttura": "email",
                "riferimento_pec_struttura": "pec",
            },
        },
        # TODO: tbc
        "Servizio": {
            # questi non sono presenti sul ct originale
            "PDC": {
                "telefono": "telefono",
                "fax": "fax",
                "email": "email",
                "pec": "pec",
            },  # noqa
        },
    }

    def createIncaricoAndMigratePersona(portal_type):
        # Taxonomies work needs to be completed before, blind coding ahead
        if portal_type == "Persona":
            fixed_total = 0
            for brain in api.content.find(portal_type=portal_type):
                item = brain.getObject()
                atto_nomina = item.atto_nomina
                logger.info(f"Fixing Punto di Contatto for '{item.title}'...")  # noqa
                file_bog = api.content.find(context=item, depth=1, id="atti-nomina")
                if not file_bog:
                    try:
                        file_bog = api.content.create(
                            type="Document",
                            id="atti-nomina",
                            title="Atti Nomina",
                            container=item,
                        )
                    except Exception:
                        logger.error("Error", Exception)

                try:
                    new_atto_nomina = api.content.create(
                        type="File",
                        id=atto_nomina.id,
                        title=atto_nomina.title,
                        container=item,
                        **{"file": atto_nomina},
                    )
                    intids = getUtility(IIntIds)
                    relation = [RelationValue(intids.getId(new_atto_nomina))]
                    incarico = api.content.create(
                        type="Incarico", title=item.ruolo.title, container=item
                    )
                    incarico.atto_nomina = relation
                    item.atto_nomina = None
                    fixed_total += 1
                    logger.info(
                        f"Fixing Punto di Contatto for '{item.title}'...:DONE"
                    )  # noqa
                except Exception:
                    logger.error("Error", Exception)
            logger.info("Updated {} objects".format(fixed_total))

        pass

    def createPDCandMigrateOldCTs(portal_type):
        logger.info(f"Fixing Punto di Contatto for '{portal_type}'...")  # noqa
        fixed_total = 0
        mapping = None
        # mapping = type_mapping[portal_type]["PDC"]
        # Reenable mapping to use
        if not mapping:
            logger.info(f"No need to fix Punto di Contatto for '{portal_type}: DONE")
            return
        for brain in api.content.find(portal_type=portal_type):
            item = brain.getObject()
            kwargs = {"value_punto_contatto": [], "persona": []}
            for key, value in mapping.items():
                if hasattr(item, key):
                    kwargs["value_punto_contatto"].append(
                        {"pdc_type": value, "pdc_value": item[key]}
                    )

            new_pdc = api.content.create(
                type="PuntoDiContatto",
                title=f"Punto di Contatto {item.id}",
                container=item,
                **kwargs,
            )
            intids = getUtility(IIntIds)
            item.contact_info = [RelationValue(intids.getId(new_pdc))]
            fixed_total += 1
            commit()

        logger.info(f"Fixing Punto di Contatto for '{portal_type}: DONE")
        logger.info("Updated {} objects".format(fixed_total))

    for pt in type_mapping:
        logger.info(
            "Migrating existing CTs for use with new Incarico and PDC Content Types"
        )
        createPDCandMigrateOldCTs(pt)
        createIncaricoAndMigratePersona(pt)


class colors(object):
    GREEN = "\033[92m"
    ENDC = "\033[0m"
    RED = "\033[91m"
    DARKCYAN = "\033[36m"
    YELLOW = "\033[93m"


def update_uo_contact_info(context):
    brains = api.portal.get_tool("portal_catalog")(portal_type="UnitaOrganizzativa")
    logger.info(
        f"{colors.DARKCYAN} Inizio la pulzia delle {len(brains)} UO campo contact_info {colors.ENDC}"  # noqa
    )
    for brain in brains:
        obj = brain.getObject()
        if type(obj.contact_info) == dict:  # noqa
            del obj.contact_info
            logger.info(
                f"{colors.GREEN} Modifica della UO senza punto di contatto {colors.ENDC}"  # noqa
            )


def readd_tassonomia_argomenti_uid(context):
    logger.info(
        f"{colors.DARKCYAN} Aggiungo la tassonomia_argomenti_uid e reindicizzo{colors.ENDC}"  # noqa
    )
    update_catalog(context)
    update_registry(context)
    idxs = ["tassonomia_argomenti_uid", "tassonomia_argomenti"]
    reindex_catalog(context, idxs)


def update_ruolo_indexing(context):
    logger.info(
        f"{colors.DARKCYAN} Reindex del ruolo nelle persone {colors.ENDC}"  # noqa
    )
    idxs = ["ruolo"]
    pc = api.portal.get_tool("portal_catalog")
    brains = pc(portal_type="Persona")
    for brain in brains:
        persona = brain.getObject()
        persona.reindexObject(idxs=idxs)


def fix_ctaxonomy_indexes_and_metadata(context):
    logger.info(f"{colors.DARKCYAN} Fix taxonomy indexes {colors.ENDC}")  # noqa
    bad_names = [
        "taxonomy_person_life_events",
        "taxonomy_business_events",
        "taxonomy_temi_dataset",
        "taxonomy_tipologia_documenti_albopretorio",
        "taxonomy_tipologia_documento",
        "taxonomy_tipologia_evento",
        "taxonomy_tipologia_frequenza_aggiornamento",
        "taxonomy_tipologia_incarico",
        "taxonomy_tipologia_licenze",
        "taxonomy_tipologia_luogo",
        "taxonomy_tipologia_notizia",
        "taxonomy_tipologia_organizzazione",
        "taxonomy_tipologia_pdc",
        "taxonomy_tipologia_stati_pratica",
    ]

    good_names = [name.replace("taxonomy_", "") for name in bad_names]
    catalog = api.portal.get_tool(name="portal_catalog")
    catalog_metadata = catalog.schema()
    catalog_indexes = catalog.indexes()

    for name in bad_names:
        # metadata
        if name in catalog_metadata:
            catalog.delColumn(name)
            logger.info(f"{colors.GREEN} Remove {name} from metadata {colors.ENDC}")

        # indexes
        if name in catalog_indexes:
            catalog.delIndex(name)
            logger.info(f"{colors.GREEN} Remove {name} from indexes {colors.ENDC}")

    context.runImportStepFromProfile(
        "design.plone.contenttypes:taxonomy", "collective.taxonomy"
    )
    brains = catalog(
        portal_type=[
            "News Item",
            "Event",
            "Venue",
            "Servizio",
            "Documento",
            "Dataset",
            "UnitaOrganizzativa",
            "Incarico",
            "Pratica",
        ]
    )
    logger.info(f"{colors.GREEN} Reindex contents with taxonomies {colors.ENDC}")
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=good_names)
    logger.info(f"{colors.GREEN} End of update {colors.ENDC}")


def update_patrocinato_da(self):
    EMPTY_BLOCKS_FIELD = {"blocks": {}, "blocks_layout": {"items": []}}
    logger.info(
        f"{colors.DARKCYAN} Change patrocinato_da field in events {colors.ENDC}"
    )
    pc = api.portal.get_tool(name="portal_catalog")
    for brain in pc(portal_type="Event"):
        obj = brain.getObject()
        patrocinato_da = getattr(obj, "patrocinato_da")
        if patrocinato_da == EMPTY_BLOCKS_FIELD:
            logger.info(
                f"{colors.YELLOW} Nessuna informazione da modificare{colors.ENDC}"
            )
            continue
        url = obj.absolute_url()
        logger.info(f"{colors.GREEN} patrocinato_da ({url}){colors.ENDC}")

        setattr(
            obj,
            "patrocinato_da",
            {
                "blocks": {
                    "d252fe92-ce88-4866-b77d-501e7275cfc0": {
                        "@type": "text",
                        "text": {
                            "blocks": [
                                {
                                    "data": {},
                                    "depth": 0,
                                    "entityRanges": [],
                                    "inlineStyleRanges": [],
                                    "key": "e23it",
                                    "text": patrocinato_da,
                                    "type": "unstyled",
                                }
                            ],
                            "entityMap": {},
                        },
                    }
                },
                "blocks_layout": {"items": ["d252fe92-ce88-4866-b77d-501e7275cfc0"]},
            },
        )
        obj.reindexObject()
    logger.info(f"{colors.DARKCYAN} End of update {colors.ENDC}")


def update_folder_for_gallery(self):
    logger.info(f"{colors.DARKCYAN} Update events {colors.ENDC}")
    pc = api.portal.get_tool(name="portal_catalog")
    for brain in pc(portal_type="Event"):
        evento = brain.getObject()

        logger.info(f"{colors.DARKCYAN} Event: {evento.absolute_url()} {colors.ENDC}")
        if "multimedia" in evento.keys():
            renamed_event = api.content.rename(evento["multimedia"], new_id="immagini")
            renamed_event.title = "Immagini"
            renamed_event.reindexObject(idxs=["id", "title"])
            logger.info(f"{colors.GREEN} Rename multimedia {colors.ENDC}")

        if "video" not in evento.keys():
            galleria_video = api.content.create(
                container=evento,
                type="Document",
                title="Video",
                id="video",
            )
            create_default_blocks(context=galleria_video)

            # select  constraints
            constraintsGalleriaVideo = ISelectableConstrainTypes(galleria_video)
            constraintsGalleriaVideo.setConstrainTypesMode(1)
            constraintsGalleriaVideo.setLocallyAllowedTypes(("Link",))

            with api.env.adopt_roles(["Reviewer"]):
                api.content.transition(obj=galleria_video, transition="publish")

            logger.info(f"{colors.GREEN} Create video {colors.ENDC}")


def to_7009(context):
    portal_types = api.portal.get_tool(name="portal_types")
    behaviors = list(portal_types["Venue"].behaviors)
    if "plone.excludefromnavigation" in behaviors:
        return
    logger.info("Enable plone.excludefromnavigation behavior")
    behaviors.append("plone.excludefromnavigation")
    portal_types["Venue"].behaviors = tuple(behaviors)
    logger.info("Reindex Venue objects")
    brains = api.content.find(portal_type="Venue")
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        venue = brain.getObject()
        if not getattr(venue, "exclude_from_nav", None):
            setattr(venue, "exclude_from_nav", False)
            venue.reindexObject(idxs=["exclude_from_nav"])


def to_7010(context):
    registry = getUtility(IRegistry)
    prefix = "Products.CMFPlone.interfaces.syndication.ISiteSyndicationSettings"

    # get the old values
    old_attributes = [
        attribute for attribute in registry.records if attribute.startswith(prefix)
    ]
    if not old_attributes:
        logger.info(
            f"{colors.GREEN} We already have the correct interface. Nothing to do here! {colors.ENDC}"  # noqa
        )
        return
    old_values = {
        attribute.split(".")[-1]: registry.records[attribute].value
        for attribute in old_attributes
    }
    logger.info(
        f"{colors.DARKCYAN} Deleting old ISiteSyndicationSettings Records {colors.ENDC}"
    )
    # delete the old records
    for attribute in old_attributes:
        del registry.records[attribute]

    # import the new interface
    logger.info(f"{colors.DARKCYAN} Setup new interface in the registry {colors.ENDC}")
    context.runImportStepFromProfile(
        "profile-design.plone.contenttypes:fix_syndication",
        "plone.app.registry",
        False,
    )
    logger.info(
        f"{colors.DARKCYAN} Set the old values into the new registry records{colors.ENDC}"  # noqa
    )
    # set the old values into the new records
    default_values = {
        "allowed": True,
        "allowed_feed_types": (
            "RSS|RSS 1.0",
            "rss.xml|RSS 2.0",
            "atom.xml|Atom",
            "itunes.xml|iTunes",
        ),
        "default_enabled": False,
        "max_items": 15,
        "render_body": False,
        "search_rss_enabled": True,
        "show_author_info": True,
        "show_syndication_button": False,
        "show_syndication_link": False,
        "site_rss_items": tuple(),
    }

    for attribute in old_values:
        # we could have None value and we can't set None with set_registry_record
        # so we can set the value to the default.
        if old_values[attribute] == None:  # noqa
            old_values[attribute] = default_values[attribute]
            logger.info(
                f"{colors.RED } Fix {attribute} to default: {old_values[attribute]} {colors.ENDC}"  # noqa
            )

        if attribute == "site_rss_items" and old_values[attribute]:
            logger.info(
                f"{colors.RED} Please manually fix {attribute} with old value"
                f" {old_values[attribute]} {colors.ENDC}"
            )
            continue

        logger.info(
            f"{colors.DARKCYAN} Set {attribute} to  {old_values[attribute]} {colors.ENDC}"  # noqa
        )
        api.portal.set_registry_record(
            name=attribute,
            value=old_values[attribute],
            interface=ISiteSyndicationSettings,
        )
    logger.info(
        f"{colors.GREEN}ISiteSyndicationSettings interface fixed! {colors.ENDC}"
    )


def to_7011(context):
    logger.info("Reindex Event and News to fix SearchableText indexing issue")

    brains = api.content.find(portal_type=["Event", "News Item"])
    tot = len(brains)
    logger.info("Found {} documents.".format(tot))
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        doc = brain.getObject()
        doc.reindexObject(idxs=["SearchableText"])
    logger.info("Ends of reindex")


def to_7012(context):
    def has_empty_prezzo(value):
        if not value:
            return True
        if value == {"blocks": {}, "blocks_layout": {"items": []}}:
            return True
        blocks_layout = value.get("blocks_layout", {}).get("items", [])
        blocks = list(value.get("blocks", {}).values())
        if len(blocks_layout) == 1 and blocks[0] == {"@type": "text"}:
            return True
        return False

    logger.info("Set default value in prezzo field because now is required.")

    brains = api.content.find(portal_type=["Event"])
    tot = len(brains)
    logger.info(f"Found {tot} Events.")
    i = 0
    fixed = []
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        event = brain.getObject()
        prezzo = getattr(event, "prezzo", None)
        if has_empty_prezzo(value=prezzo):
            fixed.append(brain.getPath())
            uid = str(uuid4())
            event.prezzo = {
                "blocks": {
                    uid: {
                        "@type": "text",
                        "text": {
                            "blocks": [
                                {
                                    "key": "fvsj1",
                                    "text": "Eventuali costi sono indicati nella descrizione dell’evento.",
                                    "type": "unstyled",
                                    "depth": 0,
                                    "inlineStyleRanges": [],
                                    "entityRanges": [],
                                    "data": {},
                                }
                            ],
                            "entityMap": {},
                        },
                    }
                },
                "blocks_layout": {"items": [uid]},
            }
    logger.info(f"Fixed {len(fixed)} Events.")


def update_pdc_with_pdc_desc(context):
    brains = api.content.find(portal_type="PuntoDiContatto")
    logger.info(f"Found {len(brains)} PuntoDiContatto content type")
    for brain in brains:
        pdc = brain.getObject()
        value_punto_contatto = getattr(pdc, "value_punto_contatto", [])
        if value_punto_contatto:
            for v in value_punto_contatto:
                if not v.get("pdc_desc", None):
                    v["pdc_desc"] = None
                    logger.info(f"Set pdc_desc for {pdc.absolute_url()}")

            pdc.value_punto_contatto = value_punto_contatto
    logger.info("Ends of update")


def add_canale_digitale_link_index(context):
    update_catalog(context)
    update_registry(context)
    brains = api.content.find(portal_type="Servizio")
    logger.info(f"Found {len(brains)} Servizio content type to reindex")
    for brain in brains:
        service = brain.getObject()
        service.reindexObject(idxs=["canale_digitale_link"])
        logger.info(f"Reindexed {service.absolute_url()}")
    logger.info("End of update, added index canale_digitale_link")


def to_7031(context):
    portal_types = api.portal.get_tool(name="portal_types")
    for ptype in ["News Item"]:
        portal_types[ptype].default_view = "view"
        portal_types[ptype].view_methods = ["view"]


def to_7100(context):
    installOrReinstallProduct(api.portal.get(), "collective.volto.enhancedlinks")
    # add behavior to modulo
    portal_types = api.portal.get_tool(name="portal_types")
    modulo_behaviors = [x for x in portal_types["Modulo"].behaviors]
    if "volto.enhanced_links_enabled" not in modulo_behaviors:
        modulo_behaviors.append("volto.enhanced_links_enabled")
    portal_types["Modulo"].behaviors = tuple(modulo_behaviors)

    # update index/metadata
    brains = api.content.find(portal_type=["File", "Image", "Modulo"])
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        brain.getObject().reindexObject(idxs=["enhanced_links_enabled"])


def to_7200(context):
    update_catalog(context)
    # add behavior to Document and Folder
    bhv = "design.plone.contenttypes.behavior.exclude_from_search"
    portal_types = api.portal.get_tool(name="portal_types")
    for ptype in ["Document", "Folder"]:
        behaviors = [x for x in portal_types[ptype].behaviors]
        if bhv not in behaviors:
            behaviors.append(bhv)
        portal_types[ptype].behaviors = tuple(behaviors)

    # set True to all of already created children
    # update index/metadata
    brains = api.content.find(portal_type=[x for x in SUBFOLDERS_MAPPING.keys()])
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        container = brain.getObject()
        mappings = SUBFOLDERS_MAPPING.get(container.portal_type, [])
        persona_old_mapping = [
            {
                "id": "foto-e-attivita-politica",
            },
            {"id": "curriculum-vitae"},
            {"id": "compensi"},
            {
                "id": "importi-di-viaggio-e-o-servizi",
            },
            {
                "id": "situazione-patrimoniale",
            },
            {
                "id": "dichiarazione-dei-redditi",
            },
            {
                "id": "spese-elettorali",
            },
            {
                "id": "variazione-situazione-patrimoniale",
            },
            {
                "id": "altre-cariche",
            },
        ]
        if container.portal_type == "Persona":
            # cleanup also some old-style (v2) folders
            mappings.extend(persona_old_mapping)

        for mapping in mappings:
            child = container.get(mapping["id"], None)
            if not child:
                continue
            if child.portal_type not in ["Folder", "Document"]:
                continue
            child.exclude_from_search = True

    catalog = api.portal.get_tool(name="portal_catalog")
    catalog.manage_reindexIndex(ids=["exclude_from_search"])
