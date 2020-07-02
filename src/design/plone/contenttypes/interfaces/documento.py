# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IDocumento(model.Schema):
    """Marker interface for content type Documento
    """

    identificativo = schema.TextLine(
        title=_(u"identificativo", default=u"Identificativo del documento"),
        required=True,
    )

    immagine = field.NamedBlobImage(
        title=_(u"immagine", default=u"Immagine"), required=False
    )

    # TODO: come gestire la tipologia del documento

    # TODO: come gestire la sottotipologia del documento

    descrizione_estesa = RichText(
        title=_(u"descrizione_estesa", default=u"Descrizione estesa"),
        required=False,
    )

    # vocabolario costruito da catalogo, prendendo le unita' organizzative
    ufficio_responsabile = RelationList(
        title=_(
            u"ufficio_responsabile",
            default=u"Ufficio responsabile del documento",
        ),
        required=True,
        value_type=RelationChoice(
            title=_(u"Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "ufficio_responsabile",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # area amministrativa non è un ct ma un' aggregazione di ct, come facciamo?
    area_responsabile = RelationList(
        title=_(
            u"area_responsabile", default=u"Area responsabile del documento"
        ),
        required=True,
        value_type=RelationChoice(
            title=_(u"Area responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "area_responsabile",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # chi sono effettivamente gli autori? Persone, uffici, servizi?
    # in ogni caso probabilmente da catalogo
    autori = RelationList(
        title=u"Autori",
        default=[],
        value_type=RelationChoice(
            title=_(u"Autore"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )
    form.widget(
        "autori",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona", "UnitaOrganizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    licenza_distribuzione = schema.TextLine(
        title=_(u"licenza_distribuzione", default=u"Licenza di distribuzione"),
        required=False,
    )

    # vocabolario da catalogo
    servizi_collegati = RelationList(
        title=u"Servizi collegati",
        default=[],
        value_type=RelationChoice(
            title=_(u"Servizio collegato"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "servizi_collegati",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Servizio"],
            # "basePath": "/servizi",
        },
    )

    canale_digitale_servizio_correlato = schema.TextLine(
        title=_(u"Canale digitale al servizio collegato"), required=False
    )

    # questo potrebbe essere qualcosa piu complicato di una semplice data
    data_inizio = schema.Date(
        title=_(u"data_inizio", default=u"Data di inizio"), required=False
    )

    # TODO: come ci gestiamo data e fasi intermedie?

    data_fine = schema.Date(
        title=_(u"data_fine", default=u"Data di scadenza"), required=False
    )  # le ho interpretate come relazioni uno a molti, quindi con schema.List?
    # vocabolario da catalogo
    dataset = RelationList(
        title=u"Dataset collegati",
        default=[],
        value_type=RelationChoice(
            title=_(u"Dataset"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )
    form.widget(
        "dataset",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Dataset"],
        },
    )

    # i riferimenti normativi li deve linkare chi si occupa di caricare e/o
    # fare la stesura del documento (secondo me)
    riferimenti_normativi = RichText(
        title=_(u"riferimenti_normativi", default=u"Riferimenti normativi"),
        required=False,
    )

    protocollo = schema.TextLine(
        title=_(u"protocollo", default=u"Protocollo"), required=True
    )

    data_protocollo = schema.Date(
        title=_(u"data_protocollo", default=u"Data del protocollo"),
        required=False,
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"), required=True
    )

    # come gestiamo "e' parte del life event"?
    # per ora gigavocabolario statico prendendo i valori da github e
    # accumunandoli in una mega lista
    life_event = schema.Choice(
        title=_(u"life_event", default=u"Parte del life event"),
        required=False,
        vocabulary="design.plone.contenttypes.AllLifeEventsVocabulary",
    )
    # come gestiamo correlati: novita, documenti, servizi?
