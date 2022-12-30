# -*- coding: utf-8 -*-
from .interfaces import Correlati
from .interfaces import ICorrelati
from zope.interface import implementer


@implementer(ICorrelati)
class GetCorrelatiServizi(Correlati):
    """Adapter for upload file"""
