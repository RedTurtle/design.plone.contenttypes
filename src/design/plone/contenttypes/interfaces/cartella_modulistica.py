# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.supermodel import model
from zope import schema


class ICartellaModulistica(model.Schema, IDesignPloneContentType):
    """Cartella Modulistica"""

    visualize_files = schema.Bool(
        title=_("visualize_files_title", default="Mostra i PDF in anteprima"),
        description=_(
            "visulize_files_description",
            default="Permette di aprire l'anteprima di tutti i PDF di questa cartella"
            " in una tab separata, altrimenti i PDF vengono scaricati",
        ),
        required=False,
        default=False,
    )
