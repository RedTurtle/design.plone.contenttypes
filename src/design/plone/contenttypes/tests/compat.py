"""Differences in the Plone core schemas between Plone versions.

Plone 6.1+ (plone.volto 5+) moves the preview image fields in their own
"preview_image" fieldset, replaces ``plone.allowdiscussion`` with
``volto.navtitle`` in the settings and enables ``volto.preview_image_link``.
"""

from importlib.metadata import version

PLONE_VERSION = tuple(int(x) for x in version("Products.CMFPlone").split(".")[:2])
PLONE_61_PLUS = PLONE_VERSION >= (6, 1)
PLONE_61 = PLONE_VERSION == (6, 1)

PREVIEW_FIELDS = ("preview_image", "preview_caption")
# 1 more fieldset in Plone 6.1+
PREVIEW_FIELDSET_COUNT = 1 if PLONE_61_PLUS else 0


def without_preview_fields(fields):
    """The default fieldset does not contain the preview fields in Plone 6.1+."""
    if not PLONE_61_PLUS:
        return fields
    return [x for x in fields if x not in PREVIEW_FIELDS]


def with_preview_fieldset(ids, before="seo", after=False):
    """Plone 6.1+ has a "preview_image" fieldset, usually before the "seo" one."""
    if not PLONE_61_PLUS:
        return ids
    ids = list(ids)
    ids.insert(ids.index(before) + (1 if after else 0), "preview_image")
    return ids


def fieldset_fields(resp, fieldset_id):
    """Fields of a fieldset, searched by id because its position depends on the Plone version."""
    return [x for x in resp["fieldsets"] if x["id"] == fieldset_id][0]["fields"]
