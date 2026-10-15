from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class ArgomentiVocabulary:
    """ """

    def __call__(self, context):
        values = {x.Title for x in api.content.find(portal_type="Pagina Argomento")}
        values = sorted(list(values))
        terms = [
            SimpleTerm(value="", token="", title="-- seleziona un valore --")  # nosec
        ]  # nosec
        for value in values:
            terms.append(SimpleTerm(value=value, token=value, title=value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class ArgomentiUIDVocabulary:
    """ """

    def __call__(self, context):
        arguments = api.content.find(
            portal_type="Pagina Argomento", sort_on="sortable_title"
        )
        terms = [
            SimpleTerm(value="", token="", title="-- seleziona un valore --")  # nosec
        ]  # nosec
        for x in arguments:
            terms.append(SimpleTerm(value=x.UID, token=x.UID, title=x.Title))

        return SimpleVocabulary(terms)


ArgomentiVocabularyFactory = ArgomentiVocabulary()
ArgomentiUIDVocabularyFactory = ArgomentiUIDVocabulary()
