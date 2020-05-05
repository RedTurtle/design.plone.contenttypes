# -*- coding: utf-8 -*-
from zope.interface import implementer
from design.plone.contenttypes.interfaces.amministrazione_folder import (
    IAmministrazioneFolder,
)
from plone.app.contenttypes.content import Folder


@implementer(IAmministrazioneFolder)
class AmministrazioneFolder(Folder):
    """
    """

    pass
