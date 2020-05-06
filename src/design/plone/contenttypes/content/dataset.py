# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer
from design.plone.contenttypes.interfaces.dataset import IDataset


@implementer(IDataset)
class Dataset(Container):
    '''
    '''
