# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from collective.venue.interfaces import IVenue


@implementer(IVenue)
class Venue(Container):
    """
    """
