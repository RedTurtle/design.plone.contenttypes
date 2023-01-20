# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.taxonomy.interfaces import ITaxonomy
from collective.volto.blocksfield.field import BlocksField
from copy import deepcopy
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.setuphandlers import remove_blocks_behavior
from design.plone.contenttypes.upgrades.draftjs_converter import to_draftjs
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.app.upgrade.utils import installOrReinstallProduct
from plone.base.utils import get_installer
from plone.dexterity.utils import iterSchemata
from plone.namedfile.file import NamedBlobFile
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFPlone.utils import safe_hasattr
from redturtle.bandi.interfaces.settings import IBandoSettings
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import getFields

import json
import logging
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
            # import pdb

            # pdb.set_trace()
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


def to_7001(context):

    installer = get_installer(context=api.portal.get())
    installer.install_product("eea.api.taxonomy")
    logger.info(
        f"{colors.DARKCYAN} eea.api.taxonomy and collective.taxonomy installed {colors.ENDC}"  # noqa
    )
    # delete actual index from portal_catalog
    for index in [
        "tipologia_notizia",
        "tipologia_documento",
        "tipologia_organizzazione",
    ]:
        api.portal.get_tool("portal_catalog").delIndex(index)

    context.runImportStepFromProfile(
        "design.plone.contenttypes:taxonomy", "collective.taxonomy"
    )
    for utility_name, utility in list(getUtilitiesFor(ITaxonomy)):
        utility.updateBehavior(**{"field_prefix": ""})
        logger.info(
            f"{colors.DARKCYAN} Change taxonomy prefix for {utility_name} {colors.ENDC}"  # noqa
        )
    logger.info(
        f"{colors.DARKCYAN} design.plone.contentypes taxonomies imported {colors.ENDC}"  # noqa
    )
    update_types(context)
    update_registry(context)
    update_catalog(context)
    update_rolemap(context)
    logger.info(
        f"{colors.DARKCYAN} Upgraded types, registry, catalog and rolemap {colors.ENDC}"  # noqa
    )


def create_incarichi_folder(context):
    logger.info(
        f"{colors.DARKCYAN} Inizio a creare la cartella Incarichi nelle persone {colors.ENDC}"  # noqa
    )
    pc = api.portal.get_tool(name="portal_catalog")
    wftool = api.portal.get_tool(name="portal_workflow")
    brains = pc({"portal_type": "Persona"})
    target = {"id": "incarichi", "title": "Incarichi", "contains": ("Incarico",)}
    for brain in brains:
        persona = brain.getObject()
        if target["id"] in persona:
            logger.info(
                f"{colors.YELLOW} {persona.title} contiene già la cartella incarichi {colors.ENDC}"  # noqa
            )
            continue
        suboject = api.content.create(
            type="Document", id=target["id"], title=target["title"], container=persona
        )
        subobjectConstraints = ISelectableConstrainTypes(suboject)
        subobjectConstraints.setConstrainTypesMode(1)
        subobjectConstraints.setLocallyAllowedTypes(target["contains"])

        if api.content.get_state(obj=persona) == "published":
            wftool.doActionFor(suboject, "publish")

        logger.info(
            f"{colors.GREEN} Creato la cartella incarichi per {persona.title}{colors.ENDC}"  # noqa
        )
    logger.info(
        f"{colors.DARKCYAN} Finito di creare la cartella Incarichi{colors.ENDC}"
    )


