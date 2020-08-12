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
        title=_(u"immagine", default=u"Immagine"),
        required=False,
        description=_(
            u"foto_persona_help",
            default=u"Foto da mostrare della persona; la dimensione suggerita è 180x100 px",
        ),
    )

    ruolo = schema.TextLine(
        title=_(u"ruolo", default=u"Ruolo"),
        description=_(
            "ruolo_help", default="Descrizione testuale del ruolo di questa persona."
        ),
        required=True,
    )

    organizzazione_riferimento = RelationList(
        title=_(
            u"organizzazione_riferimento", default=u"Organizzazione di riferimento"
        ),
        description=_(
            "organizzazione_riferimento_help",
            default="Seleziona una lista di organizzazioni a cui la persona"
            " appartiene.",
        ),
        value_type=RelationChoice(
            title=_(u"Organizzazione di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        default=[],
        required=True,
    )
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

    responsabile_di = RelationList(
        title=_(u"responsabile_di", default=u"Responsabile di"),
        description=_(
            "responsabile_di_help",
            default="Seleziona una lista di organizzazioni di cui"
            " la persona è responsabile.",
        ),
        value_type=RelationChoice(
            title=_(u"Responsabile di"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
        default=[],
    )
    form.widget(
        "responsabile_di",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    data_insediamento = schema.Date(
        title=_(u"data_insediamento", default=u"Data insediamento"),
        description=_(
            "data_insediamento_help",
            default="Solo per persona politica: specificare la data di"
            " insediamento.",
        ),
        required=False,
    )

    data_conclusione_incarico = schema.Date(
        title=_(u"data_conclusione_incarico", default=u"Data conclusione incarico"),
        description=_(
            "data_conclusione_incarico_help",
            default="Data di conclusione dell'incarico.",
        ),
        required=False,
    )

    collegamenti_organizzazione_l1 = RelationList(
        title=_(
            u"collegamenti_organizzazione_l1",
            default=u"Collegamenti all'organizzazione di I livello",
        ),
        description=_(
            "collegamenti_organizzazione_l1_help",
            default="Seleziona l'organizzazione a cui la persona è collegata."
            " Se si tratta di una persona politica, il collegamento è riferito"
            " a una struttura politica. Se si tratta di una persona"
            " amministrativa, il collegamento è riferito ad un'area"
            " amministrativa.",
        ),
        default=[],
        value_type=RelationChoice(
            title=_(u"Collegamenti organizzazione di I livello"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
    )
    form.widget(
        "collegamenti_organizzazione_l1",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    collegamenti_organizzazione_l2 = RelationList(
        title=_(
            u"collegamenti_organizzazione_l2",
            default=u"Collegamenti all'organizzazione di II livello",
        ),
        description=_(
            "collegamenti_organizzazione_l2_help",
            default="Seleziona gli assessorati di cui la persona si occupa, "
            " i gruppi politici, commissioni a cui appartiene, oppure gli"
            " uffici di cui si occupa o di cui è responsabile.",
        ),
        default=[],
        value_type=RelationChoice(
            title=_(u"Collegamenti organizzazione di II livello"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
    )
    form.widget(
        "collegamenti_organizzazione_l2",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    competenze = RichText(
        title=_(u"competenze", default=u"Competenze"),
        description=_(
            "competenze_help",
            default="Descrizione del ruolo e dei compiti della persona.",
        ),
        required=False,
    )

    deleghe = RichText(
        title=_(u"deleghe", default=u"Deleghe"),
        description=_(
            "deleghe_help", default="Elenco delle deleghe a capo della persona."
        ),
        required=False,
    )

    tipologia_persona = schema.Choice(
        title=_(u"tipologia_persona", default=u"Tipologia persona"),
        description=_(
            "tipologia_persona_help",
            default="Seleziona la tipologia di persona: politica,"
            " amministrativa o di altro tipo.",
        ),
        vocabulary="design.plone.contenttypes.TipologiaPersona",
        required=True,
    )

    biografia = RichText(
        title=_(u"biografia", default=u"Biografia"),
        description=_(
            "biografia_help",
            default="Solo per persona politica: testo descrittivo che riporta"
            " la biografia della persona.",
        ),
        required=False,
    )

    telefono = schema.TextLine(
        title=_(u"telefono", default=u"Numero di telefono"),
        description=_("telefono_help", default="Contatto telefonico della persona."),
        required=False,
    )

    email = schema.TextLine(
        title=_(u"email", default=u"Indirizzo email"),
        description=_("email_help", default="Contatto mail della persona."),
        required=False,
    )
    informazioni_di_contatto = RichText(
        title=_(u"informazioni_di_contatto", default=u"Informazioni di contatto"),
        description=_(
            "informazioni_di_contatto_help", default="Altre informazioni di contatto."
        ),
        required=False,
    )

    curriculum_vitae = field.NamedBlobFile(
        title=_(u"curriculum_vitae", default=u"Curriculum vitae"),
        required=False,
        description=_(
            "curriculum_vitae_help", default="Curriculum vitae della persona."
        ),
    )

    # compensi = field.NamedBlobFile(
    #     title=_(u"compensi", default=u"Compensi"), required=True,
    # )

    #    importi_viaggio_servizio = field.NamedBlobFile(
    #        title=_(
    #            u"importi_viaggio_servizio",
    #            default=u"Importi di viaggio e/o servizio",
    #        ),
    #        required=True,
    #    )

    atto_nomina = field.NamedFile(
        title=_(u"atto_nomina", default=u"Atto nomina"),
        required=False,
        description=_("atto_nomina_help", default="Atto di nomina della persona."),
    )

    #    situazione_patrimoniale = field.NamedFile(
    #        title=_(
    #            u"situazione_patrimoniale", default=u"Situazione patrimoniale"
    #        ),
    #        required=False,
    #    )

    #    dichiarazione_redditi = field.NamedFile(
    #        title=_(
    #            u"dichiarazione_redditi", default=u"Dichiarazione dei redditi"
    #        ),
    #        required=True,
    #    )
    #
    #    spese_elettorali = field.NamedFile(
    #        title=_(u"spese_elettorali", default=u"Spese elettorali"),
    #        required=True,
    #    )
    #
    #    variazioni_situazione_patrimoniale = field.NamedFile(
    #        title=_(
    #            u"variazioni_situazione_patrimoniale",
    #            default=u"Variazioni situazione patrimoniale",
    #        ),
    #        required=True,
    #    )

    # SearchableText fields
    dexteritytextindexer.searchable("ruolo")
    dexteritytextindexer.searchable("competenze")
    dexteritytextindexer.searchable("deleghe")
    dexteritytextindexer.searchable("tipologia_persona")
    dexteritytextindexer.searchable("telefono")
    dexteritytextindexer.searchable("email")
    dexteritytextindexer.searchable("informazioni_di_contatto")
