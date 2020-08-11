# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class IInfoTestata(model.Schema):
    """
    """

    info_testata = RichText(
        title=_(
            u"info_testata_label", default=u"Informazioni aggiuntive per la testata"
        ),
        required=False,
        description=_(
            "info_testata_help",
            default="Inserisci eventuale testo informativo che verrà mostrato in testata.",  # noqa
        ),
    )

    ricerca_in_testata = schema.Bool(
        title=_(u"ricerca_in_testata_label", default=u"Ricerca in testata"),
        default=False,
        description=_(
            "ricerca_in_testata_help",
            default="Seleziona se mostrare o meno il campo di ricerca in testata.",
        ),
    )

    mostra_navigazione = schema.Bool(
        title=_(u"mostra_navigazione_label", default=u"Mostra la navigazione"),
        default=False,
        description=_(
            "mostra_navigazione_help",
            default="Seleziona se mostrare o meno la navigazione laterale nella testata.",  # noqa
        ),
    )

    model.fieldset(
        "testata",
        label=_("testata_fieldset_label", default=u"Testata"),
        fields=["info_testata", "ricerca_in_testata"],
    )


@implementer(IInfoTestata)
@adapter(IDexterityContent)
class InfoTestata(object):
    """
    """

    def __init__(self, context):
        self.context = context
