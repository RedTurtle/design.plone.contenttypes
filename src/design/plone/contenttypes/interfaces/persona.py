# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.dexterity import textindexer
from plone.namedfile import field
from plone.supermodel import model


# TODO: migration script for these commented fields towards PDC
# telefono
# fax
# email
# TODO: migration script for these commented fields towards Incarico
# atto_nomina
# data_conclusione_incarico
# data_insediamento


class IPersona(model.Schema, IDesignPloneContentType):
    """Marker interface for contenttype Persona"""

    foto_persona = field.NamedImage(
        title=_("foto_persona_label", default="Foto della persona"),
        required=False,
        description=_(
            "foto_persona_help",
            default="Foto da mostrare della persona. "
            "La dimensione suggerita è 100x180px.",
        ),
    )

    competenze = BlocksField(
        title=_("competenze_label", default="Competenze"),
        description=_(
            "competenze_help",
            default="Descrizione del ruolo e dei compiti della persona.",
        ),
        required=False,
    )
    deleghe = BlocksField(
        title=_("deleghe_label", default="Deleghe"),
        description=_(
            "deleghe_help",
            default="Elenco delle deleghe a capo della persona.",
        ),
        required=False,
    )

    biografia = BlocksField(
        title=_("biografia_label", default="Biografia"),
        description=_(
            "biografia_help",
            default="Solo per persona politica: testo descrittivo che riporta"
            " la biografia della persona.",
        ),
        required=False,
    )

    # custom fieldsets
    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "competenze",
            "deleghe",
            "biografia",
        ],
    )

    # SearchableText fields
    textindexer.searchable("competenze")
    textindexer.searchable("deleghe")
    # TODO: migration script for these commented fields towards PDC
    # textindexer.searchable("telefono")
    # textindexer.searchable("fax")
    # textindexer.searchable("email")
