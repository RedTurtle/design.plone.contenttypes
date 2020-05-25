# -*- coding: utf-8 -*-
from design.plone.contenttypes.adapters.interfaces import ICorrelati
from plone.dexterity.browser import edit
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError


class Correlati(BrowserView):
    """ View to make action """

    def __call__(self):
        correlati = None
        try:
            correlati = getMultiAdapter(
                (self.context, self.context.REQUEST),
                ICorrelati,
                self.context.portal_type,
            )
        except ComponentLookupError:
            raise NotImplementedError("These action are not implemented yet")

        if correlati:
            return correlati()
        return None


class EditForm(edit.DefaultEditForm):
    pass
