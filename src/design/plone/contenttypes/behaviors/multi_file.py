# -*- coding: utf-8 -*-
from plone.namedfile import field
from plone.dexterity.interfaces import IDexterityContent
from design.plone.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import provider, implementer


class IMultiFileSchema(model.Schema):
    """"""

    file_principale = field.NamedBlobFile(
        title=_("file_principale_label", default="File principale"),
        description=_(
            "file_principale_help",
            default="Inserisci il file principale di questo contenuto.",
        ),
        required=True,
    )

    formato_alternativo_1 = field.NamedBlobFile(
        title=_(
            "formato_alternativo_1_label", default="Formato alternativo 1"
        ),
        description=_(
            "formato_alternativo_1_help",
            default="Inserisci un eventuale formato alternativo del "
            "file principale.",
        ),
        required=False,
    )

    formato_alternativo_2 = field.NamedBlobFile(
        title=_(
            "formato_alternativo_2_label", default="Formato alternativo 2"
        ),
        description=_(
            "formato_alternativo_2_help",
            default="Inserisci un eventuale formato alternativo del "
            "file principale.",
        ),
        required=False,
    )


@provider(IFormFieldProvider)
class IMultiFile(IMultiFileSchema):
    """"""


@implementer(IMultiFile)
@adapter(IDexterityContent)
class MultiFile(object):
    """"""

    def __init__(self, context):
        self.context = context
