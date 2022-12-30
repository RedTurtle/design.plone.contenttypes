# -*- coding: utf-8 -*-
from design.plone.contenttypes.upgrades.upgrades import remove_blocks_behavior
from design.plone.contenttypes.upgrades.upgrades import update_types
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from redturtle.bandi.interfaces.settings import IBandoSettings
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

    # update behaviors
    portal_types = api.portal.get_tool(name="portal_types")
    BEHAVIORS = {
        "Document": {
            "in": [
                "plone.leadimage",
                "volto.preview_image",
            ],
            "out": [
                "plone.leadimage",
                "volto.preview_image",
                "plone.tableofcontents",
            ],
        },
    }
    for ct in BEHAVIORS.keys():
        ct_behaviors = [
            x
            for x in portal_types[ct].behaviors
            if x not in BEHAVIORS[ct]["out"]  # noqa
        ]
        ct_behaviors.extend([x for x in BEHAVIORS[ct]["in"] if x not in ct_behaviors])
        portal_types[ct].behaviors = tuple(ct_behaviors)

    # remove default ente
    api.portal.set_registry_record("default_ente", (), interface=IBandoSettings)


def post_install_taxonomy(context):
    update_types(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
