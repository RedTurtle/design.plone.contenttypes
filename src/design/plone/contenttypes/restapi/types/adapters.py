# -*- coding: utf-8 -*-
from plone.restapi.types.adapters import ObjectJsonSchemaProvider
from plone.restapi.types.interfaces import IJsonSchemaProvider
from zope.component import adapter, getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IField, IVocabularyFactory

from design.plone.contenttypes import _


@adapter(IField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class LeadImageJsonSchemaProvider(ObjectJsonSchemaProvider):
    def get_size_vocabulary(self):

        factory = getUtility(
            IVocabularyFactory, "design.plone.vocabularies.leadimage_dimension"
        )

        vocabulary = factory(self.context)._terms
        return {term.token: term.title for term in vocabulary if term.token}

    def get_schema(self):
        schema = super(LeadImageJsonSchemaProvider, self).get_schema()
        sizes = self.get_size_vocabulary()
        portal_type = getattr(self.request, "steps")[-1]
        portal_type_size = sizes.get(portal_type, None)
        if portal_type_size:
            msgid = _(
                "image_size_help",
                default=u"La dimensione dell'immagine dovrebbe essere di ${size} px",  # noqa
                mapping={u"size": portal_type_size},
            )
            schema["description"] = translate(msgid, context=self.request)

        return schema
