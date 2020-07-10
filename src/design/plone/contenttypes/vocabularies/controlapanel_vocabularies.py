# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.vocabularies import (
    IVocabulariesControlPanel,
)
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class BaseVocabulary(object):
    def __call__(self, context):

        values = api.portal.get_registry_record(
            self.field, interface=IVocabulariesControlPanel, default=[]
        )
        if not values:
            return SimpleVocabulary([])

        terms = [SimpleTerm(value=x, token=x, title=x) for x in values]
        terms.insert(
            0,
            SimpleTerm(value="", token="", title="-- seleziona un valore --"),
        )

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class TipologieNotizia(BaseVocabulary):
    field = "tipologie_notizia"


@implementer(IVocabularyFactory)
class TipologieUnitaOrganizzativaVocabulary(BaseVocabulary):
    field = "tipologie_unita_organizzativa"


@implementer(IVocabularyFactory)
class LeadImageDimension(BaseVocabulary):
    field = "lead_image_dimension"

    def __call__(self, context):

        values = api.portal.get_registry_record(
            self.field, interface=IVocabulariesControlPanel, default=[]
        )
        if not values:
            return SimpleVocabulary([])

        terms = []
        for value in values:
            token, title = value.split("|")
            terms.append(SimpleTerm(value=token, token=token, title=title))
        return SimpleVocabulary(terms)


LeadImageDimensionFactory = LeadImageDimension()
TipologieNotiziaFactory = TipologieNotizia()
TipologieUnitaOrganizzativaVocabularyFactory = (
    TipologieUnitaOrganizzativaVocabulary()
)
