"""
This is a customization for original view. in design.plone.contenttypes
we allow folder deepening to contain also Modulo CT and we need to
handle it properly
"""

from design.plone.contenttypes.behaviors.multi_file import IMultiFileSchema
from plone.restapi.interfaces import IFieldSerializer
from redturtle.bandi.browser.bando import BandoView as BaseBandoView
from redturtle.bandi.browser.bando import IBandoView
from zope.component import queryMultiAdapter
from zope.interface import implementer

MODULO_FIELDS = [
    "file_principale",
    "formato_alternativo_1",
    "formato_alternativo_2",
]


@implementer(IBandoView)
class BandoView(BaseBandoView):

    def type_hook_modulo(self, brain):
        """
        Custom data for modulo
        """
        obj = brain.getObject()
        data = {}
        for field in MODULO_FIELDS:
            field_obj = IMultiFileSchema[field]
            serializer = queryMultiAdapter(
                (field_obj, obj, self.request), IFieldSerializer
            )
            data[field] = serializer()
        return data
