# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.relationfield import (
    RelationListFieldSerializer as DefaultRelationListFieldSerializer,
)
from z3c.relationfield.interfaces import IRelationList
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer


@adapter(IRelationList, IDexterityContent, IDesignPloneContenttypesLayer)
@implementer(IFieldSerializer)
class RelationListFieldSerializer(DefaultRelationListFieldSerializer):
    def __call__(self):
        data = []
        for value in self.get_value():
            if not value:
                continue
            try:
                content = value.to_object
            except AttributeError:
                # we'll migrate to PDC, right now we have Blocks
                continue
            if not content:
                continue
            if not api.user.has_permission("View", obj=content):
                continue
            if content.effective().isFuture() and not api.user.has_permission(
                "Modify portal content", obj=self.context
            ):
                # effective date is in the future.
                # Users that can edit current context, should see it because otherwise
                # they will not see it in edit form.
                continue
            summary = getMultiAdapter(
                (content, getRequest()), ISerializeToJsonSummary
            )()
            if content.effective().Date() != "1969/12/31":
                summary["effective"] = json_compatible(content.effective())
            else:
                summary["effective"] = None
            if content.portal_type == "Event":
                summary["start"] = json_compatible(getattr(content, "start", ""))
                summary["end"] = json_compatible(getattr(content, "end", ""))
            if getattr(content, "icona", ""):
                summary["icona"] = content.icona
            data.append(json_compatible(summary))
        return data
