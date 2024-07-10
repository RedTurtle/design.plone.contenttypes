# -*- coding: utf-8 -*-
from .upgrades import colors
from .upgrades import logger
from .upgrades import update_catalog
from .upgrades import update_registry
from .upgrades import update_rolemap
from .upgrades import update_types
from Acquisition import aq_base
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.base.utils import get_installer
from plone.namedfile.file import NamedBlobFile
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFPlone.utils import safe_hasattr
from zope.component import getUtilitiesFor


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
    """TODO: documentare
    -> to 7001
    """
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
    """TODO: documentare"""
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
            wftool.doActionFor(incarico["importi-di-viaggio-e-o-servizi"], "publish")
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

        logger.info(f"{colors.GREEN} Creato incarico per {persona.title}{colors.ENDC}")

    logger.info(
        f"{colors.DARKCYAN} Finito di creare gli incarichi delle persone{colors.ENDC}"
    )


def create_pdc(context):
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
