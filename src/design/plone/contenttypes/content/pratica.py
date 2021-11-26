# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.pratica import IPratica
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IPratica)
class Pratica(Container):
    """ """
