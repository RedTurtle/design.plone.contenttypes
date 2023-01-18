# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.interfaces import IRow
from design.plone.contenttypes import _
from plone.restapi.types.adapters import ObjectJsonSchemaProvider
from plone.restapi.types.interfaces import IJsonSchemaProvider
from plone.restapi.types.utils import get_fieldsets
from plone.restapi.types.utils import get_jsonschema_properties
from plone.restapi.types.utils import iter_fields
from zope.component import adapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IField
from zope.schema.interfaces import IVocabularyFactory


DATAGRID_FIELDS = ["value_punto_contatto", "timeline_tempi_scadenze"]


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
                default="La dimensione dell'immagine dovrebbe essere di ${size} px",  # noqa
                mapping={"size": portal_type_size},
            )
            schema["description"] = translate(msgid, context=self.request)

        return schema


@adapter(IRow, Interface, Interface)
@implementer(IJsonSchemaProvider)
class DataGridRowJsonSchemaProvider(ObjectJsonSchemaProvider):
    def __init__(self, field, context, request):
        super().__init__(field, context, request)
        self.fieldsets = get_fieldsets(context, request, self.field.schema)

    def get_factory(self):
        return "DataGridField Row"

    def get_properties(self):
        if self.prefix:
            prefix = ".".join([self.prefix, self.field.__name__])
        else:
            prefix = self.field.__name__
        return get_jsonschema_properties(
            self.context, self.request, self.fieldsets, prefix
        )

    def additional(self):
        info = super().additional()
        properties = self.get_properties()
        required = []
        for field in iter_fields(self.fieldsets):
            name = field.field.getName()

            # Determine required fields
            if field.field.required:
                required.append(name)

            # Include field modes
            if field.mode:
                properties[name]["mode"] = field.mode

        info["fieldsets"] = [
            {
                "id": "default",
                "title": "Default",
                "fields": [x for x in properties.keys()],
            },
        ]
        info["required"] = required
        info["properties"] = properties
        return info
