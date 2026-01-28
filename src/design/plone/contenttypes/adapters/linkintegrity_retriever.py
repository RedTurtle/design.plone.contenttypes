"""Link Integrity - link retriever methods."""

from design.plone.contenttypes.interfaces.servizio import IServizio
from plone.app.linkintegrity.interfaces import IRetriever
from zope.component import adapter
from zope.interface import implementer


@implementer(IRetriever)
@adapter(IServizio)
class ServizioCanaleDigitaleRetriever:
    """"""

    def __init__(self, context):
        self.context = context

    def retrieveLinks(self):
        """
        If canale_digitale_link refers to an internal object, enable linkintegrity
        """
        canale_digitale_link = getattr(self.context, "canale_digitale_link", None)
        if canale_digitale_link and "resolveuid" in canale_digitale_link:
            return [canale_digitale_link]
        return []
