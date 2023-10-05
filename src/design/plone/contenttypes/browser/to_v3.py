from Acquisition import aq_base
from collective.taxonomy.interfaces import ITaxonomy
from copy import deepcopy
from design.plone.contenttypes.upgrades.upgrades import update_catalog
from design.plone.contenttypes.upgrades.upgrades import update_registry
from design.plone.contenttypes.upgrades.upgrades import update_rolemap
from design.plone.contenttypes.upgrades.upgrades import update_types
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from plone.base.utils import get_installer
from plone.namedfile.file import NamedBlobFile
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFPlone.utils import safe_hasattr
from Products.Five import BrowserView
from z3c.relationfield import RelationValue
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import logging

logger = logging.getLogger(__name__)


class colors(object):
    GREEN = "\033[92m"
    ENDC = "\033[0m"
    RED = "\033[91m"
    DARKCYAN = "\033[36m"
    YELLOW = "\033[93m"


TYPE_TO_TAXONOMIES_MAPPING = {
    "News Item": {
        "tipologia_notizia": {
            "it": {
                "Avviso": "avviso",
                "Comunicato stampa": "comunicato_stampa",
                "Comunicato (stampa)": "comunicato_stampa",
                "Novit\u00e0": "notizia",
                "Notizia": "notizia",
            }
        }
    },
    "Documento": {
        "tipologia_documento": {
            "it": {
                "Accordi tra enti": "accordo_tra_enti",
                "Atti normativi": "atto_normativo",
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


class View(BrowserView):
    @property
    def setup_tool(self):
        return api.portal.get_tool("portal_setup")

    def __call__(self):
        update_types(self.setup_tool)
        update_registry(self.setup_tool)
        update_catalog(self.setup_tool)
        update_rolemap(self.setup_tool)

        logger.info(
            "Convert behavior: collective.dexteritytextindexer => plone.textindexer"
        )
        portal_types = api.portal.get_tool(name="portal_types")
        for fti in portal_types.values():
            behaviors = []
            for behavior in getattr(fti, "behaviors", ()):
                if behavior == "collective.dexteritytextindexer":
                    behavior = "plone.textindexer"
                behaviors.append(behavior)

            fti.behaviors = tuple(behaviors)

        self.migrate_pdc_and_incarico()

        # do to_7001 upgrade-steps
        self.to_7001()
        self.create_incarichi_folder()
        self.create_incarico_for_persona()
        self.create_pdc()

        # do to_7002 upgrade-steps
        self.update_taxonomies()
        self.update_taxonomies_on_blocks()

        self.update_uo_contact_info()
        self.readd_tassonomia_argomenti_uid()
        self.update_ruolo_indexing()
        self.fix_ctaxonomy_indexes_and_metadata()
        self.update_patrocinato_da()
        self.update_folder_for_gallery()

        api.portal.show_message(message="Sito aggiornato alla versione v3.")
        return self.request.response.redirect(api.portal.get().portal_url())

    def migrate_pdc_and_incarico(self):
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
        for pt in type_mapping:
            logger.info(
                "Migrating existing CTs for use with new Incarico and PDC Content Types"
            )
            self.createPDCandMigrateOldCTs(pt)
            self.createIncaricoAndMigratePersona(pt)

    def createIncaricoAndMigratePersona(self, portal_type):
        # Taxonomies work needs to be completed before, blind coding ahead
        if portal_type == "Persona":
            fixed_total = 0
            for brain in api.content.find(portal_type=portal_type):
                item = brain.getObject()
                atto_nomina = item.atto_nomina
                logger.info(f"Fixing Punto di Contatto for '{item.title}'...")
                file_bog = api.content.find(context=item, depth=1, id="atti-nomina")
                if not file_bog:
                    file_bog = api.content.create(
                        type="Document",
                        id="atti-nomina",
                        title="Atti Nomina",
                        container=item,
                    )
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
            logger.info("Updated {} objects".format(fixed_total))

    def createPDCandMigrateOldCTs(self, portal_type):
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

        logger.info(f"Fixing Punto di Contatto for '{portal_type}: DONE")
        logger.info("Updated {} objects".format(fixed_total))

    def to_7001(self):
        """
        old to_7001 upgrade-step
        """
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

        self.setup_tool.runImportStepFromProfile(
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
        logger.info(
            f"{colors.DARKCYAN} Upgraded types, registry, catalog and rolemap {colors.ENDC}"  # noqa
        )

    def create_incarichi_folder(self):
        """TODO: documentare
        -> to 7001
        """
        logger.info(
            f"{colors.DARKCYAN} Inizio a creare la cartella Incarichi nelle persone {colors.ENDC}"  # noqa
        )
        wftool = api.portal.get_tool(name="portal_workflow")
        brains = api.content.find(portal_type="Persona")
        target = {"id": "incarichi", "title": "Incarichi", "contains": ("Incarico",)}
        for brain in brains:
            persona = brain.getObject()
            if target["id"] in persona:
                logger.info(
                    f"{colors.YELLOW} {persona.title} contiene già la cartella incarichi {colors.ENDC}"  # noqa
                )
                continue
            suboject = api.content.create(
                type="Document",
                id=target["id"],
                title=target["title"],
                container=persona,
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

    def create_incarico_for_persona(self):
        """TODO: documentare"""
        logger.info(
            f"{colors.DARKCYAN} Inizio a creare gli incarichi delle persone {colors.ENDC}"
        )
        # intids = getUtility(IIntIds)
        wftool = api.portal.get_tool(name="portal_workflow")
        brains = api.content.find(portal_type="Persona")
        MAPPING_TIPO = {
            "Amministrativa": "amministrativo",
            "Politica": "politico",
            "Altro tipo": "altro",
            "politica": "politico",  # parma
            "amministrativa": "amministrativo",  # parma
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
                # we could have the attribute and then remove the value
                incarico_title = persona.ruolo or f"Incarico di {persona.title}"
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
            if safe_hasattr(persona, "atto_nomina") and getattr(persona, "atto_nomina"):
                atto_nomina = api.content.create(
                    type="Documento",
                    id="atto-di-nomina",
                    title="Atto di nomina",
                    container=incarico,
                )
                atto_nomina.description = f"Atto di nomina di {persona.title} per il ruolo di {incarico_title}"  # noqa
                # questo sotto rimane valido col vecchio schema del documento pubblico
                # atto_nomina.file_correlato = NamedBlobFile(
                #     data=persona.atto_nomina.data,
                #     filename=persona.atto_nomina.filename,
                #     contentType="application/pdf",
                # )
                # invece aggiungiamo un modulo sotto al documento
                modulo_atto_nomina = api.content.create(
                    type="Modulo",
                    id="atto-di-nomina",
                    title="Atto di nomina",
                    container=atto_nomina,
                )
                modulo_atto_nomina.file_principale = NamedBlobFile(
                    data=persona.atto_nomina.data,
                    filename=persona.atto_nomina.filename,
                    contentType="application/pdf",
                )

                atto_nomina.tipologia_documento = ["documento_attivita_politica"]
                # incarico.atto_nomina = [RelationValue(intids.getId(atto_nomina))]
                api.relation.create(
                    source=incarico, target=atto_nomina, relationship="atto_nomina"
                )
                logger.info(
                    f"{colors.GREEN} Creato atto nomina per {persona.title} {colors.ENDC}"
                )

            if safe_hasattr(persona, "tipologia_persona") and persona.tipologia_persona:
                incarico.tipologia_incarico = MAPPING_TIPO[persona.tipologia_persona]

            # persona.incarichi_persona = [RelationValue(intids.getId(incarico))]
            api.relation.create(
                source=persona, target=incarico, relationship="incarichi_persona"
            )

            if api.content.get_state(obj=persona) == "published":
                wftool.doActionFor(incarico, "publish")
                wftool.doActionFor(incarico["compensi-file"], "publish")
                wftool.doActionFor(
                    incarico["importi-di-viaggio-e-o-servizi"], "publish"
                )
                if atto_nomina:
                    wftool.doActionFor(atto_nomina, "publish")

            if safe_hasattr(persona, "compensi-file") and safe_hasattr(
                incarico, "compensi-file"
            ):
                compensi = getattr(persona, "compensi-file")
                for obj in compensi.contentItems():
                    api.content.move(source=obj, target=incarico["compensi-file"])

            if safe_hasattr(persona, "importi-di-viaggio-e-o-servizi") and safe_hasattr(
                incarico, "importi-di-viaggio-e-o-servizi"
            ):
                importi = getattr(persona, "importi-di-viaggio-e-o-servizi")
                for obj in importi.contentItems():
                    api.content.move(
                        source=obj, target=incarico["importi-di-viaggio-e-o-servizi"]
                    )

            logger.info(
                f"{colors.GREEN} Creato incarico per {persona.title}{colors.ENDC}"
            )

        logger.info(
            f"{colors.DARKCYAN} Finito di creare gli incarichi delle persone{colors.ENDC}"
        )

    def create_pdc(self):
        """TODO: documentare (pdc = "punto di contatto")"""
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
                and type(obj.contact_info) == list  # noqa
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
                    if type(field_value) != list:  # noqa
                        # in some case we have a f*****g list
                        field_value = [
                            field_value,
                        ]
                    for value in field_value:
                        data.append({"pdc_type": mapping[field], "pdc_value": value})

                if not data:
                    continue

                if not migrated_contact_info(obj):
                    if hasattr(aq_base(obj), "contact_info"):
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

    def update_taxonomies(self):
        """TODO: documentare"""
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
                obj_language = getattr(obj, "language", "it") or "it"
                for taxonomy in TYPE_TO_TAXONOMIES_MAPPING[portal_type]:
                    mapping = TYPE_TO_TAXONOMIES_MAPPING[portal_type][taxonomy][
                        obj_language
                    ]
                    old_value = getattr(aq_base(obj), taxonomy, None)
                    if type(old_value) == list:  # noqa
                        # this is a sort of race condition.
                        # we already have created ct Documento for attonomina
                        # in case we are using atto di nomina, skip
                        if obj.portal_type != "Documento":
                            raise Exception
                        if obj.id != "atto-di-nomina":
                            raise Exception
                        continue
                    else:
                        if old_value and old_value in mapping:
                            new_value = mapping[old_value]
                            if taxonomy == "tipologia_documento":
                                new_value = [new_value]
                            setattr(obj, taxonomy, new_value)
                            logger.info(
                                f"{colors.GREEN} Modifica della tassonomia '{taxonomy}' di {obj.title} da {old_value} a {new_value}{colors.ENDC}"  # noqa
                            )
                obj.reindexObject()

    def update_taxonomies_on_blocks(self):
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
                                            in TAXONOMIES_MAPPING[query["i"]][
                                                item_language
                                            ]
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

    def update_uo_contact_info(self):
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

    def reindex_catalog(self, idxs):
        pc = api.portal.get_tool(name="portal_catalog")
        brains = pc()
        for brain in brains:
            if idxs:
                brain.getObject().reindexObject(idxs=idxs)
            else:
                brain.getObject().reindexObject()

    def readd_tassonomia_argomenti_uid(self):
        logger.info(
            f"{colors.DARKCYAN} Aggiungo la tassonomia_argomenti_uid e reindicizzo{colors.ENDC}"  # noqa
        )
        idxs = ["tassonomia_argomenti_uid", "tassonomia_argomenti"]
        self.reindex_catalog(idxs)

    def update_ruolo_indexing(self):
        logger.info(
            f"{colors.DARKCYAN} Reindex del ruolo nelle persone {colors.ENDC}"  # noqa
        )
        idxs = ["ruolo"]
        pc = api.portal.get_tool("portal_catalog")
        brains = pc(portal_type="Persona")
        for brain in brains:
            persona = brain.getObject()
            persona.reindexObject(idxs=idxs)

    def fix_ctaxonomy_indexes_and_metadata(self):
        logger.info(f"{colors.DARKCYAN} Fix taxonomy indexes {colors.ENDC}")  # noqa
        bad_names = [
            "taxonomy_person_life_events",
            "taxonomy_business_events",
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

        self.setup_tool.runImportStepFromProfile(
            "design.plone.contenttypes:taxonomy", "collective.taxonomy"
        )
        brains = catalog(
            portal_type=[
                "News Item",
                "Event",
                "Venue",
                "Servizio",
                "Documento",
                "UnitaOrganizzativa",
                "Incarico",
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
                    "blocks_layout": {
                        "items": ["d252fe92-ce88-4866-b77d-501e7275cfc0"]
                    },
                },
            )
            obj.reindexObject()
        logger.info(f"{colors.DARKCYAN} End of update {colors.ENDC}")

    def update_folder_for_gallery(self):
        logger.info(f"{colors.DARKCYAN} Update events {colors.ENDC}")
        pc = api.portal.get_tool(name="portal_catalog")
        for brain in pc(portal_type="Event"):
            evento = brain.getObject()

            logger.info(
                f"{colors.DARKCYAN} Event: {evento.absolute_url()} {colors.ENDC}"
            )
            if "multimedia" in evento.keys():
                renamed_event = api.content.rename(
                    evento["multimedia"], new_id="immagini"
                )
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
