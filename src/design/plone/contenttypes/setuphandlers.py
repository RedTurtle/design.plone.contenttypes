# -*- coding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from redturtle.bandi.interfaces.settings import IBandoSettings
from zope.component import getUtilitiesFor
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

    api.portal.set_registry_record("default_ente", (), interface=IBandoSettings)


def post_install_taxonomy(context):
    context.runImportStepFromProfile(
        "profile-design.plone.contenttypes:default", "typeinfo", True
    )
    # C'è una versione di collective.taxonomies in cui quel campo non viene
    # settato correttamente.
    for utility_name, utility in list(getUtilitiesFor(ITaxonomy)):
        utility.updateBehavior(**{"field_prefix": ""})


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def remove_blocks_behavior(context):
    portal_types = api.portal.get_tool(name="portal_types")
    for ptype in ["News Item", "Event"]:
        portal_types[ptype].behaviors = tuple(
            [x for x in portal_types[ptype].behaviors if x != "volto.blocks"]
        )
