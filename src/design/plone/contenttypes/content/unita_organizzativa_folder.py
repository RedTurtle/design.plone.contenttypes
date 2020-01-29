# -*- coding: utf-8 -*-
from zope.interface import implementer
from design.plone.contenttypes.interfaces.unita_organizzativa_folder import (
    IUnitaOrganizzativaFolder,
)
from plone.app.contenttypes.content import Folder


@implementer(IUnitaOrganizzativaFolder)
class UnitaOrganizzativaFolder(Folder):
    """ 
    """
