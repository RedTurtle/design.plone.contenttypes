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

    ricerca_in_testata = schema.Bool(
        title=_("ricerca_in_testata_title", default="Mostra ricerca in testata"),
        description=_(
            "ricerca_in_testata_description",
            default="Permette di cercare campi in testata",
        ),
        required=False,
        default=True,
    )

    non_collassare_gli_elementi = schema.Bool(
        title=_(
            "non_collassare_gli_elementi_title", default="Non collassare gli elementi"
        ),
        description=_(
            "non_collassare_gli_elementi_description",
            default="Permette di non collassare gli elementi",
        ),
        required=False,
        default=False,
    )
