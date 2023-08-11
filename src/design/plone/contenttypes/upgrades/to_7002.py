# -*- coding: utf-8 -*-
from .upgrades import colors
from .upgrades import logger
from Acquisition import aq_base
from copy import deepcopy
from plone import api


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
