# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import INewsItem
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(INewsItem)
class NewsItem(Container):
    '''
    '''
