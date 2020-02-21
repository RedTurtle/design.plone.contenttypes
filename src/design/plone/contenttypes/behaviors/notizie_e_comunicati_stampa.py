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
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from design.plone.contenttypes import _


# TODO: merge with NEWS
@provider(IFormFieldProvider)
class INotizieEComunicatiStampa(model.Schema):
    """ Marker interface for NotizieEComunicatiStampa
    """

    model.fieldset(
        'other_information',
        label=_(u'other_information', default=u'Informazioni avanzate'),
        fields=['numero_progressivo_cs', 'tassonomia_argomenti', 'dataset', 'luoghi_notizia']
    )
    model.fieldset(
        'categorization',
        fields=['related_news']
    )


    # TODO: vocabolario per le tipologie di notizie
    tipologia_notizia = schema.Choice(
        title=_(u"tipologia_notizia", default=u"Tipologia notizia"),
        required=True,
        vocabulary="design.plone.contenttypes.TipologiaNotizia",
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
    form.widget(
        "a_cura_di",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Unita organizzativa"],
        },
    )
    a_cura_di_persone = RelationList(
        title=_(u'a_cura_di_persone', default=u'Persone'),
        default=[],
        value_type=RelationChoice(
            title=u'Related', vocabulary='plone.app.vocabularies.Catalog'
        ),
        required=False,
    )
    form.widget(
        'a_cura_di_persone',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'recentlyUsed': True,  # Just turn on. Config in plone.app.widgets.
            "selectableTypes": ["Persona"],
        },
    )

    # immagine = field.NamedImage(
    #     title=_(u"immagine", default=u"Immagine in evidenza"), required=False,
    # )

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

    related_news = RelationList(
        title=u"Notizie collegate",
        default=[],
        value_type=RelationChoice(
            title=_(u"related_news", default=u"Notizie collegate"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "related_news",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["News Item"],
        },
    )

    luoghi_notizia = RelationList(
        title=u"Luoghi notizia",
        default=[],
        value_type=RelationChoice(
            title=_(u"luoghi_notizia", default=u"Luoghi"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    form.widget(
        "luoghi_notizia",
        RelatedItemsFieldWidget,
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Venue"],
        },
    )

    dataset = RichText(
        title=_(u"dataset", default=u"Dataset"), required=False,
    )

    # informazioni = RichText(
    #     title=_(u"informazioni", default=u"Informazioni"), required=True,
    # )

    # TODO: come gestiamo i correlati?


@implementer(INotizieEComunicatiStampa)
@adapter(IDexterityContent)
class NotizieEComunicatiStampa(object):
    """
    """

    def __init__(self, context):
        self.context = context