def create_incarico_for_persona(context):
    logger.info(
        f"{colors.DARKCYAN} Inizio a creare gli incarichi delle persone {colors.ENDC}"
    )
    # intids = getUtility(IIntIds)
    pc = api.portal.get_tool(name="portal_catalog")
    wftool = api.portal.get_tool(name="portal_workflow")
    brains = pc({"portal_type": "Persona"})
    MAPPING_TIPO = {
        "Amministrativa": "amministrativo",
        "Politica": "politico",
        "Altro tipo": "altro",
    }
    for brain in brains:

        persona = brain.getObject()

        incarichi_folder = persona["incarichi"]

        if incarichi_folder.values():
            logger.info(
                f"{colors.RED}{persona.title} ha già un incarico creato {colors.ENDC}"
            )  # noqa
            continue

        if safe_hasattr(persona, "ruolo"):
            incarico_title = persona.ruolo
        else:
            logger.info(
                f"{colors.RED} Attenzione: {persona.title} non ha un ruolo {colors.ENDC}"  # noqa
            )
            incarico_title = f"Incarico di {persona.title}"

        incarico = api.content.create(
            type="Incarico", title=incarico_title, container=incarichi_folder
        )
        # incarico.persona = [RelationValue(intids.getId(persona))]
        api.relation.create(source=incarico, target=persona, relationship="persona")
        if safe_hasattr(persona, "organizzazione_riferimento"):
            incarico.unita_organizzativa = persona.organizzazione_riferimento

        if safe_hasattr(persona, "data_insediamento"):
            incarico.data_inizio_incarico = persona.data_insediamento
            incarico.data_insediamento = persona.data_insediamento

        if safe_hasattr(persona, "data_conclusione_incarico"):
            incarico.data_conclusione_incarico = persona.data_conclusione_incarico

        atto_nomina = None
        if safe_hasattr(persona, "atto_nomina"):
            atto_nomina = api.content.create(
                type="Documento",
                id="atto-di-nomina",
                title="Atto di nomina",
                container=incarico,
            )
            atto_nomina.description = f"Atto di nomina di {persona.title} per il ruolo di {incarico_title}"  # noqa
            atto_nomina.file_correlato = NamedBlobFile(
                data=persona.atto_nomina.data,
                filename=persona.atto_nomina.filename,
                contentType="application/pdf",
            )
            atto_nomina.tipologia_documento = ["documento_attivita_politica"]
            # incarico.atto_nomina = [RelationValue(intids.getId(atto_nomina))]
            api.relation.create(
                source=incarico, target=atto_nomina, relationship="atto_nomina"
            )

        if safe_hasattr(persona, "tipologia_persona"):
            incarico.tipologia_incarico = MAPPING_TIPO[persona.tipologia_persona]

        # persona.incarichi_persona = [RelationValue(intids.getId(incarico))]
        api.relation.create(
            source=persona, target=incarico, relationship="incarichi_persona"
        )

        if api.content.get_state(obj=persona) == "published":
            wftool.doActionFor(incarico, "publish")
            wftool.doActionFor(incarico["compensi-file"], "publish")
            wftool.doActionFor(incarico["importi-di-viaggio-e-o-servizi"], "publish")
            if atto_nomina:
                wftool.doActionFor(atto_nomina, "publish")

        logger.info(f"{colors.GREEN} Creato incarico per {persona.title}{colors.ENDC}")

    logger.info(
        f"{colors.DARKCYAN} Finito di creare gli incarichi delle persone{colors.ENDC}"
    )


