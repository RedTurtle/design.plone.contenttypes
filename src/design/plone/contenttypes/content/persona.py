# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.persona import IPersona


@implementer(IPersona)
class Persona(Container):
    """ 
    """
