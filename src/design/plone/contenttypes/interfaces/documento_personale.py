# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IDocumentoPersonale(model.Schema):
    """ Marker interface for DocumentoPersonale
    """

    protocollo = schema.TextLine(
        title=_(u"protocollo", default=u"Protocollo"), required=True
    )

    data_protocollo = schema.Date(
        title=_(u"data_protocollo", default=u"Data del protocollo"), required=True
    )

    immagine = field.NamedImage(
        title=_(u"immagine", default=u"Immagine"), required=False
    )

    pratica_associata = field.NamedFile(
        title=_(u"pratica_associata", default=u"Pratica associata"), required=True
    )

    servizio_origine = schema.Choice(
        title=_(u"servizio_origine", default=u"Servizio che genera il documento"),
        vocabulary="design.plone.contenttypes.Mockup",
        required=True,
    )

    # TODO: come gestiamo i campi "Tipologia del documento", "sottotipologia
    # del documento" e "lingua del documento"?

    # TODO: il vocabolario controllato da usare sara' "Argomenti di interesse
    #  pere gli utenti di un comune"
    argomenti_utenti = schema.Choice(
        title=_(u"argomenti_utenti", default=u"Argomenti utenti"),
        vocabulary="design.plone.contenttypes.Mockup",
        required=True,
    )

    oggetto = RichText(
        title=_(u"oggetto", default=u"Oggetto"),
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
            u"ufficio_responsabile_documento_personale", default=u"Ufficio responsabile"
        ),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    # TODO: usare vocabolario dinamico per le tipologie di aree amministrative
    # (dovrebbe rientrare nel content type "Unita' organizzativa")
    area_responsabile = schema.Choice(
        title=_(u"area_responsabile_documento_personale", default=u"Area responsabile"),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    # TODO: usare vocabolario dinamico per le gli autori?
    autori = RelationList(
        title=u"Autore/i",
        default=[],
        value_type=RelationChoice(
            title=_(u"Autore"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    licenza_distribuzione = schema.TextLine(
        title=_(u"licenza_distribuzione", default=u"Licenza di distribuzione"),
        required=False,
    )

    # TODO: usare vocabolario dinamico per i servizi collegati?
    servizi_collegati = RelationList(
        title=u"Servizi collegati",
        default=[],
        value_type=RelationChoice(
            title=_(u"Servizio collegato"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    canale_digitale_servizio = schema.TextLine(
        title=_(
            u"canale_digitale_servizio", default=u"Canale digitale servizio collegato"
        ),
        required=False,
    )

    data_inizio = schema.Date(
        title=_(u"data_inizio", default=u"Data di inizio"), required=False
    )

    data_e_fasi_intermedie = RichText(
        title=_(u"data_e_fasi_intermedie", default=u"Data e fasi intermedie"),
        required=False,
    )

    data_inizio = schema.Date(
        title=_(u"data_inizio", default=u"Data di inizio"), required=False
    )

    # TODO: vocabolario per i dataset collegati ad un documento
    dataset = RelationList(
        title=_(u"Dataset"),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Dataset collegato"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    informazioni = RichText(
        title=_(u"informazioni", default=u"Ulteriori informazioni"), required=False
    )

    riferimenti_normativi = RichText(
        title=_(u"riferimenti_normativi", default=u"Riferimenti normativi"),
        required=False,
    )
