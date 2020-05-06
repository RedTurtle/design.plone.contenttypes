# -*- coding: utf-8 -*-
from design.plone.contenttypes.utils import folderSubstructureGenerator
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["design.plone.contenttypes:uninstall"]


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    folderSubstructureGenerator(portal, "Amministrazione")
    folderSubstructureGenerator(portal, "Servizi")
    folderSubstructureGenerator(portal, "Novità")
    folderSubstructureGenerator(portal, "Documenti e dati")


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
