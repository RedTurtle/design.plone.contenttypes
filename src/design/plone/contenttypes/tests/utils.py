# -*- coding: utf-8 -*-
"""
Helpers to run the same tests on Plone 6.0, 6.1 and 6.2.
"""

from importlib.metadata import version

import re


def _version_tuple(dist):
    return tuple(int(x) for x in re.match(r"(\d+)\.(\d+)", version(dist)).groups())


# Plone 6.1+: plone.app.discussion is no more a core add-on, so the default
# content-types (Document, Folder, News Item) do not have plone.allowdiscussion.
PLONE_61 = _version_tuple("Products.CMFPlone") >= (6, 1)
PLONE_62 = _version_tuple("Products.CMFPlone") >= (6, 2)

# plone.volto 5+ (Plone 6.1+):
# - preview_image and preview_caption are in their own "preview_image" fieldset
#   and not in "default";
# - Document, Event and News Item have also volto.preview_image_link (with
#   preview_image_link and preview_caption_link fields in the "preview_image"
#   fieldset) and volto.navtitle (nav_title field in "settings").
PLONE_VOLTO_5 = _version_tuple("plone.volto") >= (5, 0)

PREVIEW_FIELDS = ["preview_image", "preview_caption"]


def default_fieldset_fields(fields):
    """
    Expected fields of the "default" fieldset, given the Plone 6.0 ones.
    """
    if PLONE_VOLTO_5:
        return [x for x in fields if x not in PREVIEW_FIELDS]
    return fields


def fieldsets_ids(ids, preview_before="seo"):
    """
    Expected fieldsets ids, given the Plone 6.0 ones: with plone.volto 5+ there
    is also "preview_image", before preview_before (or at the end if None).
    """
    if not PLONE_VOLTO_5:
        return ids
    ids = list(ids)
    if preview_before:
        ids.insert(ids.index(preview_before), "preview_image")
    else:
        ids.append("preview_image")
    return ids


def get_fieldset_fields(schema, fieldset_id):
    """
    Return the fields of a fieldset from a @types response, looking it up by id
    instead of by position (it changes between Plone versions).
    """
    for fieldset in schema["fieldsets"]:
        if fieldset["id"] == fieldset_id:
            return fieldset["fields"]
    raise KeyError(
        "Fieldset {} not found in {}".format(
            fieldset_id, [x["id"] for x in schema["fieldsets"]]
        )
    )
