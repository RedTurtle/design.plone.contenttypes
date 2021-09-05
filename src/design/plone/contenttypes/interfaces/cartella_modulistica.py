# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.supermodel import model


class ICartellaModulistica(model.Schema, IDesignPloneContentType):
    """ Cartella Modulistica """
