# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from collective.volto.blocksfield.field import BlocksField
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from plone.namedfile import field
from zope.component import adapter
from zope.interface import provider, implementer
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form


@provider(IFormFieldProvider)
class ITrasparenza(model.Schema):
    """
    Behavior conenene i campi per la sezione amministrazione trasparente
    """

    modalita_avvio = schema.TextLine(
        title=_(u"modalita_avvio_label", default=u"Modalita di avvio"),
        description=_(
            u"modalita_avvio_help",
            default=u"Indicare la modalità di avvio del procedimento.",
        ),
        required=False,
    )
    descrizione = BlocksField(
        title=_(
            u"descrizione_procedimento_label",
            default=u"Descrizione del procedimento",
        ),
        required=False,
        description=_(
            "descrizione_procedimento_help",
            default="Inserisci eventuale testo descrittivo del procedimento.",  # noqa
        ),
    )
    file_correlato = field.NamedBlobFile(
        title=_("file_correlato_label", default="File correlato"),
        description=_(
            "file_correlato_help",
            default="Inserisci il file correlato di questo pocedimento.",
        ),
        required=False,
    )

    soggetti_esterni = BlocksField(
        title=_(
            u"soggetti_eserni_label",
            default=u"Soggetti esterni, nonché, strutture interne coinvolte nel procedimento",
        ),
        required=False,
        description=_(
            "soggetti_eserni_help",
            default="Inserisci eventuali soggetti esterni, nonché, strutture interne coinvolte nel procedimento.",  # noqa
        ),
    )

    decorrenza_termine = BlocksField(
        title=_(
            u"decorrenza_termini_label",
            default=u"Decorrenza termine del procedimento",
        ),
        required=False,
        description=_(
            "decorrenza_termini_help",
            default="Inserisci la decorrenza termine del procedimento.",  # noqa
        ),
    )
    fine_termine = BlocksField(
        title=_(
            u"fine_termine_label", default=u"Fine termine del procedimento",
        ),
        required=False,
        description=_(
            "fine_termine_help",
            default="Inserisci la fine termine del procedimento.",  # noqa
        ),
    )
    tempo_medio = BlocksField(
        title=_(
            u"tempo_medio_label", default=u"Tempo medio del procedimento",
        ),
        required=False,
        description=_(
            "tempo_medio_help",
            default="Inserisci il tempo medio del procedimento.",  # noqa
        ),
    )
    silenzio_assenso = schema.Bool(
        title=_(
            u"silenzio_assenso_label",
            default=u"Silenzio assenso/Dichiarazione dell'interessato sostitutiva del provvedimento finale",  # noqa
        ),
        default=False,
        required=False,
        description=_(
            "silenzio_assenso_help",
            default="Indicare se il procedimento prevede il silenzio assenso o la dichiarazione dell'interessato sostitutiva del provvedimento finale.",  # noqa
        ),
    )
    provvedimento_finale = BlocksField(
        title=_(
            u"provvedimento_finale_label",
            default=u"Provvedimento del procedimento",
        ),
        required=False,
        description=_(
            "provvedimento_finale_help",
            default="Eventuale provvedimento finale del procedimento.",  # noqa
        ),
    )
    responsabile_procedimento = RelationList(
        title=_(
            "responsabile_procedimento",
            default=u"Responsabile del procedimento",
        ),
        description=_(
            "responsabile_procedimento_help",
            default="Indicare il responsabile del procedimento.",
        ),
        value_type=RelationChoice(
            title=_(u"Responsabile procedimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )
    dirigente = RelationList(
        title=_("dirigente", default=u"Dirigente",),
        description=_("dirigente_help", default="Indicare il dirigente.",),
        value_type=RelationChoice(
            title=_(u"Dirigente"), vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )
    organo_competente_provvedimento_finale = BlocksField(
        title=_(
            u"organo_competente_provvedimento_finale_label",
            default=u"Organo competente del provvedimento finale",
        ),
        required=False,
        description=_(
            "organo_competente_provvedimento_finale_help",
            default="Organo competente del provvedimento finale.",  # noqa
        ),
    )
    modalita_richiesta_informazioni = BlocksField(
        title=_(
            u"modalita_richiesta_informazioni_label",
            default=u"Modalità per richiedere informazioni",
        ),
        required=False,
        description=_(
            "modalita_richiesta_informazioni_help",
            default="Indicare le modalità per richiedere informazioni riguardo a questo procedimento.",  # noqa
        ),
    )
    procedura_online = schema.TextLine(
        title=_(
            u"procedura_online_label",
            default=u"Procedura informatizzata online",
        ),
        description=_(
            u"procedura_online_help",
            default=u"Indicare, se la procedura è informatizzata online, il riferimento.",  # noqa
        ),
        required=False,
    )
    altre_modalita_invio = BlocksField(
        title=_(
            u"altre_modalita_invio_label", default=u"Altre modalità di invio",
        ),
        description=_(
            u"altre_modalita_invio_help",
            default=u"Indicare, se esistono, altre modalità di invio.",  # noqa
        ),
        required=False,
    )
    atti_documenti_corredo = BlocksField(
        title=_(
            u"atti_documenti_corredo_label",
            default=u"Atti e documenti a corredo dell'istanza",
        ),
        description=_(
            u"atti_documenti_corredo_help",
            default=u"Indicare, se la esistono, atti e documenti a corredo dell'istanza.",  # noqa
        ),
        required=False,
    )
    reperimento_modulistica = BlocksField(
        title=_(
            u"reperimento_modulistica_label",
            default=u"Dove reperire la modulistica",
        ),
        description=_(
            u"reperimento_modulistica_help",
            default=u"Indicare dove è possibile reperre la modulistica per il procedimento.",  # noqa
        ),
        required=False,
    )
    pagamenti = BlocksField(
        title=_(u"pagamenti_label", default=u"Pagamenti previsti e modalità",),
        description=_(
            u"pagamenti_help",
            default=u"Indicare le informazioni riguardanti i pagamenti previsti e modalità di pagamento.",  # noqa
        ),
        required=False,
    )
    strumenti_tutela = BlocksField(
        title=_(u"strumenti_tutela_label", default=u"Strumenti di tutela"),
        description=_(
            u"strumenti_tutela_help",
            default=u"Indicare gli eventuali strumenti di tutela.",
        ),
        required=False,
    )
    # rt o collegamento a persona? esiste sempre?
    titolare_potere_sostitutivo = BlocksField(
        title=_(
            u"titolare_potere_sostitutivo_label",
            default=u"Titolare del potere sostitutivo",
        ),
        required=False,
        description=_(
            "titolare_potere_sostitutivo_help",
            default="Eventuale titolare del potere sostitutivo.",  # noqa
        ),
    )
    customer_satisfaction = BlocksField(
        title=_(
            u"customer_satisfaction_label",
            default=u"Risultati indagini di customer satisfaction",
        ),
        required=False,
        description=_(
            "customer_satisfaction_help",
            default="Risultati indagini di customer satisfaction.",  # noqa
        ),
    )
    riferimenti_normativi = BlocksField(
        title=_(
            u"riferimenti_normativi_label", default=u"Riferimenti normativi",
        ),
        required=False,
        description=_(
            "riferimenti_normativi_help",
            default="Indicare eventuali riferimenti normativi.",  # noqa
        ),
    )

    form.widget(
        "responsabile_procedimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
        },
    )
    form.widget(
        "dirigente",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
        },
    )

    model.fieldset(
        "trasparenza",
        label=_("trasparenza_fieldset_label", default=u"Trasparenza"),
        fields=[
            "modalita_avvio",
            "descrizione",
            "file_correlato",
            "soggetti_esterni",
            "decorrenza_termine",
            "fine_termine",
            "tempo_medio",
            "silenzio_assenso",
            "provvedimento_finale",
            "responsabile_procedimento",
            "dirigente",
            "organo_competente_provvedimento_finale",
            "modalita_richiesta_informazioni",
            "procedura_online",
            "altre_modalita_invio",
            "atti_documenti_corredo",
            "reperimento_modulistica",
            "pagamenti",
            "strumenti_tutela",
            "titolare_potere_sostitutivo",
            "customer_satisfaction",
            "riferimenti_normativi",
        ],
    )


@implementer(ITrasparenza)
@adapter(IDexterityContent)
class Trasparenza(object):
    """
    """

    def __init__(self, context):
        self.context = context
