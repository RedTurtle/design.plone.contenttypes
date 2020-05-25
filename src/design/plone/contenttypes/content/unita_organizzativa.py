# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IUnitaOrganizzativa)
class UnitaOrganizzativa(Container):
    '''
    '''
