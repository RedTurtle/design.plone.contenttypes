# -*- coding: utf-8 -*-
from .upgrades import logger
from plone import api


def to_8000(context):
    """
    Convert old-style behavior names, keeping the original order.
    Iterate over all portal_types as a safety net: each product should fix its
    own types, but this catches any type we missed.
    """
    mapping = {
        "plone.app.content.interfaces.INameFromTitle": "plone.namefromtitle",
        "plone.app.dexterity.behaviors.discussion.IAllowDiscussion": "plone.allowdiscussion",
        "plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation": "plone.excludefromnavigation",
        "plone.app.dexterity.behaviors.id.IShortName": "plone.shortname",
        "plone.app.dexterity.behaviors.metadata.IDublinCore": "plone.dublincore",
        "plone.app.relationfield.behavior.IRelatedItems": "plone.relateditems",
        "plone.app.versioningbehavior.behaviors.IVersionable": "plone.versioning",
        "plone.app.lockingbehavior.behaviors.ILocking": "plone.locking",
        "Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes": "plone.constraintypes",
    }

    portal_types = api.portal.get_tool(name="portal_types")
    for type_id, fti in portal_types.objectItems():
        old_behaviors = tuple(getattr(fti, "behaviors", ()))
        behaviors = []
        for behavior in old_behaviors:
            new_behavior = mapping.get(behavior, behavior)
            if new_behavior != behavior:
                logger.info(
                    f"[{type_id}] Replaced behavior {behavior} => {new_behavior}"
                )
            if new_behavior not in behaviors:
                behaviors.append(new_behavior)
        if tuple(behaviors) != old_behaviors:
            # _updateProperty also notifies the FTI modification (schema cache)
            fti._updateProperty("behaviors", tuple(behaviors))
