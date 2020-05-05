# -*- coding: utf-8 -*-
from .interfaces import ICorrelati, Correlati
from zope.interface import implementer


@implementer(ICorrelati)
class GetCorrelatiServizi(Correlati):
    """ Adapter for upload file """
