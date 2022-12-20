# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.punto_di_contatto import IPuntoDiContatto


@implementer(IPuntoDiContatto)
class PuntoDiContatto(Container):
    """ """
