# -*- coding: utf-8 -*-
from zope.interface import implementer
from design.plone.contenttypes.interfaces.persone_folder import IPersoneFolder
from plone.app.contenttypes.content import Folder


@implementer(IPersoneFolder)
class PersoneFolder(Folder):
    """ Marker interface for PersoneFolder
    """
