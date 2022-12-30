# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IDocumentoPersonale(model.Schema):
    """Marker interface for DocumentoPersonale"""

    protocollo = schema.TextLine(
        title=_("protocollo", default="Protocollo"), required=True
    )

    data_protocollo = schema.Date(
        title=_("data_protocollo", default="Data del protocollo"),
        required=True,
    )

    immagine = field.NamedImage(title=_("immagine", default="Immagine"), required=False)

    pratica_associata = field.NamedFile(
        title=_("pratica_associata", default="Pratica associata"),
        required=True,
    )

    servizio_origine = schema.Choice(
        title=_("servizio_origine", default="Servizio che genera il documento"),
        vocabulary="design.plone.contenttypes.Mockup",
        required=True,
    )

    # TODO: come gestiamo i campi "Tipologia del documento", "sottotipologia
    # del documento" e "lingua del documento"?

    # TODO: il vocabolario controllato da usare sara' "Argomenti di interesse
    #  pere gli utenti di un comune"
    argomenti_utenti = schema.Choice(
        title=_("argomenti_utenti", default="Argomenti utenti"),
        vocabulary="design.plone.contenttypes.Mockup",
        required=True,
    )

    oggetto = BlocksField(
        title=_("oggetto", default="Oggetto"),
        # non viene specificato se il campo e' obbligatorio o meno
        required=False,
    )

    # TODO: decidere se "link al documento" sara' un folder o un file. Se e'
    # un folder "formati disponibili" diventa un campo
    # generato facendo una query dei file presenti all'interno di "link al
    #  documento"?
    # Inserito come folder "Allegati" per il momento, magari si chiede

    # TODO: usare vocabolario dinamico per le tipologie di uffici (dovrebbe
    # rientrare nel content type "Unita' organizzativa")
    ufficio_responsabile = schema.Choice(
        title=_(
            "ufficio_responsabile_documento_personale",
            default="Ufficio responsabile",
        ),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    # TODO: usare vocabolario dinamico per le tipologie di aree amministrative
    # (dovrebbe rientrare nel content type "Unita' organizzativa")
    area_responsabile = schema.Choice(
        title=_(
            "area_responsabile_documento_personale",
            default="Area responsabile",
        ),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    # TODO: usare vocabolario dinamico per le gli autori?
    autori = RelationList(
        title="Autore/i",
        default=[],
        value_type=RelationChoice(
            title=_("Autore"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    licenza_distribuzione = schema.TextLine(
        title=_("licenza_distribuzione", default="Licenza di distribuzione"),
        required=False,
    )

    # TODO: usare vocabolario dinamico per i servizi collegati?
    servizi_collegati = RelationList(
        title="Servizi collegati",
        default=[],
        value_type=RelationChoice(
            title=_("Servizio collegato"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )

    canale_digitale_servizio = schema.TextLine(
        title=_(
            "canale_digitale_servizio",
            default="Canale digitale servizio collegato",
        ),
        required=False,
    )

    data_inizio = schema.Date(
        title=_("data_inizio", default="Data di inizio"), required=False
    )

    data_e_fasi_intermedie = BlocksField(
        title=_("data_e_fasi_intermedie", default="Data e fasi intermedie"),
        required=False,
    )

    data_inizio = schema.Date(
        title=_("data_inizio", default="Data di inizio"), required=False
    )

    # TODO: vocabolario per i dataset collegati ad un documento
    dataset = RelationList(
        title=_("Dataset"),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Dataset collegato"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    informazioni = BlocksField(
        title=_("informazioni", default="Ulteriori informazioni"),
        required=False,
    )

    riferimenti_normativi = BlocksField(
        title=_("riferimenti_normativi", default="Riferimenti normativi"),
        required=False,
    )
