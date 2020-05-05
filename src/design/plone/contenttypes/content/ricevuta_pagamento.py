# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.ricevuta_pagamento import (
    IRicevutaPagamento,
)
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IRicevutaPagamento)
class RicevutaPagamento(Container):
    '''
    '''
