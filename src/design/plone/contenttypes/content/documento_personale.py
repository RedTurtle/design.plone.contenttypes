# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.documento_personale import (
    IDocumentoPersonale,
)


@implementer(IDocumentoPersonale)
class DocumentoPersonale(Container):
    '''
    '''
