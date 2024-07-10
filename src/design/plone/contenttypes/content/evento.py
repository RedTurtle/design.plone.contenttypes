# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.event.interfaces import IEvent
from zope.interface import implementer


@implementer(IEvent)
class Event(Container):
    """ """
