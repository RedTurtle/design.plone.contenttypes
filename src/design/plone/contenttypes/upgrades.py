# -*- coding: utf-8 -*-
from plone import api


DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"


# def import_registry(registry_id, dependencies=False):
#     setup_tool = api.portal.get_tool("portal_setup")
#     setup_tool.runImportStepFromProfile(
#         DEFAULT_PROFILE, registry_id, run_dependencies=dependencies
#     )


def import_types_registry(context):
    "Import types registry configuration"
    import_registry("typeinfo")


def update_profile(context, profile):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile)


def add_indexes_to_catalog(index_to_add, indextype):
    pc = api.portal.get_tool("portal_catalog")
    indexes = pc.indexes()
    added = 0

    for index in index_to_add:
        if index not in indexes:
            pc.addIndex(name=index, type=indextype)
            added = 1

    if added:
        pc.refreshCatalog()


def upgrade_rolemap(context):
    update_profile(context, "rolemap")


def add_index_to_search_dashboard(context):
    add_indexes_to_catalog([], "KeywordIndex")


def import_portlets(context):
    update_profile(context, "portlets")


def import_registry(context):
    update_profile(context, "plone.app.registry")


def import_controlpanel(context):
    update_profile(context, "controlpanel")


def from_x_to_1004(context):
    import_registry(context)
    import_controlpanel(context)

