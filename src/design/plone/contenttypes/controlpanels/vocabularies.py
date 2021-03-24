# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form
from zope.schema import List, TextLine, SourceText
from zope.interface import Interface


class IVocabulariesControlPanel(Interface):
    tipologie_notizia = List(
        title=_(u"Tipologie Notizia"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di una"
            " Notizia; inserisci i valori uno per riga"
        ),
        required=True,
        default=["Avviso", "Comunicato stampa", "Novità"],
        value_type=TextLine(),
    )

    tipologie_unita_organizzativa = List(
        title=_(u"Tipologie Unità Organizzativa"),
        description=_(
            "Inserisci i valori utilizzabili per le tipologie di un'"
            " Unità Organizzativa; inserisci i valori uno per riga"
        ),
        required=True,
        default=["Politica", "Amministrativa", "Altro"],
        value_type=TextLine(),
    )

    tipologie_documento = List(
        title=_(u"Tipologie Documento"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di"
            " un Documento; inserisci i valori uno per riga"
        ),
        required=True,
        default=[
            "Accordi tra enti",
            "Atti normativi",
            "Dataset",
            "Documenti (tecnici) di supporto",
            "Documenti albo pretorio",
            "Documenti attività politica",
            "Documenti funzionamento interno",
            "Istanze",
            "Modulistica",
        ],
        value_type=TextLine(),
    )

    tipologie_persona = List(
        title=_(u"Tipologie Persona"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di"
            " una Persona; inserisci i valori uno per riga"
        ),
        required=True,
        default=[
            "Amministrativa",
            "Politica",
            "Altro tipo",
        ],
        value_type=TextLine(),
    )

    lead_image_dimension = List(
        title=_(u"Indicare le dimensioni delle lead image dei contenuti"),
        description=_(
            u"Inserire le dimensioni nella forma di esempio PortalType|900x900"
        ),
        required=True,
        default=[
            "News Item|1920x600",
            "Servizio|1920x600",
            "UnitaOrganizzativa|1920x600",
            "Persona|180x100",
        ],
        value_type=TextLine(),
    )

    search_sections = SourceText(
        title=_("search_sections_label", default="Sezioni ricerca"),
        description=_(
            "search_sections_help",
            default="Inserire una lista di sezioni per la ricerca.",
        ),
        default="",
        required=False,
    )


class VocabulariesControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IVocabulariesControlPanel
    id = "design-plone-vocabularies-control-panel"
    label = _(u"Vocabolari")


VocabulariesControlPanelView = layout.wrap_form(
    VocabulariesControlPanelForm, ControlPanelFormWrapper
)
VocabulariesControlPanelView.label = _(u"Vocabolari")
