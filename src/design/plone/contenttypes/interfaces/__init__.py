# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from redturtle.volto.interfaces import IRedturtleVoltoLayer
from zope.interface import Interface


class IDesignPloneContenttypesLayer(IRedturtleVoltoLayer):
    """Marker interface that defines a browser layer."""


class IDesignPloneContentType(Interface):
    """
    Marker interface for all Design Italia content-types
    """
