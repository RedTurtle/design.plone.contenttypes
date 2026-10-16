from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.supermodel import model


class IModulo(model.Schema, IDesignPloneContentType):
    """Modulo"""
