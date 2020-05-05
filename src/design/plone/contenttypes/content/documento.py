# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.documento import IDocumento


@implementer(IDocumento)
class Documento(Container):
    """
    """
