# -*- coding: utf-8 -*-
from design.plone.contenttypes.patches.baseserializer import (
    patch_base_folder_serializer,
)
from design.plone.contenttypes.patches.baseserializer import patch_base_serializer
from design.plone.contenttypes.patches.collective_volto_formsupport import (
    patch_FormDataExportGet_get_data,
)
from design.plone.contenttypes.patches.collective_volto_formsupport import (
    patch_FormDataStore_methods,
)
from design.plone.contenttypes.patches.collective_volto_formsupport import (
    patch_SubmitPost_reply,
)

import logging


logger = logging.getLogger("design.plone.contenttypes.patches")

logger.info("Patching plone.restapi.serializer.dxcontent.SerializeToJson._call__")
logger.info("Patching plone.restapi.serializer.dxcontent.SerializeFolderToJson._call__")
patch_base_serializer()
patch_base_folder_serializer()

patch_FormDataExportGet_get_data()
patch_SubmitPost_reply()
patch_FormDataStore_methods()
