# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.services import Service
from zope.interface import alsoProvides

import plone.protect.interfaces


class CorrelatiService(Service):
    """Service to make action"""

    def reply(self):
        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        results = api.content.get_view(
            name="correlati",
            context=self.context,
            request=self.context.REQUEST,
        )()

        # TODO: serializzare la possibile risposta
        # XXX: si rompe
        return results
