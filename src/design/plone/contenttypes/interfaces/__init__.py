"""Module where all interfaces, events and exceptions live."""

from redturtle.bandi.interfaces.browserlayer import IRedturtleBandiLayer
from redturtle.volto.interfaces import IRedturtleVoltoLayer
from zope.interface import Interface


class IDesignPloneContenttypesLayer(IRedturtleVoltoLayer, IRedturtleBandiLayer):
    """Marker interface that defines a browser layer."""


class IDesignPloneContentType(Interface):
    """
    Marker interface for all Design Italia content-types
    """
