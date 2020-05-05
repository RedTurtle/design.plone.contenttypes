# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def newsFolderCreateHandler(newsFolder, event):
    """ create Novita, set constraints and create structure tree if necessary
    """
    notizie = api.content.create(
        type="Folder", title="Notizie", container=newsFolder
    )
    comunicati = api.content.create(
        type="Folder", title="Comunicati", container=newsFolder
    )
    eventi = api.content.create(
        type="Folder", title="Eventi", container=newsFolder
    )

    notizieConstraints = ISelectableConstrainTypes(notizie)
    notizieConstraints.setConstrainTypesMode(1)
    notizieConstraints.setLocallyAllowedTypes(("Notizie e comunicati stampa",))

    comunicatiConstraints = ISelectableConstrainTypes(comunicati)
    comunicatiConstraints.setConstrainTypesMode(1)
    comunicatiConstraints.setLocallyAllowedTypes(
        ("Notizie e comunicati stampa",)
    )

    eventiConstraints = ISelectableConstrainTypes(eventi)
    eventiConstraints.setConstrainTypesMode(1)
    eventiConstraints.setLocallyAllowedTypes(("Evento",))
