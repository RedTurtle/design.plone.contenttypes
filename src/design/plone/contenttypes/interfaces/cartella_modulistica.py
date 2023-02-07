# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model

from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.contenttypes import _


class ICartellaModulistica(model.Schema, IDesignPloneContentType):
    """Cartella Modulistica"""

    visualize_files = schema.Bool(
        title=_("visualize_files_title", default="Mostra i PDF in anteprima"),
        description=_(
            "visulize_files_description",
            default="Permette di aprire l'anteprima di tutti i PDF di questa cartella in una tab separata, altrimenti i PDF vengono scaricati",
        ),
        required=False,
        default=False,
    )
