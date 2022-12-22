# -*- coding: utf-8 -*-
from plone.app.dexterity import textindexer
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IPersona(model.Schema, IDesignPloneContentType):
    """Marker interface for contenttype Persona"""

    foto_persona = field.NamedImage(
        title=_("foto_persona_label", default="Foto della persona"),
        required=False,
        description=_(
            "foto_persona_help",
            default="Foto da mostrare della persona. "
            "La dimensione suggerita è 180x100 px.",
        ),
    )

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

    data_conclusione_incarico = schema.Date(
        title=_(
            "data_conclusione_incarico_label",
            default="Data conclusione incarico",
        ),
        description=_(
            "data_conclusione_incarico_help",
            default="Data di conclusione dell'incarico.",
        ),
        required=False,
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

    data_insediamento = schema.Date(
        title=_("data_insediamento_label", default="Data insediamento"),
        description=_(
            "data_insediamento_help",
            default="Solo per persona politica: specificare la data di"
            " insediamento.",
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

    telefono = schema.List(
        title=_("telefono_persona_label", default="Numero di telefono"),
        description=_(
            "telefono_persona_help",
            default="Contatto telefonico della persona. E' possibile inserire "
            'più di un numero. Premendo "Invio" o "tab" si può passare al '
            "successivo da inserire.",
        ),
        value_type=schema.TextLine(),
        missing_value=[],
        default=[],
        required=False,
    )
    fax = schema.TextLine(
        title=_("fax_persona_label", default="Fax"),
        description=_("fax_persona_help", default="Indicare un numero di fax."),
        required=False,
    )
    email = schema.List(
        title=_("email_persona_label", default="Indirizzo email"),
        description=_(
            "email_persona_help",
            default="Contatto mail della persona. E' possibile inserire più"
            ' di un indirizzo. Premendo "Invio" o "tab" si può passare al '
            "successivo da inserire.",
        ),
        value_type=schema.TextLine(),
        missing_value=[],
        default=[],
        required=False,
    )
    curriculum_vitae = field.NamedBlobFile(
        title=_("curriculum_vitae_label", default="Curriculum vitae"),
        required=False,
        description=_(
            "curriculum_vitae_help",
            default="Allega un file contenente il curriculum vitae della persona. "
            "Se ha più file da allegare, utilizza questo campo per quello principale "
            'e gli altri mettili dentro alla cartella "Curriculum vitae" che troverai dentro alla Persona.',
        ),
    )

    atto_nomina = field.NamedFile(
        title=_("atto_nomina_label", default="Atto di nomina"),
        required=False,
        description=_(
            "atto_nomina_help",
            default="Inserire un file contenente l'atto di nomina della" " persona.",
        ),
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
    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "organizzazione_riferimento",
            "data_conclusione_incarico",
            "competenze",
            "deleghe",
            "data_insediamento",
            "biografia",
        ],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["telefono", "fax", "email"],
    )
    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=["curriculum_vitae", "atto_nomina"],
    )

    # SearchableText fields
    textindexer.searchable("competenze")
    textindexer.searchable("deleghe")
    textindexer.searchable("telefono")
    textindexer.searchable("fax")
    textindexer.searchable("email")
