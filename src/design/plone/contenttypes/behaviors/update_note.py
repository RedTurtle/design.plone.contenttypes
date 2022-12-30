# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IUpdateNote(model.Schema):
    """ """

    update_note = schema.TextLine(
        title=_("update_note_label", default="Note di aggiornamento"),
        description=_(
            "help_update_note",
            default="Inserisci una nota per indicare che il contenuto corrente è stato aggiornato."  # noqa
            "Questo testo può essere visualizzato nei blocchi elenco con determinati layout per informare "  # noqa
            "gli utenti che un determinato contenuto è stato aggiornato. "
            "Ad esempio se in un bando sono stati aggiunti dei documenti.",
        ),
        required=False,
    )


@implementer(IUpdateNote)
@adapter(IDexterityContent)
class UpdateNote(object):
    """ """

    def __init__(self, context):
        self.context = context
