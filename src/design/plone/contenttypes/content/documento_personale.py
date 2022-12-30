# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.documento_personale import IDocumentoPersonale
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IDocumentoPersonale)
class DocumentoPersonale(Container):
    """ """
