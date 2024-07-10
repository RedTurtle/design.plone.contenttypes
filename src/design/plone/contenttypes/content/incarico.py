# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.incarico import IIncarico
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IIncarico)
class Incarico(Container):
    """ """
