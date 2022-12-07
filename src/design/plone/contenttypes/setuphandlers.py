# -*- coding: utf-8 -*-
from plone import api
from redturtle.bandi.interfaces.settings import IBandoSettings
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "design.plone.contenttypes:uninstall",
            "design.plone.contenttypes:to_3000",
        ]


def post_install(context):
    """Post install script"""

    remove_blocks_behavior(context)

    portal_types = api.portal.get_tool(name="portal_types")
    # add image fields at the end of document behaviors and remove tableofcontents
    document_behaviors = [
        x
        for x in portal_types["Document"].behaviors
        if x
        not in [
            "plone.leadimage",
            "volto.preview_image",
            "plone.tableofcontents",
        ]
    ]
    document_behaviors.extend(["plone.leadimage", "volto.preview_image"])
    portal_types["Document"].behaviors = tuple(document_behaviors)

    # remove default ente
    api.portal.set_registry_record("default_ente", (), interface=IBandoSettings)


def remove_blocks_behavior(context):
    portal_types = api.portal.get_tool(name="portal_types")
    for ptype in ["News Item", "Event"]:
        portal_types[ptype].behaviors = tuple(
            [x for x in portal_types[ptype].behaviors if x != "volto.blocks"]
        )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
