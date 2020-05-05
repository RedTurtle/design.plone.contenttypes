# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form
from zope import schema
from zope.interface import Interface


class IVocabulariesControlPanel(Interface):
    news_tipologia_notizia = schema.Text(
        title=_(u"Tipologie notizia"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di"
            " notizia; inserisci i valori uno per riga"
        ),
        required=True,
    )
    tipologia_unita_organizzativa = schema.Text(
        title=_(u"Tipologie unita organizzativa"),
        description=_(
            u"Inserisci i valori utilizzabili per le tipologie di"
            " unita organizzativa; inserisci i valori uno per riga"
        ),
        required=True,
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
