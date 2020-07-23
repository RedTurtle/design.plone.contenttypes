# -*- coding: utf-8 -*-
from design.plone.contenttypes.patches.baseserializer import (
    patch_base_serializer,
    patch_base_folder_serializer,
)
import logging

logger = logging.getLogger("design.plone.contenttypes.patches")

logger.info(
    "Patching plone.restapi.serializer.dxcontent.SerializeToJson._call__"
)
logger.info(
    "Patching plone.restapi.serializer.dxcontent.SerializeFolderToJson._call__"
)
patch_base_serializer()
patch_base_folder_serializer()
