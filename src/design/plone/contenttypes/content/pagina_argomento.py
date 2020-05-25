# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.pagina_argomento import (
    IPaginaArgomento,
)
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IPaginaArgomento)
class PaginaArgomento(Container):
    '''
    '''
