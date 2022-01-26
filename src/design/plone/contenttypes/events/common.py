# -*- coding: utf-8 -*-


def onModify(context, event):

    for description in event.descriptions:
        if "IBasic.title" in getattr(description, "attributes", []):
            for child in context.listFolderContents():
                child.reindexObject(idxs=["parent"])
