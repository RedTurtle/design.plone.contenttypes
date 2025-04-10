# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from design.plone.contenttypes.utils import create_default_blocks
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


SUBFOLDERS_MAPPING = {
    "Bando": {
        "content": [
            {"id": "documenti", "title": "Documenti", "type": "Bando Folder Deepening"},
            {
                "id": "comunicazioni",
                "title": "Comunicazioni",
                "type": "Bando Folder Deepening",
            },
            {"id": "esiti", "title": "Esiti", "type": "Bando Folder Deepening"},
        ],
    },
    "Documento": {
        "content": [
            {
                "id": "multimedia",
                "title": "Multimedia",
                "type": "Document",
                "allowed_types": ("Image",),
            },
        ],
    },
    "Event": {
        "content": [
            {
                "id": "immagini",
                "title": "Immagini",
                "allowed_types": ("Image", "Link"),
                "publish": True,
            },
            {
                "id": "video",
                "title": "Video",
                "allowed_types": ("Link",),
                "publish": True,
            },
            {
                "id": "sponsor_evento",
                "title": "Sponsor Evento",
                "allowed_types": ("Link",),
                "publish": True,
            },
            {
                "id": "documenti",
                "title": "Allegati",
                "allowed_types": ("File",),
                "publish": True,
            },
        ],
    },
    "Incarico": {
        "content": [
            {"id": "compensi-file", "title": "Compensi", "allowed": ("File",)},
            {
                "id": "importi-di-viaggio-e-o-servizi",
                "title": "Importi di viaggio e/o servizi",
                "allowed_types": ("File",),
            },
        ],
        "allowed_types": [],
    },
    "Venue": {
        "content": [
            {
                "id": "multimedia",
                "title": "Multimedia",
                "type": "Folder",
                "allowed_types": (
                    "Image",
                    "Link",
                ),
                "publish": True,
            }
        ],
    },
    "News Item": {
        "content": [
            {
                "id": "multimedia",
                "title": "Multimedia",
                "allowed_types": (
                    "Image",
                    "Link",
                ),
            },
            {
                "id": "documenti-allegati",
                "title": "Documenti allegati",
                "allowed_types": (
                    "File",
                    "Image",
                ),
            },
        ],
    },
    "ComunicatoStampa": {
        "content": [
            {
                "id": "multimedia",
                "title": "Multimedia",
                "allowed_types": (
                    "Image",
                    "Link",
                ),
            },
            {
                "id": "documenti-allegati",
                "title": "Documenti allegati",
                "allowed_types": (
                    "File",
                    "Image",
                ),
            },
        ]
    },
    "Persona": {
        "content": [
            {
                "id": "foto-e-attivita-politica",
                "title": "Foto e attività politica",
                "allowed_types": ("Image",),
            },
            {
                "id": "curriculum-vitae",
                "title": "Curriculum vitae",
                "allowed_types": ("File",),
            },
            {
                "id": "situazione-patrimoniale",
                "title": "Situazione patrimoniale",
                "allowed_types": ("File",),
            },
            {
                "id": "dichiarazione-dei-redditi",
                "title": "Dichiarazione dei redditi",
                "allowed_types": ("File",),
            },
            {
                "id": "spese-elettorali",
                "title": "Spese elettorali",
                "allowed_types": ("File",),
            },
            {
                "id": "variazione-situazione-patrimoniale",
                "title": "Variazione situazione patrimoniale",
                "allowed_types": ("File",),
            },
            {
                "id": "altre-cariche",
                "title": "Altre cariche",
                "allowed_types": ("File",),
            },
            {"id": "incarichi", "title": "Incarichi", "allowed_types": ("Incarico",)},
            {
                "id": "altri-documenti",
                "title": "Altri documenti",
                "allowed_types": ("File", "Image", "Link"),
            },
            {
                "id": "dichiarazione-insussistenza-cause-di-inconferibilita-e-incompatibilita",  # noqa
                "title": "Dichiarazione insussistenza cause di inconferibilità e"
                " incompatibilità",
                "allowed_types": ("File",),
            },
            {
                "id": "emolumenti-complessivi-percepiti-a-carico-della-finanza-pubblica",  # noqa
                "title": "Emolumenti complessivi percepiti a carico della finanza"
                " pubblica",
                "allowed_types": ("File",),
            },
        ],
        "allowed_types": [],
    },
    "Pratica": {
        "content": [
            {
                "id": "allegati",
                "title": "Allegati",
                "type": "Folder",
                "allowed_types": ("File",),
            }
        ],
    },
    "Servizio": {
        "content": [
            {
                "id": "modulistica",
                "title": "Modulistica",
                "allowed_types": ("Link",),
            },
            {"id": "allegati", "title": "Allegati", "allowed_types": ("File", "Link")},
        ],
    },
    "UnitaOrganizzativa": {
        "content": [
            {"id": "allegati", "title": "Allegati", "allowed_types": ("File",)},
        ],
    },
}


def onModify(context, event):
    for description in event.descriptions:
        if "IBasic.title" in getattr(
            description, "attributes", []
        ) or "IDublinCore.title" in getattr(description, "attributes", []):
            context_state = api.content.get_view(
                name="plone_context_state", context=context, request=context.REQUEST
            )
            if context_state.is_folderish():
                for child in context.listFolderContents():
                    child.reindexObject(idxs=["parent"])


def createStructure(context, subfolders_mapping):

    for mapping in subfolders_mapping.get("content", {}):
        if mapping["id"] not in context.keys():
            portal_type = mapping.get("type", "Document")
            child = api.content.create(
                container=context,
                type=portal_type,
                title=mapping["title"],
                id=mapping["id"],
            )
            if portal_type == "Document":
                create_default_blocks(context=child)

            if portal_type in ["Folder", "Document"]:
                child.exclude_from_search = True
                child.reindexObject(idxs=["exclude_from_search"])
            # select constraints
            if mapping.get("allowed_types", ()):
                constraints_child = ISelectableConstrainTypes(child)
                constraints_child.setConstrainTypesMode(1)
                constraints_child.setLocallyAllowedTypes(mapping["allowed_types"])

            if mapping.get("publish", False):
                with api.env.adopt_roles(["Reviewer"]):
                    api.content.transition(obj=child, transition="publish")

    allowed_types = subfolders_mapping.get("allowed_types", None)
    if allowed_types is not None and not isinstance(allowed_types, list):
        raise ValueError("Subfolder map is not well formed")

    if isinstance(allowed_types, list):
        constraints_context = ISelectableConstrainTypes(context)
        constraints_context.setConstrainTypesMode(1)
        constraints_context.setLocallyAllowedTypes(allowed_types)


def createSubfolders(context, event):
    """
    Create subfolders structure based on a portal_type mapping
    """
    if not IDesignPloneContenttypesLayer.providedBy(context.REQUEST):
        return

    subfolders_mapping = SUBFOLDERS_MAPPING.get(context.portal_type, [])
    if not subfolders_mapping:
        return
    createStructure(context, subfolders_mapping)
