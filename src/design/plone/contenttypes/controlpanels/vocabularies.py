from z3c.form import form
from Products.Five import BrowserView
from zope.interface import Interface
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from design.plone.contenttypes import _


class IVocabulariesControlPanel(Interface):
    news_tipologia_notizia = schema.Text(
        title=_(u'Tipologie notizia'),
        description=_(u"Inserisci i valori utilizzabili per le tipologie di"
            " notizia; inserisci i valori uno per riga"),
        required=True
    )


class VocabulariesControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IVocabulariesControlPanel
    id = 'design-plone-vocabularies-control-panel'
    label = _(u'Vocabolari')


VocabulariesControlPanelView = layout.wrap_form(
        VocabulariesControlPanelForm,
        ControlPanelFormWrapper)
VocabulariesControlPanelView.label = _(u"Vocabolari")

