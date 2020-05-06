# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.unita_organizzativa_folder import (
    IUnitaOrganizzativaFolder,
)
from plone.app.contenttypes.content import Folder
from zope.interface import implementer


@implementer(IUnitaOrganizzativaFolder)
class UnitaOrganizzativaFolder(Folder):
    """
    """
