# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from design.plone.contenttypes.interfaces.messaggio import IMessaggio
from zope.interface import implementer

@implementer(IMessaggio)
class Messaggio(Container):
    """ Marker interface for Messaggio
    """
