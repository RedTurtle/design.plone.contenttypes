# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.supermodel import model
from redturtle.bandi import bandiMessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from redturtle.bandi import bandiMessageFactory as _rtbando
from redturtle.bandi.interfaces.bandoSchema import IBandoSchema, getDefaultEnte
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form


class IBandoAgidSchema(IBandoSchema):
    """ A Dexterity schema for Annoucements """

    form.order_after(riferimenti_bando="IRichTextBehavior.text")
    riferimenti_bando = RichText(
        title=_(
            "riferimenti_bando_agid_label", default=u"Ulteriori informazioni"
        ),
        description=_(
            "riferimenti_bando_agid_help",
            default=u"Ulteriori informazioni non previste negli altri campi;"
            " si può trattare di contatti o note informative la cui conoscenza"
            " è indispensabile per la partecipazione al bando",
        ),
        required=False,
    )

    form.order_after(chiusura_procedimento_bando="IRichTextBehavior.text")
    chiusura_procedimento_bando = schema.Date(
        title=_rtbando(
            "chiusura_procedimento_bando_label",
            default=u"Closing date procedure",
        ),
        description=_rtbando("chiusura_procedimento_bando_help", default=u""),
        required=False,
    )

    form.order_after(scadenza_bando="IRichTextBehavior.text")
    scadenza_bando = schema.Datetime(
        title=_rtbando(
            "scadenza_bando_label", default=u"Expiration date and time"
        ),
        description=_rtbando(
            "scadenza_bando_help",
            default=u"Deadline to participate in the announcement",
        ),
        required=False,
    )

    form.order_after(scadenza_domande_bando="IRichTextBehavior.text")
    scadenza_domande_bando = schema.Datetime(
        title=_(
            "scadenza_domande_bando_label",
            default=u"Termine per le richieste di chiarimenti",
        ),
        description=_(
            "scadenza_domande_bando_help",
            default=u"Data entro la quale sarà possibile far pervenire domande"
            " e richieste di chiarimento a chi eroga il bando",
        ),
        required=False,
    )

    form.order_after(ente_bando="IRichTextBehavior.text")
    directives.widget(
        "ente_bando",
        AjaxSelectFieldWidget,
        vocabulary="redturtle.bandi.enti.vocabulary",
    )
    ente_bando = schema.Tuple(
        title=_rtbando(u"ente_label", default=u"Authority"),
        description=_rtbando(
            u"ente_help", default=u"Select some authorities."
        ),
        required=False,
        defaultFactory=getDefaultEnte,
        value_type=schema.TextLine(),
        missing_value=None,
    )

    form.order_after(destinatari="IRichTextBehavior.text")
    directives.widget(destinatari=CheckBoxFieldWidget)
    destinatari = schema.List(
        title=_rtbando("destinatari_label", default=u"Recipients"),
        description=_rtbando("destinatari_help", default=""),
        required=True,
        value_type=schema.Choice(
            vocabulary="redturtle.bandi.destinatari.vocabulary"
        ),
    )

    form.order_after(tipologia_bando="IRichTextBehavior.text")
    directives.widget(tipologia_bando=RadioFieldWidget)
    tipologia_bando = schema.Choice(
        title=_rtbando("tipologia_bando_label", default=u"Announcement type"),
        description=_rtbando("tipologia_bando_help", default=""),
        vocabulary="redturtle.bandi.tipologia.vocabulary",
        required=True,
    )

    ufficio_responsabile = RelationList(
        title=_(
            "ufficio_responsabile_label",
            default="Ufficio responsabile del documento",
        ),
        description=_(
            "ufficio_responsabile_help",
            default="Seleziona l'ufficio responsabile di questo documento.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    area_responsabile = RelationList(
        title=_(
            "area_responsabile_label",
            default="Area responsabile del documento",
        ),
        description=_(
            "area_responsabile_help",
            default="Seleziona l'area amministrativa responsabile del "
            "documento.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Area"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

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
