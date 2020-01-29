# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from design.plone.contenttypes.interfaces.ricevuta_pagamento import IRicevutaPagamento

@implementer(IRicevutaPagamento)
class RicevutaPagamento(Container):
    '''
    '''