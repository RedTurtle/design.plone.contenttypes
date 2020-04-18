from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def servizioCreateHandler(servizio, event):
    """
    Complete content type Servizio setup on added event, generating 
    missing folders, fields, etc.

    @param servizio: Content item

    @param event: Event that triggers the method (onAdded event)
    """
    # if "luoghi" not in servizio.keys():
    #     luoghi = api.content.create(
    #         type="Document", title="Luoghi", container=servizio
    #     )
    # else:
    #     luoghi = servizio["luoghi"]
    #     luoghiConstraints = ISelectableConstrainTypes(luoghi)
    #     luoghiConstraints.setConstrainTypesMode(1)
    #     luoghiConstraints.setLocallyAllowedTypes(("Venue",))

    # if "sedi" not in servizio.keys():
    #     sedi = api.content.create(
    #         type="Document", title="Sedi", container=servizio
    #     )
    # else:
    #     sedi = servizio["sedi"]
    #     sediConstraints = ISelectableConstrainTypes(sedi)
    #     sediConstraints.setConstrainTypesMode(1)
    #     sediConstraints.setLocallyAllowedTypes(("Venue",))

    for folder in [
        {"id": "modulistica", "title": "Modulistica", "contains": ("File",)},
        {"id": "allegati", "title": "Allegati", "contains": ("File",)},
    ]:
        if folder["id"] not in servizio.keys():
            child = api.content.create(
                type="Document", title=folder["title"], container=servizio
            )
        else:
            child = servizio[folder["id"]]
            childConstraints = ISelectableConstrainTypes(child)
            childConstraints.setConstrainTypesMode(1)
            childConstraints.setLocallyAllowedTypes(folder["contains"])
