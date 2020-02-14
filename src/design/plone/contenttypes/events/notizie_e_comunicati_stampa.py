from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces import ISelectableConstrainTypes


def notiziaCreateHandler(notizia, event):
    """
    Complete content type notizia setup on added event, generating
    missing folders, fields, etc.

    @param notizia: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    # persone = _createObjectByType("Folder", notizia, "persone")
    # persone.title = "Persone"
    # persone.reindexObject(idxs=["Title"])
    # constraintsPersone = ISelectableConstrainTypes(persone)
    # constraintsPersone.setConstrainTypesMode(1)
    # scegliere le restrizioni
    # constraintsPersone.setLocallyAllowedTypes(("Persona",))

    # luogo = _createObjectByType("Folder", notizia, "luogo")
    # luogo.title = "Luoghi"
    # luogo.reindexObject(idxs=["Title"])
    # constraintsLuoghi = ISelectableConstrainTypes(luogo)
    # constraintsLuoghi.setConstrainTypesMode(1)
    # # scegliere le restrizioni
    # constraintsLuoghi.setLocallyAllowedTypes(("Venue",))

    multimedia = _createObjectByType("Document", notizia, "multimedia")
    multimedia.title = "Multimedia"
    multimedia.reindexObject(idxs=["Title"])
    constraintsMultimedia = ISelectableConstrainTypes(multimedia)
    constraintsMultimedia.setConstrainTypesMode(1)
    # scegliere le restrizioni
    constraintsMultimedia.setLocallyAllowedTypes(("File", "Image"))

    # ci serve? In teoria la macrobuca dovrebbe essere la sezione "Documenti"
    documentiAllegati = _createObjectByType(
        "Document", notizia, "documenti-allegati"
    )
    documentiAllegati.title = "Documenti allegati"
    documentiAllegati.reindexObject(idxs=["Title"])
    constraintsDocumentiAllegati = ISelectableConstrainTypes(documentiAllegati)
    constraintsDocumentiAllegati.setConstrainTypesMode(1)
    # scegliere le restrizioni
    constraintsDocumentiAllegati.setLocallyAllowedTypes(("File", "Image"))
