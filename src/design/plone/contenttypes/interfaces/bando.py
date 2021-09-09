# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform import directives as form
from plone.supermodel import model
from redturtle.bandi import bandiMessageFactory as _
from redturtle.bandi import bandiMessageFactory as _rtbando
from redturtle.bandi.interfaces.bandoSchema import IBandoSchema, getDefaultEnte
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IBandoAgidSchema(IBandoSchema, IDesignPloneContentType):
    """ A Dexterity schema for Annoucements """

    # ridefinito, così usiamo il campo dei blocchi
    text = BlocksField(
        title=_("text_label", default="Testo"),
        description=_("text_help", default="",),
        required=False,
    )
    tipologia_bando = schema.Choice(
        title=_rtbando("tipologia_bando_label", default="Announcement type"),
        description=_rtbando("tipologia_bando_help", default=""),
        vocabulary="redturtle.bandi.tipologia.vocabulary",
        required=True,
    )
    destinatari = schema.List(
        title=_rtbando("destinatari_label", default="Recipients"),
        description=_rtbando("destinatari_help", default=""),
        required=False,
        value_type=schema.Choice(vocabulary="redturtle.bandi.destinatari.vocabulary"),
    )
    ente_bando = schema.Tuple(
        title=_rtbando("ente_label", default="Authority"),
        description=_rtbando("ente_help", default="Select some authorities."),
        required=False,
        defaultFactory=getDefaultEnte,
        value_type=schema.TextLine(),
        missing_value=None,
    )
    scadenza_domande_bando = schema.Datetime(
        title=_(
            "scadenza_domande_bando_label",
            default="Termine per le richieste di chiarimenti",
        ),
        description=_(
            "scadenza_domande_bando_help",
            default="Data entro la quale sarà possibile far pervenire domande"
            " e richieste di chiarimento a chi eroga il bando",
        ),
        required=False,
    )
    scadenza_bando = schema.Datetime(
        title=_rtbando("scadenza_bando_label", default="Expiration date and time"),
        description=_rtbando(
            "scadenza_bando_help",
            default="Deadline to participate in the announcement",
        ),
        required=False,
    )

    chiusura_procedimento_bando = schema.Date(
        title=_rtbando(
            "chiusura_procedimento_bando_label", default="Closing date procedure",
        ),
        description=_rtbando("chiusura_procedimento_bando_help", default=""),
        required=False,
    )

    riferimenti_bando = BlocksField(
        title=_("riferimenti_bando_agid_label", default="Ulteriori informazioni"),
        description=_(
            "riferimenti_bando_agid_help",
            default="Ulteriori informazioni non previste negli altri campi;"
            " si può trattare di contatti o note informative la cui conoscenza"
            " è indispensabile per la partecipazione al bando",
        ),
        required=False,
    )

    ufficio_responsabile = RelationList(
        title=_(
            "ufficio_responsabile_bando_label",
            default="Ufficio responsabile del bando",
        ),
        description=_(
            "ufficio_responsabile_bando_help",
            default="Seleziona l'ufficio responsabile di questo bando.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    area_responsabile = RelationList(
        title=_("area_responsabile_label", default="Area responsabile del documento",),
        description=_(
            "area_responsabile_help",
            default="Seleziona l'area amministrativa responsabile del " "documento.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Area"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    # widgets
    directives.widget(
        "ente_bando",
        AjaxSelectFieldWidget,
        vocabulary="redturtle.bandi.enti.vocabulary",
    )
    directives.widget(destinatari=CheckBoxFieldWidget)
    directives.widget(tipologia_bando=RadioFieldWidget)
    form.widget(
        "ufficio_responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "area_responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["area_responsabile", "ufficio_responsabile"],
    )
