from Acquisition import aq_inner, aq_parent


def EventModified(dx_event, event):
    parent = aq_parent(aq_inner(dx_event))
    if parent.portal_type == "Event":
        parent.reindexObject(idxs=["rassegna"])
    return
