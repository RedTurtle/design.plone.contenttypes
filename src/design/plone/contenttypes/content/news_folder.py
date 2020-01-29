# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.news_folder import INewsFolder
from plone.app.contenttypes.content import Folder
from zope.interface import implementer


@implementer(INewsFolder)
class NewsFolder(Folder):
    """
    """
