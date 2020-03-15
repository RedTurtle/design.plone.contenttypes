from plone.supermodel import model
from plone.app.textfield import RichText
from zope import schema
from plone.namedfile import field
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form

from design.plone.contenttypes import _


class IPersona(model.Schema):
    """ Marker interface for contenttype Persona
    """

    foto_persona = field.NamedImage(
        title=_(u"immagine", default=u"Immagine"), required=False,
    )

    ruolo = schema.TextLine(
        title=_(u"ruolo", default=u"Ruolo"), required=True,
    )

    ruolo = schema.TextLine(
        title=_(u"ruolo", default=u"Ruolo"), required=True,
    )

    organizzazione_riferimento = RelationList(
        title=_(
            u"organizzazione_riferimento",
            default=u"Organizzazione di riferimento",
        ),
        value_type=RelationChoice(
            title=_(u"Organizzazione di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
    )
    form.widget(
        "organizzazione_riferimento",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
            "basePath": "/amministrazione",
        },
    )

    responsabile_di = RelationList(
        title=_(u"responsabile_di", default=u"Responsabile di"),
        value_type=RelationChoice(
            title=_(u"Responsabile di"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        missing_value=(),
    )
    form.widget(
        "responsabile_di",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    data_conclusione_incarico = schema.Date(
        title=_(
            u"data_conclusione_incarico", default=u"Data conclusione incarico"
        ),
        required=False,
    )

    collegamenti_organizzazione_l1 = RelationList(
        title=_(
            u"collegamenti_organizzazione_l1",
            default=u"Collegamenti all'organizzazione di I livello",
        ),
        value_type=RelationChoice(
            title=_(u"Collegamenti organizzazione di I livello"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
    )
    form.widget(
        "collegamenti_organizzazione_l1",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    collegamenti_organizzazione_l2 = RelationList(
        title=_(
            u"collegamenti_organizzazione_l2",
            default=u"Collegamenti all'organizzazione di II livello",
        ),
        value_type=RelationChoice(
            title=_(u"Collegamenti organizzazione di II livello"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
    )
    form.widget(
        "collegamenti_organizzazione_l2",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    competenze = RichText(
        title=_(u"competenze", default=u"Competenze"), required=False,
    )

    deleghe = RichText(
        title=_(u"deleghe", default=u"Deleghe"), required=False,
    )

    tipologia_persona = schema.Choice(
        title=_(u"tipologia_persona", default=u"Tipologia persona"),
        vocabulary="design.plone.contenttypes.TipologiaPersona",
        required=True,
    )

    data_insediamento = schema.Date(
        title=_(u"data_insediamento", default=u"Data insediamento"),
        required=False,
    )

    biografia = RichText(
        title=_(u"biografia", default=u"Biografia"), required=False,
    )

    telefono = schema.TextLine(
        title=_(u"telefono", default=u"Numero di telefono"), required=False,
    )

    email = schema.TextLine(
        title=_(u"email", default=u"Indirizzo email"), required=False,
    )
    informazioni_di_contatto = RichText(
        title=_(
            u"informazioni_di_contatto", default=u"Informazioni di contatto"
        ),
        required=False,
    )

    curriculum_vitae = field.NamedBlobFile(
        title=_(u"curriculum_vitae", default=u"Curriculum vitae"),
        required=False,
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
        title=_(u"atto_nomina", default=u"Atto nomina"), required=False,
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

    ulteriori_informazioni = RichText(
        title=_(u"ulteriori_informazioni", default=u"Ulteriori informazioni"),
        required=False,
    )
