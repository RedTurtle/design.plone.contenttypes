# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.cartella_modulistica import (
    ICartellaModulistica,
)


@implementer(ICartellaModulistica)
class CartellaModulistica(Container):
    """ Cartella Modulistica """
