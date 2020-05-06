# -*- coding: utf-8 -*-
from collective.venue.interfaces import IVenue
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IVenue)
class Venue(Container):
    """
    """
