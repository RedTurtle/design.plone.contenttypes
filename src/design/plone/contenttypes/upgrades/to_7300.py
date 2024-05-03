# -*- coding: utf-8 -*-
from .upgrades import logger
from Acquisition import aq_base
from plone import api
from plone.namedfile import file


def to_7300(context):
    mapping = {
        # portal_type
        "Documento Personale": {
            # field: "type"
            "immagine": "image",
            "pratica_associata": "file",
        },
        "Messaggio": {
            "documenti_allegati": "file",
        },
        "Persona": {
            "foto_persona": "image",
        },
        "RicevutaPagamento": {
            "stampa_ricevuta": "file",
            "pratica_associata": "file",
            "allegato": "file",
        },
    }

    mapping_types = {
        "image": (file.NamedImage, file.NamedBlobImage),
        "file": (file.NamedFile, file.NamedBlobFile),
    }

    for portal_type, fields in mapping.items():
        brains = api.content.find(unrestricted=True, portal_type=portal_type)
        logger.info("Updating fields for %s %s objects", portal_type, len(brains))
        for brain in brains:
            obj = aq_base(brain.getObject())
            for fieldname, _type in fields.items():
                value = getattr(obj, fieldname, None)
                # if value:
                #     import pdb; pdb.set_trace()
                if value and isinstance(value, mapping_types[_type][0]):
                    logger.info("Updated %s for %s", fieldname, brain.getPath())
                    setattr(
                        obj,
                        fieldname,
                        mapping_types[_type][1](
                            data=value.data,
                            contentType=value.contentType,
                            filename=value.filename,
                        ),
                    )
    logger.info("Finished updating fields")
