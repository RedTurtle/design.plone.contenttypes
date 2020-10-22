# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class TipologieDocumento(object):
    """"""

    def __call__(self, context):
        values = [
            _("Documenti albo pretorio"),
            _("Modulistica"),
            _("Documenti funzionamento interno"),
            _("Atti normativi"),
            _("Accordi tra enti"),
            _("Documenti attività politica"),
            _("Documenti (tecnici) di supporto"),
            _("Istanze"),
            _("Dataset"),
        ]
        terms = [
            SimpleTerm(
                value="", token="", title=_("-- seleziona un valore --")
            )
        ]
        terms.extend([SimpleTerm(value=x, token=x, title=x) for x in values])

        return SimpleVocabulary(terms)


TipologieDocumentoFactory = TipologieDocumento()
