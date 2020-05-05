# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.messaggio import IMessaggio
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IMessaggio)
class Messaggio(Container):
    """ Marker interface for Messaggio
    """