def create_pdc(context):
    portal_types = ["UnitaOrganizzativa", "Persona", "Event", "Venue"]
    MAPPINGS = {
        "Persona": {
            "telefono": "telefono",
            "fax": "fax",
            "email": "email",
            "pec": "pec",
        },
        "UnitaOrganizzativa": {
            "telefono": "telefono",
            "fax": "fax",
            "email": "email",
            "pec": "pec",
            "web": "url",
        },
        "Event": {
            "telefono": "telefono",
            "fax": "fax",
            "email": "email",
            "web": "url",
        },
        "Venue": {
            "telefono": "telefono",
            "fax": "fax",
            "email": "email",
            "pec": "pec",
            "web": "url",
        },
    }

    def migrated_contact_info(source):
        # we check if we have attribute, if it's a list and no more a json (block field)
        # finally we check if we have at least a value.
        if (
            safe_hasattr(source, "contact_info")
            and type(obj.contact_info) == list
            and len(obj.contact_info) > 0
        ):
            return True

    pc = api.portal.get_tool(name="portal_catalog")
    wftool = api.portal.get_tool(name="portal_workflow")
    portal = api.portal.get()
    punti_contatto_id = "punti-di-contatto"
    punti_contatto_title = "Punti di contatto"
    if "punti-di-contatto" not in portal:
        punti_contatto = api.content.create(
            type="Document",
            id=punti_contatto_id,
            title=punti_contatto_title,
            container=portal,
        )
        punti_contatto.exclude_from_nav = True
        punti_contatto.reindexObject()
        wftool.doActionFor(punti_contatto, "publish")
        logger.info(
            f"{colors.GREEN} Creato cartella punti di contatto nella radice del portal{colors.ENDC}"  # noqa
        )
    else:
        punti_contatto = portal[punti_contatto_id]

    for portal_type in portal_types:
        brains = pc(**{"portal_type": portal_type})
        logger.info(
            f"{colors.YELLOW} Stiamo per creare i PDC per {len(brains)} oggetti di tipo {portal_type}{colors.ENDC}"  # noqa
        )
        for brain in brains:
            obj = brain.getObject()
            mapping = MAPPINGS[portal_type]
            data = []
            for field in mapping:
                field_value = getattr(obj, field, None)
                if not field_value:
                    continue
                if type(field_value) != list:
                    # in some case we have a f*****g list
                    field_value = [
                        field_value,
                    ]
                for value in field_value:
                    data.append({"pdc_type": mapping[field], "pdc_value": value})

            if not data:
                continue

            if not migrated_contact_info(obj):
                obj.old_contact_info = obj.contact_info
                if obj.portal_type == "UnitaOrganizzativa":
                    del obj.contact_info
            else:
                logger.info(
                    f"{colors.RED} Esiste già un punto di contatto per {obj.title}({obj.absolute_url()}){colors.ENDC}"  # noqa
                )
                continue

            pdc = api.content.create(
                type="PuntoDiContatto",
                title=f"Punto di contatto per: {obj.title}",
                container=punti_contatto,
            )

            api.relation.create(source=obj, target=pdc, relationship="contact_info")

            pdc.value_punto_contatto = data
            # publish
            wftool.doActionFor(pdc, "publish")

            logger.info(
                f"{colors.GREEN} Creato il punto di contatto per {obj.title}({obj.absolute_url()}){colors.ENDC}"  # noqa
            )


TYPE_TO_TAXONOMIES_MAPPING = {
    "News Item": {
        "tipologia_notizia": {
            "it": {
                "Avviso": "avviso",
                "Comunicato stampa": "comunicato_stampa",
                "Novit\u00e0": "notizia",
            }
        }
    },
    "Documento": {
        "tipologia_documento": {
            "it": {
                "Accordi tra enti": "accordo_tra_enti",
                "Atti normativi": "atto_normativo",
                "Dataset": "Dataset",
                "Documenti (tecnici) di supporto": "documento_tecnico_di_supporto",
                "Documenti albo pretorio": "documenti_albo_pretorio",
                "Documenti attivit\u00e0 politica": "documento_attivita_politica",
                "Documenti funzionamento interno": "documento_funzionamento_interno",
                "Istanze": "istanza",
                "Modulistica": "modulistica",
            }
        }
    },
    "UnitaOrganizzativa": {
        "tipologia_organizzazione": {
            "it": {
                "Politica": "struttura_politica",
                "Amministrativa": "struttura_amministrativa",
                "Altro": "altra_struttura",
            }
        }
    },
}

TAXONOMIES_MAPPING = {}
for portal_type in TYPE_TO_TAXONOMIES_MAPPING:
    for TAXONOMY in TYPE_TO_TAXONOMIES_MAPPING[portal_type]:
        TAXONOMIES_MAPPING[TAXONOMY] = TYPE_TO_TAXONOMIES_MAPPING[portal_type][TAXONOMY]


