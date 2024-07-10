# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.cartella_modulistica import (
    ICartellaModulistica,
)
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(ICartellaModulistica)
class CartellaModulistica(Container):
    """Cartella Modulistica"""
