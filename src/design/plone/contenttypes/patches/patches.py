from collective.taxonomy.vocabulary import Vocabulary


def eea_api_taxonomy_taxonomy_call(self, context):

    if not self.data:
        return Vocabulary(self.name, {}, {}, {}, 2)

    request = getattr(context, "REQUEST", None)
    language = self.getCurrentLanguage(request)
    return self.makeVocabulary(language)
