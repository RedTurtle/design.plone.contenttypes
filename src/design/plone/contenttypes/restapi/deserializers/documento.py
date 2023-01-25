# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.documento import IDocumento
from plone.restapi.behaviors import IBlocks
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.dxcontent import DeserializeFromJson
from plone.restapi.indexers import SearchableText_blocks
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


TITLE_MAX_LEN = 160
DESCRIPTION_MAX_LEN = 160
EMPTY_BLOCK_MARKER = {"@type": "text"}
MANDATORY_RICH_TEXT_FIELDS = [
    # "descrizione_estesa",
    "formati_disponibili",
]


def new_error(message):
    return {"error": "ValidationError", "message": message}


def text_in_block(blocks):
    @implementer(IBlocks)
    class FakeObject(object):
        """
        We use a fake object to use SearchableText Indexer
        """

        def Subject(self):
            return ""

        def __init__(self, blocks, blocks_layout):
            self.blocks = blocks
            self.blocks_layout = blocks_layout
            self.id = ""
            self.title = ""
            self.description = ""

    if not blocks:
        return None

    fakeObj = FakeObject(blocks.get("blocks", ""), blocks.get("blocks_layout", ""))
    return SearchableText_blocks(fakeObj)()


@implementer(IDeserializeFromJson)
@adapter(IDocumento, Interface)
class DeserializeDocumentoFromJson(DeserializeFromJson):
    def __call__(
        self, validate_all=False, data=None, create=False
    ):  # noqa: ignore=C901

        if data is None:
            data = json_body(self.request)

        method = self.request.get("method")
        is_post = method == "POST"
        is_patch = method == "PATCH"
        errors = []

        title = data.get("title")
        description = data.get("description")

        if is_post:
            # Title validation
            if not title:
                errors.append(new_error("Il titolo del servizio è obbligatorio"))
            elif len(title) > TITLE_MAX_LEN:
                errors.append(
                    new_error(
                        "Il titolo può avere una lunghezza di massimo {} caratteri".format(  # noqa
                            TITLE_MAX_LEN
                        )
                    )
                )

            # description validation
            if not description:
                errors.append(new_error("La descrizione del servizio è obbligatorio"))
            elif len(description) > DESCRIPTION_MAX_LEN:
                errors.append(
                    new_error(
                        "La descrizione del servizio deve avere una lunghezza di massimo {} caratteri".format(  # noqa
                            DESCRIPTION_MAX_LEN
                        )
                    )
                )

            for field in MANDATORY_RICH_TEXT_FIELDS:
                if field not in data:
                    errors.append(new_error("Il campo {} è obbligatorio".format(field)))
                elif field in data and not text_in_block(data.get(field)):
                    errors.append(new_error("Il campo {} è obbligatorio".format(field)))

        if is_patch:
            # Title validation
            if "title" in data and not title:
                errors.append(new_error("Il titolo del servizio è obbligatorio"))
            if title and len(title) > TITLE_MAX_LEN:
                errors.append(
                    new_error(
                        "Il titolo può avere una lunghezza di massimo {} caratteri".format(  # noqa
                            TITLE_MAX_LEN
                        )
                    )
                )
            # description validation
            if "description" in data and not description:
                errors.append(new_error("La descrizione del servizio è obbligatorio"))
            if description and len(description) > DESCRIPTION_MAX_LEN:
                errors.append(
                    new_error(
                        "La descrizione del servizio deve avere una lunghezza di massimo {} caratteri".format(  # noqa
                            DESCRIPTION_MAX_LEN
                        )
                    )
                )
            if "description" not in data and not self.context.description:
                errors.append(new_error("La descrizione del servizio è obbligatorio"))

            for field in MANDATORY_RICH_TEXT_FIELDS:
                if field in data and not text_in_block(data.get(field)):
                    errors.append(new_error("Il campo {} è obbligatorio".format(field)))
                # Se siamo nella patch siamo in modifica. Se siamo in modifica e siamo
                # su un sito che ha avuto upgrade alla versione pnrr può essere che
                # dei campi obbligatori un tempo non lo fossero e quindi arriviamo
                # fino a qui
                if field not in data and not text_in_block(
                    getattr(self.context, field)
                ):
                    errors.append(new_error("Il campo {} è obbligatorio".format(field)))

        if errors:
            raise BadRequest(errors)
        return super(DeserializeDocumentoFromJson, self).__call__(
            validate_all=False, data=data, create=False
        )
