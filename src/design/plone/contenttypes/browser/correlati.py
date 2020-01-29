from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from Products.Five import BrowserView
from design.plone.contenttypes.adapters.interfaces import ICorrelati
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from plone.dexterity.browser import edit


class Correlati(BrowserView):
    """ View to make action """

    def __call__(self):
        correlati = None
        import pdb

        pdb.set_trace()
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
