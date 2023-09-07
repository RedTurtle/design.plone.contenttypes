# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes import AGID_VERSION
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


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

    # Questo campo per direttive e richieste viene nascosto nella form
    # Lo si tiene perche si vuole evitare di perder dati tra le migrazioni
    # e magari non poter piu' usare la feature collegata, ossia
    # la check persone, in quanto relazioni potrebbero rompersi o perdersi
    organizzazione_riferimento = RelationList(
        title=_(
            "organizzazione_riferimento_label",
            default="Organizzazione di riferimento",
        ),
        description=_(
            "organizzazione_riferimento_help",
            default="Seleziona una lista di organizzazioni a cui la persona"
            " appartiene.",
        ),
        value_type=RelationChoice(
            title=_("Organizzazione di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        default=[],
        required=False,
    )

    if AGID_VERSION == "V3":
        form.omitted("organizzazione_riferimento")

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

    # custom widgets
    form.widget(
        "organizzazione_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # custom fieldsets
    # TODO da verificare in base a v2/v3
    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "organizzazione_riferimento",
            "competenze",
            "deleghe",
            "biografia",
        ],
    )

    # SearchableText fields
    # TODO da verificare in base a v2/v3
    textindexer.searchable("competenze")
    textindexer.searchable("deleghe")
    # TODO: migration script for these commented fields towards PDC
    # textindexer.searchable("telefono")
    # textindexer.searchable("fax")
    # textindexer.searchable("email")
