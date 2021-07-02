# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IInfoTestata(model.Schema):
    """
    """

    info_testata = RichText(
        title=_(
            u"info_testata_label",
            default=u"Informazioni aggiuntive per la testata",
        ),
        required=False,
        description=_(
            "info_testata_help",
            default="Inserisci eventuale testo informativo che verrà mostrato in testata.",  # noqa
        ),
    )
    immagine_testata = namedfile.NamedBlobImage(
        title=_(
            u"immagine_testata_label",
            default=u"Immagine aggiuntiva per la testata",
        ),
        description=u"Inserisci un'eventuale immagine da mostrare in testata.",
        required=False,
    )
    ricerca_in_testata = schema.Bool(
        title=_(u"ricerca_in_testata_label", default=u"Ricerca in testata"),
        default=False,
        required=False,
        description=_(
            "ricerca_in_testata_help",
            default="Seleziona se mostrare o meno il campo di ricerca in testata.",
        ),
    )
    mostra_bottoni_condivisione = schema.Bool(
        title=_(
            u"mostra_bottoni_condivisione_label",
            default=u"Mostra i bottoni per la condivisione sui social",
        ),
        default=False,
        required=False,
        description=_(
            "mostra_bottoni_condivisione_help",
            default="Seleziona se mostrare o meno i bottoni con i link per "
            "la condivisione sui vari social, mail e stampa.",
        ),
    )
    mostra_navigazione = schema.Bool(
        title=_(u"mostra_navigazione_label", default=u"Mostra la navigazione"),
        default=False,
        required=False,
        description=_(
            "mostra_navigazione_help",
            default="Seleziona se mostrare o meno la navigazione laterale nella testata.",  # noqa
        ),
    )

    model.fieldset(
        "testata",
        label=_("testata_fieldset_label", default=u"Testata"),
        fields=[
            "ricerca_in_testata",
            "mostra_bottoni_condivisione",
            "immagine_testata",
            "info_testata",
            "mostra_navigazione",
        ],
    )


@implementer(IInfoTestata)
@adapter(IDexterityContent)
class InfoTestata(object):
    """
    """

    def __init__(self, context):
        self.context = context
