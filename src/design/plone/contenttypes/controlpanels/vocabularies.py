# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form
from zope.schema import List, TextLine
from zope.interface import Interface


class IVocabulariesControlPanel(Interface):
    tipologie_notizia = List(
        title=_(u"Tipologie notizia"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di"
            " notizia; inserisci i valori uno per riga"
        ),
        required=True,
        default=[],
        value_type=TextLine(),
    )

    tipologie_unita_organizzativa = List(
        title=_(u"Tipologie unita organizzativa"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di"
            " unita organizzativa; inserisci i valori uno per riga"
        ),
        required=True,
        default=[],
        value_type=TextLine(),
    )

    lead_image_dimension = List(
        title=_(u"Indicare le dimensioni delle lead image dei contenuti"),
        description=_(
            u"Inserire le dimensioni nella forma di esempio PortalType|900x900"
        ),
        required=True,
        default=[],
        value_type=TextLine(),
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
