# -*- coding: utf-8 -*-
from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.utils import get_settings_for_language
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger(__name__)


class BaseVocabulary(object):
    def __call__(self, context):

        values = get_settings_for_language(field=self.field)
        if not values:
            return SimpleVocabulary([])

        terms = [SimpleTerm(value=x, token=x, title=x) for x in values]
        terms.insert(
            0, SimpleTerm(value="", token="", title="-- seleziona un valore --"),
        )

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class TipologieNotizia(BaseVocabulary):
    field = "tipologie_notizia"


@implementer(IVocabularyFactory)
class TipologieUnitaOrganizzativaVocabulary(BaseVocabulary):
    field = "tipologie_unita_organizzativa"


@implementer(IVocabularyFactory)
class TipologieDocumento(BaseVocabulary):
    field = "tipologie_documento"


@implementer(IVocabularyFactory)
class TipologiePersona(BaseVocabulary):
    field = "tipologie_persona"


@implementer(IVocabularyFactory)
class LeadImageDimension(BaseVocabulary):
    field = "lead_image_dimension"

    def __call__(self, context):

        values = api.portal.get_registry_record(
            self.field, interface=IDesignPloneSettings, default=[]
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
TipologieDocumentoFactory = TipologieDocumento()
TipologiePersonaFactory = TipologiePersona()
TipologieUnitaOrganizzativaVocabularyFactory = TipologieUnitaOrganizzativaVocabulary()
