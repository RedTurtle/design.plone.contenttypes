# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.address.behaviors import IAddress
from plone.app.dexterity.textindexer import utils
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("design.plone.contenttypes")


# Mark fields from external behaviors indexable in SearchableText
utils.searchable(IAddress, "street")
utils.searchable(IAddress, "city")
utils.searchable(IAddress, "zip_code")
utils.searchable(IAddress, "country")

# need to be the last thing we import: in the patch we import the message
# factory above
#  TEMPORANEAMENTE DISABILITATO PER FARE L'OVERRIDE STANDARD
# from design.plone.contenttypes import patches  # noqa
