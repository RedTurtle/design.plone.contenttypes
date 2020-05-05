# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IPersona)
class Persona(Container):
    """
    """
