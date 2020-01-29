# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.luoghi_folder import ILuoghiFolder
from plone.app.contenttypes.content import Folder

from zope.interface import implementer


@implementer(ILuoghiFolder)
class LuoghiFolder(Folder):
    """
    """
