# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.contenttypes.interfaces.punto_di_contatto import IPuntoDiContatto, IPDCValueSchema
from plone.app.dexterity.textindexer.converters import (
    DefaultDexterityTextIndexFieldConverter,
)
from plone.app.dexterity.textindexer.interfaces import IDexterityTextIndexFieldConverter
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.indexers import (
    TextBlockSearchableText as BaseTextBlockSearchableText,
)
from plone.restapi.interfaces import IBlockSearchableText
from z3c.form.interfaces import IWidget
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IList, IInterface
from collective.z3cform.datagridfield.interfaces import IDataGridFieldWidget


@implementer(IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IRelationChoice, IWidget)
class RelationChoiceFieldConverter(DefaultDexterityTextIndexFieldConverter):
    def convert(self):
        relation = self.field.get(self.context)
        if not relation:
            return ""
        related_obj = relation.to_object
        if not related_obj:
            return ""
        return related_obj.Title()


@implementer(IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IRelationList, IWidget)
class RelationListFieldConverter(DefaultDexterityTextIndexFieldConverter):
    def convert(self):
        relations = self.field.get(self.context)
        if not relations:
            return ""
        return " ".join([x.to_object.Title() for x in relations if x.to_object])


@implementer(IBlockSearchableText)
@adapter(IDesignPloneContentType, IBrowserRequest)
class TextBlockSearchableText(BaseTextBlockSearchableText):
    """ """


@implementer(IDexterityTextIndexFieldConverter)
@adapter(IPuntoDiContatto, IList, IDataGridFieldWidget)
class PDCFieldConverter(DefaultDexterityTextIndexFieldConverter):
    def __init__(self):
        import pdb; pdb.set_trace()

    def convert(self):
        import pdb; pdb.set_trace()
        relations = self.field.get(self.context)
        if not relations:
            return ""
        return " ".join([x.to_object.Title() for x in relations if x.to_object])


@implementer(IDexterityTextIndexFieldConverter)
@adapter(IPDCValueSchema, IInterface, IWidget)
class PDCValueFieldConverter(DefaultDexterityTextIndexFieldConverter):
    def convert(self):
        import pdb; pdb.set_trace()
        relations = self.field.get(self.context)
        if not relations:
            return ""
        return " ".join([x.to_object.Title() for x in relations if x.to_object])
