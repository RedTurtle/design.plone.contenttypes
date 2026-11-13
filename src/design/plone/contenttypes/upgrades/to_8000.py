# -*- coding: utf-8 -*-
from .upgrades import logger
from Acquisition import aq_base
from plone import api
from plone.namedfile import file


def to_8000(context):
    """
    convert old-style behavior names
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
    for type_id, portal_type in portal_types.items():
        behaviors = list(portal_type.behaviors)
        for old_behavior, new_behavior in mapping.items():
            if old_behavior in behaviors:
                behaviors.remove(old_behavior)
                if new_behavior not in behaviors:
                    behaviors.append(new_behavior)
                    logger.info(
                        f"[{type_id}] Replaced behavior {old_behavior} => {new_behavior}"
                    )
        portal_type.behaviors = tuple(behaviors)
