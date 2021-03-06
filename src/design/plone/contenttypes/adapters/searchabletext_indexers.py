# -*- coding: utf-8 -*-
from collective.dexteritytextindexer.converters import (
    DefaultDexterityTextIndexFieldConverter,
)
from collective.dexteritytextindexer.interfaces import IDexterityTextIndexFieldConverter
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from plone.dexterity.interfaces import IDexterityContent
from z3c.form.interfaces import IWidget
from zope.component import adapter
from zope.interface import implementer


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
