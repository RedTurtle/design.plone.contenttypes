# -*- coding: utf-8 -*-
from plone import api


def bandoCreateHandler(bando, event):
    """ """
    folders = [
        {"id": "documenti", "title": "Documenti"},
        {"id": "comunicazioni", "title": "Comunicazioni"},
        {"id": "esiti", "title": "Esiti"},
    ]
    for mapping in folders:
        if mapping["id"] not in bando:
            api.content.create(
                type="Bando Folder Deepening",
                title=mapping["title"],
                id=mapping["id"],
                container=bando,
            )
