# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.servizio import IServizio


@implementer(IServizio)
class Servizio(Container):
    """ 
    """
