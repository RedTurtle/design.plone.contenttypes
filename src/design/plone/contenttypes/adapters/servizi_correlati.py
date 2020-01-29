from zope.interface import implementer
from .interfaces import ICorrelati, Correlati
from plone import api
from zope.event import notify
from plone.namedfile.file import NamedBlobFile
import base64


@implementer(ICorrelati)
class GetCorrelatiServizi(Correlati):
    """ Adapter for upload file """

    def __call__(self):
        data = super(GetCorrelatiServizi, self).__call__()

        # using acquisition to get documenti folder from hosted in context
        # TODO: non usare acqusition per recuperare quel dato
        import pdb

        pdb.set_trace()
