# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.persone_folder import IPersoneFolder
from plone.app.contenttypes.content import Folder
from zope.interface import implementer


@implementer(IPersoneFolder)
class PersoneFolder(Folder):
    """ Marker interface for PersoneFolder
    """
