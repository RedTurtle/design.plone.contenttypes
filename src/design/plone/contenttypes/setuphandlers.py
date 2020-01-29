# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import (
    INonInstallable,
    ISelectableConstrainTypes,
)
from design.plone.contenttypes.utils import folderSubstructureGenerator
from zope.interface import implementer
from plone import api


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "design.plone.contenttypes:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()

    # if not api.content.find(portal_type="AmministrazioneFolder"):
    # amministrazione = api.content.create(
    #     container=portal,
    #     type="Folder",
    #     id="amministrazione",
    #     title="Amministrazione",
    # )

    # api.content.transition(obj=amministrazione, transition="publish")

    # also generate amministrazione substructure like this, removing
    # custom folder cts?
    folderSubstructureGenerator(portal, "Amministrazione")
    folderSubstructureGenerator(portal, "Servizi")
    folderSubstructureGenerator(portal, "Novità")
    folderSubstructureGenerator(portal, "Documenti e dati")
    # news = api.content.create(
    #     container=portal, type="NewsFolder", id="novità", title="Novità",
    # )
    # api.content.transition(obj=news, transition="publish")

    # servizi = api.content.create(
    #     container=portal, type="Folder", id="servizi", title="Servizi",
    # )
    # serviziConstraints = ISelectableConstrainTypes(servizi)
    # serviziConstraints.setConstrainTypesMode(1)
    # serviziConstraints.setLocallyAllowedTypes(("Servizio",))

    # tolgo la possibilità di aggiungere l'oggetto ovunque
    # pt = portal.portal_types
    # Amministrazione = pt["AmministrazioneFolder"]
    # Amministrazione.global_allow = False


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
