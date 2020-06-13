# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.vocabularies import (
    IVocabulariesControlPanel,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, Interface)
class VocabulariesControlpanel(RegistryConfigletPanel):
    schema = IVocabulariesControlPanel
    configlet_id = "DesignPloneVocabularies"
    configlet_category_id = "Products"
    schema_prefix = None
