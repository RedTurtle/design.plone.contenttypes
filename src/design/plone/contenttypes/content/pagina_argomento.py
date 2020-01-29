# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.pagina_argomento import IPaginaArgomento

@implementer(IPaginaArgomento)
class PaginaArgomento(Container):
    '''
    '''