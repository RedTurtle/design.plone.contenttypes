# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.punto_di_contatto import IPuntoDiContatto
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IPuntoDiContatto)
class PuntoDiContatto(Container):
    """ """
