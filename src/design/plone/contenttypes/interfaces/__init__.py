# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IDesignPloneContenttypesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IDesignPloneContentType(Interface):
    """
    Marker interface for all Design Italia content-types
    """
