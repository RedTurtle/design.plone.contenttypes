# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.services.content.add import FolderPost

import json


class DocumentoPost(FolderPost):
    def reply(self):
        data = json_body(self.request)
        if data.get("@type", "") == "Image":
            data["@type"] = "Modulo"
            data["file_principale"] = data["image"]
            del data["image"]
        elif data.get("@type", "") == "File":
            data["@type"] = "Modulo"
            data["file_principale"] = data["file"]
            del data["file"]
        self.request["BODY"] = json.dumps(data)
        return super(DocumentoPost, self).reply()
