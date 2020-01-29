# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from plone.app.contenttypes.interfaces import INewsItem


@implementer(INewsItem)
class NewsItem(Container):
    '''
    '''
