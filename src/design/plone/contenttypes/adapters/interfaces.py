# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from zope.interface import Interface


class ICorrelati(Interface):
    pass


class Correlati(object):
    """ Generic class for defining correlationn data """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        data = json_body(self.request)
        return data
