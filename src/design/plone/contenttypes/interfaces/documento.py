# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IDocumento(model.Schema, IDesignPloneContentType):
    """Marker interface for content type Documento"""

    identificativo = schema.TextLine(
        title=_(
            "identificativo_documento_label", default="Identificativo del documento.",
        ),
        description=_(
            "identificativo_documento_help",
            default="Un numero identificativo del documento.",
        ),
        required=False,
    )

    tipologia_documento = schema.Choice(
        title=_("tipologia_documento_label", default="Tipologia del documento"),
        description=_(
            "tipologia_documento_help", default="Seleziona la tipologia del documento.",
        ),
        required=True,
        vocabulary="design.plone.vocabularies.tipologie_documento",
    )

    ufficio_responsabile = RelationList(
        title=_(
            "ufficio_responsabile_documento_label",
            default="Ufficio responsabile del documento",
        ),
        description=_(
            "ufficio_responsabile_documento_help",
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
        title=_("area_responsabile_label", default="Area responsabile del documento",),
        description=_(
            "area_responsabile_help",
            default="Seleziona l'area amministrativa responsabile del " "documento.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Area"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    autori = RelationList(
        title=_("autori_label", default="Autore/i",),
        description=_(
            "autori_help",
            default="Seleziona una lista di autori che hanno pubblicato "
            "il documento. Possono essere Persone o Unità Organizzative.",
        ),
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        default=[],
    )

    licenza_distribuzione = schema.TextLine(
        title=_("licenza_distribuzione_label", default="Licenza di distribuzione"),
        description=_(
            "licenza_distribuzione_help",
            default="La licenza con il quale viene distribuito questo documento.",
        ),
        required=False,
    )

    riferimenti_normativi = BlocksField(
        title=_(
            "riferimenti_normativi_documento_label", default="Riferimenti normativi",
        ),
        description=_(
            "riferimenti_normativi_documento_help",
            default="Inserisici del testo di dettaglio per eventuali "
            "riferimenti normativi utili a questo documento.",
        ),
        required=False,
    )

    documenti_allegati = RelationList(
        title=_("documenti_allegati_label", default="Documenti allegati",),
        description=_(
            "documenti_allegati_help",
            default="Seleziona una serie di altri contenuti di tipo Documento "
            "che vanno allegati a questo.",
        ),
        default=[],
        required=False,
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    # custom widgets
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
        "autori",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona", "UnitaOrganizzativa"],
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
    form.widget(
        "documenti_allegati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 10, "selectableTypes": ["Documento"]},
    )

    #  custom fieldsets
    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default="Descrizione"),
        fields=[
            "ufficio_responsabile",
            "area_responsabile",
            "autori",
            "licenza_distribuzione",
        ],
    )

    model.fieldset(
        "informazioni",
        label=_("informazioni_label", default=u"Ulteriori informazioni"),
        fields=["riferimenti_normativi", "documenti_allegati"],
    )

    # custom order
    form.order_after(
        ufficio_responsabile="IDescrizioneEstesaDocumento.descrizione_estesa"
    )
    form.order_after(area_responsabile="ufficio_responsabile")
    form.order_after(autori="area_responsabile")
    form.order_after(licenza_distribuzione="autori")
    form.order_after(
        riferimenti_normativi="IAdditionalHelpInfos.ulteriori_informazioni"
    )
    form.order_after(documenti_allegati="riferimenti_normativi")
