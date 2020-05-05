# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IServizio)
class Servizio(Container):
    """
    """
