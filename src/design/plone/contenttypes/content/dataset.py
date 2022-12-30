# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.dataset import IDataset
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IDataset)
class Dataset(Container):
    """ """