def update_taxonomies(context):
    # delete actual index from portal_catalog
    logger.info(
        f"{colors.DARKCYAN} Migrazione delle tassonomie dai vecchi ai nuovi valori {colors.ENDC}"  # noqa
    )
    pc = api.portal.get_tool("portal_catalog")
    for portal_type in TYPE_TO_TAXONOMIES_MAPPING:
        brains = pc(**{"portal_type": portal_type})
        logger.info(
            f"{colors.DARKCYAN} Modifica delle tassonomie per {len(brains)} {portal_type}{colors.ENDC}"  # noqa
        )
        for brain in brains:
            obj = brain.getObject()
            obj_language = getattr(obj, "language", "it")
            for taxonomy in TYPE_TO_TAXONOMIES_MAPPING[portal_type]:
                old_value = getattr(obj, taxonomy)
                if (
                    old_value
                    and old_value
                    in TYPE_TO_TAXONOMIES_MAPPING[portal_type][taxonomy][obj_language]
                ):
                    new_value = TYPE_TO_TAXONOMIES_MAPPING[portal_type][taxonomy][
                        obj_language
                    ][old_value]
                    if taxonomy == "tipologia_documento":
                        new_value = [
                            new_value,
                        ]
                    setattr(obj, taxonomy, new_value)
                    logger.info(
                        f"{colors.GREEN} Modifica della tassonomia '{taxonomy}' di {obj.title} da {old_value} a {new_value}{colors.ENDC}"  # noqa
                    )

            obj.reindexObject()


def update_taxonomies_on_blocks(context):
    """
    Code from
    https://github.com/RedTurtle/design.plone.contenttypes/pull/139/files#diff-330d75e9be6e5193ab4622582fe7031d05094784e08aa3ada201a4e3d1642632R33
    """
    # https://www.comune.novellara.re.it/novita/notizie/archivio-notizie

    logger.info(
        f"{colors.DARKCYAN} Update dei blocchi listing basati sulle nuove tassonomie {colors.ENDC}"  # noqa
    )
    brains = api.portal.get_tool("portal_catalog")()
    for index, brain in list(enumerate(brains)):
        item = aq_base(brain.getObject())
        item_language = item.language or "it"
        if not index % 500:
            logger.info(
                f"{colors.DARKCYAN} ({index}/{len(brains)}) Proseguo l'analisi delle pagine {colors.ENDC}"  # noqa
            )
        if getattr(item, "blocks", {}):
            blocks = deepcopy(item.blocks)

            if blocks:
                for block in blocks.values():
                    if block.get("@type", "") == "listing":
                        for query in block.get("querystring", {}).get("query", []):

                            if query["i"] in [
                                "tipologia_notizia",
                                "tipologia_documento",
                                "tipologia_organizzazione",
                            ]:
                                new_values = []
                                for v in query["v"]:
                                    old_value = query["v"]
                                    if (
                                        v
                                        in TAXONOMIES_MAPPING[query["i"]][item_language]
                                    ):
                                        v = TAXONOMIES_MAPPING[query["i"]][
                                            item_language
                                        ][v]
                                    new_values.append(v)
                                query["v"] = new_values
                                logger.info(
                                    f"{colors.GREEN} Modifica della query per '{query['i']}' di {item.title} da {old_value} a {query['v']}{colors.ENDC}"  # noqa
                                )
                item.blocks = blocks
    logger.info(
        f"{colors.DARKCYAN} Terminato l'update dei blocchi {colors.ENDC}"  # noqa
    )


def update_uo_contact_info(context):
    brains = api.portal.get_tool("portal_catalog")(portal_type="UnitaOrganizzativa")
    logger.info(
        f"{colors.DARKCYAN} Inizio la pulzia delle {len(brains)} UO campo contact_info {colors.ENDC}"  # noqa
    )
    for brain in brains:
        obj = brain.getObject()
        if type(obj.contact_info) == dict:
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
