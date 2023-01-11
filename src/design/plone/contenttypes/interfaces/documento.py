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
            "identificativo_documento_label",
            default="Identificativo del documento.",
        ),
        description=_(
            "identificativo_documento_help",
            default="Un numero identificativo del documento.",
        ),
        required=False,
    )

    protocollo = schema.TextLine(
        title=_(
            "protocollo_documento_label",
            default="Numero di protocollo",
        ),
        description=_(
            "protocollo_documento_help",
            default="Il numero di protocollo del documento.",
        ),
        max_length=255,
        required=False,
    )
    data_protocollo = schema.Date(
        title=_("data_protocollo", default="Data del protocollo"),
        required=False,
    )
    # descrizione = BlocksField(
    #     title=_("descrizione_label", default="Descrizione"),
    #     description=_(
    #         "descrizione_help",
    #         default="L'oggetto del documento spiegato in modo semplice per il cittadino",  # noqa
    #     ),
    #     required=True,
    # )
    # url = schema.URI(
    #     title=_("url_documento_label", default="Link al documento"),
    #     description=_(
    #         "url_documento_help",
    #         default="Link al documento vero e proprio, in un formato scaricabile attraverso una URL.",  # noqa
    #     ),
    #     required=False,
    # )
    # file_correlato = field.NamedBlobFile(
    #     title=_("file_correlato_label", default="File correlato"),
    #     description=_(
    #         "file_correlato_help",
    #         default="Se non è presente un link ad una risorsa esterna, ricordarsi di caricare l'allegato vero e proprio",  # noqa
    #     ),
    #     required=False,
    # )
    ufficio_responsabile = RelationList(
        title=_(
            "ufficio_responsabile_documento_label",
            default="Ufficio responsabile del documento",
        ),
        description=_(
            "ufficio_responsabile_documento_help",
            default="Seleziona l'ufficio responsabile di questo documento.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Ufficio responsabile"),
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
            default="Seleziona l'area amministrativa responsabile del " "documento.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Area"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    autori = RelationList(
        title=_(
            "autori_label",
            default="Autore/i",
        ),
        description=_(
            "autori_help",
            default="Seleziona una lista di autori che hanno pubblicato "
            "il documento. Possono essere Persone o Unità Organizzative.",
        ),
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        default=[],
    )
    formati_disponibili = BlocksField(
        title=_("formati_disponibili_label", default="Formati disponibili"),
        description=_(
            "formati_disponibili_help",
            default="Lista dei formati in cui è disponibile il documento",
        ),
        required=True,
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
            "riferimenti_normativi_documento_label",
            default="Riferimenti normativi",
        ),
        description=_(
            "riferimenti_normativi_documento_help",
            default="Inserisici del testo di dettaglio per eventuali "
            "riferimenti normativi utili a questo documento.",
        ),
        required=False,
    )

    dataset = RelationList(
        title=_(
            "dataset_label",
            default="Dataset collegati",
        ),
        description=_(
            "dataset_collegati_help",
            default="Schede dataset collegate al documento",
        ),
        default=[],
        required=False,
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    # custom widgets
    form.widget(
        "dataset",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 10, "selectableTypes": ["Dataset"]},
    )

    # servizi = RelationList(
    #     title=_(
    #         "servizi_label",
    #         default="Servizi collegati",
    #     ),
    #     description=_(
    #         "servizi_help",
    #         default="Servizi collegati al documento",
    #     ),
    #     default=[],
    #     required=False,
    #     value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    # )

    # # custom widgets
    # form.widget(
    #     "servizi",
    #     RelatedItemsFieldWidget,
    #     vocabulary="plone.app.vocabularies.Catalog",
    #     pattern_options={"maximumSelectionSize": 20, "selectableTypes": ["Servizio"]},
    # )

    documenti_allegati = RelationList(
        title=_(
            "documenti_allegati_label",
            default="Documenti allegati",
        ),
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
        label=_("informazioni_label", default="Ulteriori informazioni"),
        fields=["riferimenti_normativi", "documenti_allegati"],
    )

    # custom order
    form.order_after(
        ufficio_responsabile="IDescrizioneEstesaDocumento.descrizione_estesa"
    )
    form.order_after(area_responsabile="ufficio_responsabile")
    form.order_after(autori="area_responsabile")
    form.order_after(
        licenza_distribuzione="IDescrizioneEstesaDocumento.descrizione_estesa"
    )
    form.order_after(
        riferimenti_normativi="IAdditionalHelpInfos.ulteriori_informazioni"
    )
    form.order_after(documenti_allegati="riferimenti_normativi")
