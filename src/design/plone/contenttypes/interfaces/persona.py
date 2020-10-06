# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IPersona(model.Schema):
    """ Marker interface for contenttype Persona
    """

    foto_persona = field.NamedImage(
        title=_("foto_persona_label", default="Foto della persona"),
        required=False,
        description=_(
            "foto_persona_help",
            default="Foto da mostrare della persona. "
            "La dimensione suggerita è 180x100 px.",
        ),
    )
    ruolo = schema.TextLine(
        title=_("ruolo", default="Ruolo"),
        description=_(
            "ruolo_help",
            default="Descrizione testuale del ruolo di questa persona.",
        ),
        required=True,
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
        required=True,
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

    competenze = RichText(
        title=_("competenze_label", default="Competenze"),
        description=_(
            "competenze_help",
            default="Descrizione del ruolo e dei compiti della persona.",
        ),
        required=False,
    )
    deleghe = RichText(
        title=_("deleghe_label", default="Deleghe"),
        description=_(
            "deleghe_help",
            default="Elenco delle deleghe a capo della persona.",
        ),
        required=False,
    )

    tipologia_persona = schema.Choice(
        title=_("tipologia_persona_label", default="Tipologia persona"),
        description=_(
            "tipologia_persona_help",
            default="Seleziona la tipologia di persona: politica,"
            " amministrativa o di altro tipo.",
        ),
        vocabulary="design.plone.contenttypes.TipologiaPersona",
        required=True,
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

    biografia = RichText(
        title=_("biografia_label", default="Biografia"),
        description=_(
            "biografia_help",
            default="Solo per persona politica: testo descrittivo che riporta"
            " la biografia della persona.",
        ),
        required=False,
    )

    telefono = schema.TextLine(
        title=_("telefono_persona_label", default="Numero di telefono"),
        description=_(
            "telefono_persona_help",
            default="Contatto telefonico della persona.",
        ),
        required=False,
    )

    email = schema.TextLine(
        title=_("email_persona_label", default="Indirizzo email"),
        description=_(
            "email_persona_help", default="Contatto mail della persona."
        ),
        required=False,
    )
    curriculum_vitae = field.NamedBlobFile(
        title=_("curriculum_vitae_label", default="Curriculum vitae"),
        required=False,
        description=_(
            "curriculum_vitae_help",
            default="Allega un file contenente il "
            "curriculum vitae della persona.",
        ),
    )
    compensi = field.NamedBlobFile(
        title=_("compensi_label", default="Compensi"),
        description=_(
            "compensi_help",
            default="Allega un file contenente la lista dei compensi di "
            "qualsiasi natura connessi all'assunzione della carica. Solo per "
            "persona politica.",
        ),
        required=False,
    )

    importi_viaggio_servizio = field.NamedBlobFile(
        title=_(
            "importi_viaggio_servizio_label",
            default="Importi di viaggio e/o servizio",
        ),
        description=_(
            "importi_viaggio_servizio_help",
            default="Allega un file contenente la lista degli importi di "
            "viaggio di servizio e missioni pagati con fondi pubblici. "
            "Solo per persona politica.",
        ),
        required=False,
    )
    altre_cariche = field.NamedBlobFile(
        title=_("altre_cariche_label", default="Altre cariche"),
        description=_(
            "altre_cariche_help",
            default="Allega un file contenente i dati relativi all'assunzione"
            " di altre cariche, presso enti pubblici o privati, e relativi "
            "compensi a qualsiasi titolo corrisposti. "
            "Solo per persona politica.",
        ),
        required=False,
    )
    informazioni_di_contatto = RichText(
        title=_(
            "informazioni_di_contatto_label",
            default="Informazioni di contatto",
        ),
        description=_(
            "informazioni_di_contatto_help",
            default="Altre informazioni di contatto.",
        ),
        required=False,
    )

    atto_nomina = field.NamedFile(
        title=_("atto_nomina_label", default="Atto di nomina"),
        required=False,
        description=_(
            "atto_nomina_help",
            default="Inserire un file contenente l'atto di nomina della"
            " persona.",
        ),
    )
    situazione_patrimoniale = field.NamedFile(
        title=_(
            "situazione_patrimoniale_label", default="Situazione patrimoniale"
        ),
        required=False,
        description=_(
            "situazione_patrimoniale_help",
            default="Inserire un file contenente la situazione patrimoniale "
            "della persona. Solo per persona politica.",
        ),
    )
    dichiarazione_redditi = field.NamedFile(
        title=_(
            "dichiarazione_redditi_label", default="Dichiarazione dei redditi"
        ),
        required=False,
        description=_(
            "dichiarazione_redditi_help",
            default="Inserire un file contenente la copia dell'ultima "
            "dichiarazione dei redditi. Solo per persona politica.",
        ),
    )
    spese_elettorali = field.NamedFile(
        title=_("spese_elettorali_label", default="Spese elettorali"),
        required=False,
        description=_(
            "spese_elettorali_help",
            default="Inserire un file contenente la dichiarazione concernente"
            " le spese sostenute e le obbligazioni assunte per la propaganda "
            "elettorale. Solo per persona politica.",
        ),
    )
    variazioni_situazione_patrimoniale = field.NamedFile(
        title=_(
            "variazioni_situazione_patrimoniale_label",
            default="Variazioni situazione partimoniale",
        ),
        required=False,
        description=_(
            "variazioni_situazione_patrimoniale_help",
            default="Inserire un file contenente le variazioni della "
            "situazione patrimoniale intervenute nell'anno precedente e copia "
            "della dichiarazione dei redditi. Solo per persona politica.",
        ),
    )

    # custom widgets
    form.widget(
        "organizzazione_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
            "basePath": "/amministrazione",
        },
    )

    # custom fieldsets
    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "ruolo",
            "organizzazione_riferimento",
            "data_conclusione_incarico",
            "competenze",
            "deleghe",
            "tipologia_persona",
            "data_insediamento",
            "biografia",
        ],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["telefono", "email"],
    )
    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=[
            "curriculum_vitae",
            "compensi",
            "importi_viaggio_servizio",
            "altre_cariche",
            "informazioni_di_contatto",
            "atto_nomina",
            "situazione_patrimoniale",
            "dichiarazione_redditi",
            "spese_elettorali",
            "variazioni_situazione_patrimoniale",
        ],
    )
    # SearchableText fields
    dexteritytextindexer.searchable("ruolo")
    dexteritytextindexer.searchable("competenze")
    dexteritytextindexer.searchable("deleghe")
    dexteritytextindexer.searchable("tipologia_persona")
    dexteritytextindexer.searchable("telefono")
    dexteritytextindexer.searchable("email")
    dexteritytextindexer.searchable("informazioni_di_contatto")
