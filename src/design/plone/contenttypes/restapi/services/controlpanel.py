# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import (
    IDesignPloneSettings,
    IDesignPloneSettingsControlpanel,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


@adapter(Interface, Interface)
@implementer(IDesignPloneSettingsControlpanel)
class DesignPloneSettings(RegistryConfigletPanel):
    schema = IDesignPloneSettings
    configlet_id = "DesignPloneSettings"
    configlet_category_id = "Products"
    schema_prefix = None
