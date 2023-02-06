# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model

from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.contenttypes import _


class ICartellaModulistica(model.Schema, IDesignPloneContentType):
    """Cartella Modulistica"""

    visualize_files = schema.Bool(
        title=_("visualize_files", default="Visualizza i file allegati"),
        description="Visualizza i fai nei tutti i contentuti della cartella al posto di scaricare immediatamente",
        required=False,
        default=False,
    )
