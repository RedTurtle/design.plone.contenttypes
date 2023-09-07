# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from collective.z3cform.datagridfield.row import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from design.plone.contenttypes import _
from plone.app.z3cform.widget import DateFieldWidget
from plone.app.z3cform.widget import LinkFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class ITempiEScadenzeValueSchema(model.Schema):
    """
    Row Schema
    """

    milestone = schema.TextLine(
        title=_("milestone_label", default="Titolo"),
        required=False,
        default="",
    )
    milestone_description = schema.TextLine(
        title=_("milestone_description_label", default="Sottotitolo"),
        required=False,
        default="",
    )
    interval_qt = schema.TextLine(
        title=_("interval_qt_label", default="Intervallo"),
        description=_(
            "interval_qt_help",
            default="Intervallo della fase (es. 1)",
        ),
        required=False,
        default="",
    )
    interval_type = schema.TextLine(
        title=_("interval_type_label", default="Tipo intervallo"),
        description=_(
            "interval_type_help",
            default="Ad esempio: " "ore, giorni, settimane, mesi.",
        ),
        required=False,
        default="",
    )
    data_scadenza = schema.Date(
        title=_("data_scadenza_label", default="Data scadenza"),
        required=False,
    )

    form.widget(
        "data_scadenza",
        DateFieldWidget,
    )


@provider(IFormFieldProvider)
class IServizioBehavior(model.Schema):
    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio e chi può usufruirne.",
        ),
    )
    come_si_fa = BlocksField(
        title=_("come_si_fa", default="Come fare"),
        required=True,
        description=_(
            "come_si_fa_help",
            default="Descrizione della procedura da seguire per poter"
            " usufruire del servizio.",
        ),
    )
    cosa_si_ottiene = BlocksField(
        title=_("cosa_si_ottiene", default="Cosa si ottiene"),
        description=_(
            "cosa_si_ottiene_help",
            default="Indicare cosa si può ottenere dal servizio, ad esempio"
            " 'carta di identità elettronica', 'certificato di residenza'.",
        ),
        required=True,
    )

    canale_digitale_link = schema.TextLine(
        title=_("canale_digitale_link", default="Link al canale digitale"),
        description=_(
            "canale_digitale_link_help",
            default="Collegamento con l'eventuale canale digitale di"
            " attivazione del servizio.",
        ),
        required=False,
    )
    # vocabolario dalle unita' organizzative presenti a catalogo?
    canale_fisico = RelationList(
        title=_("canale_fisico", default="Canale fisico"),
        description=_(
            "canale_fisico_help",
            default="Unità organizzative per la fruizione del servizio",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Canale fisico"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    tempi_e_scadenze = BlocksField(
        title=_("tempi_e_scadenze", default="Tempi e scadenze"),
        required=True,
        description=_(
            "tempi_e_scadenze_help",
            default="Descrivere le informazioni dettagliate riguardo eventuali tempi"
            " e scadenze di questo servizio.",
        ),
    )

    timeline_tempi_scadenze = schema.List(
        title=_("timeline_tempi_scadenze", default="Timeline tempi e scadenze"),
        default=[],
        value_type=DictRow(schema=ITempiEScadenzeValueSchema),
        description=_(
            "timeline_tempi_scadenze_help",
            default="Timeline tempi e scadenze del servizio: indicare per ogni "
            "scadenza un titolo descrittivo ed un eventuale sottotitolo. "
            "Per ogni scadenza, selezionare opzionalmente o l'intervallo (Campi"
            ' "Intervallo" e "Tipo Intervallo", es. "1" e "settimana"),'
            ' oppure direttamente una data di scadenza (campo: "Data Scadenza"'
            ", esempio 31/12/2023). "
            'Se vengono compilati entrambi, ha priorità il campo "Data Scadenza".',
        ),
        required=False,
    )

    form.order_before(condizioni_di_servizio="ILeadImageBehavior.image")
    form.order_before(a_chi_si_rivolge="chi_puo_presentare")
    form.order_before(come_si_fa="procedure_collegate")
    form.order_before(cosa_si_ottiene="procedure_collegate")
    form.order_after(canale_digitale_link="canale_digitale")
    form.order_after(canale_fisico="canale_digitale_link")

    # custom widgets
    condizioni_di_servizio = field.NamedBlobFile(
        title=_("condizioni_di_servizio", default="Condizioni di servizio"),
        required=False,
    )

    form.widget(
        "canale_fisico",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "timeline_tempi_scadenze",
        DataGridFieldFactory,
        frontendOptions={"widget": "data_grid"},
    )
    form.widget("canale_digitale_link", LinkFieldWidget)

    # custom fieldsets
    model.fieldset(
        "accedi_al_servizio",
        label=_("accedi_al_servizio_label", default="Accedere al servizio"),
        fields=[
            "come_si_fa",
            "cosa_si_ottiene",
            "canale_digitale_link",
            "canale_fisico",
        ],
    )

    model.fieldset(
        "tempi_e_scadenze",
        label=_("tempi_e_scadenze_label", default="Tempi e scadenze"),
        fields=["tempi_e_scadenze", "timeline_tempi_scadenze"],
    )

    model.fieldset(
        "a_chi_si_rivolge",
        label=_("a_chi_si_rivolge_label", default="A chi si rivolge"),
        fields=["a_chi_si_rivolge"],
    )


@implementer(IServizioBehavior)
@adapter(IDexterityContent)
class ServizioBehavior(object):
    """ """

    def __init__(self, context):
        self.context = context
