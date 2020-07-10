# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("design.plone.contenttypes")

# need to be the last thing we import: in the patch we import the message
# factory above
from design.plone.contenttypes import patches  # noqa
