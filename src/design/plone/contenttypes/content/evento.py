# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from plone.event.interfaces import IEvent


@implementer(IEvent)
class Event(Container):
    """
    """
