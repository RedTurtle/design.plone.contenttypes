from plone.supermodel import model
from plone.app.textfield import RichText
from zope import schema
from plone.namedfile import field
from zope.interface import provider, implementer
from zope.component import adapter
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice, RelationList
from design.plone.contenttypes import _


# TODO: merge with NEWS
@provider(IFormFieldProvider)
class INotizieEComunicatiStampa(model.Schema):
    """ Marker interface for NotizieEComunicatiStampa
    """

    # TODO: vocabolario per le tipologie di notizie
    tipologia_notizia = schema.Choice(
        title=_(u"tipologia_notizia", default=u"Tipologia notizia"),
        required=True,
        vocabulary="design.plone.contenttypes.Mockup",
    )

    # numero progressivo del cs se esiste. Numero o stringa?
    numero_progressivo_cs = schema.TextLine(
        title=_(
            u"numero_progressivo_cs",
            default=u"Numero progressivo del comunicato stampa",
        ),
        required=False,
    )

    a_cura_di = RelationChoice(
        title=_(u"a_cura_di", default=u"A cura di"),
        required=True,
        vocabulary="plone.app.vocabularies.Catalog",
    )

    immagine = field.NamedImage(
        title=_(u"immagine", default=u"Immagine in evidenza"), required=False,
    )

    tassonomia_argomenti = schema.List(
        title=_(u"tassonomia_argomenti", default=u"Tassonomia argomenti"),
        default=[],
        value_type=schema.Choice(
            title=_(u"Argomenti"),
            vocabulary="design.plone.contenttypes.TagsVocabulary",
        ),
        required=False,
    )

    # come trattiamo le back reference, ad esempio quelle a "Persone" e "Luoghi"?
    # multiref usando due cartelle come "buche"
    # non genera duplicazione? quei dati hanno gia' delle buche

    # fare folder multimedia

    # stile specifico da usare in frontend

    documenti_allegati = RelationList(
        title=u"Documenti allegati",
        default=[],
        value_type=RelationChoice(
            title=_(u"documenti_allegati", default=u"Documenti allegati"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "documenti_allegati",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Documento"],
        },
    )

    dataset = RichText(
        title=_(u"dataset", default=u"Dataset"), required=False,
    )

    informazioni = RichText(
        title=_(u"informazioni", default=u"Informazioni"), required=True,
    )

    # TODO: come gestiamo i correlati?


@implementer(INotizieEComunicatiStampa)
@adapter(IDexterityContent)
class NotizieEComunicatiStampa(object):
    """
    """

    def __init__(self, context):
        self.context = context
