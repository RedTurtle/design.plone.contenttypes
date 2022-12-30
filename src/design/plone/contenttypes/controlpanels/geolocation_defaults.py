# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form
from zope.interface import Interface
from zope.schema import TextLine


class IGeolocationDefaults(Interface):
    street = TextLine(
        title=_("Via"),
        required=False,
        default="Via Liszt, 21",
    )
    zip_code = TextLine(
        title=_("CAP"),
        required=False,
        default="00144",
    )
    city = TextLine(
        title=_("Città"),
        required=False,
        default="Roma",
    )
    country = TextLine(
        title=_("Nazione"),
        required=False,
        default="{'title': 'Italia','token': '380',}",
    )
    geolocation = TextLine(
        title=_("Coordinate"),
        required=True,
        default="{'latitude': 41.8337833,'longitude': 12.4677863,}",
    )


class GeolocationDefaultControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IGeolocationDefaults
    id = "geolocation-defaults"
    label = _("Geolocation default")


GeolocationDefaultControlPanellView = layout.wrap_form(
    GeolocationDefaultControlPanelForm, ControlPanelFormWrapper
)
GeolocationDefaultControlPanellView.label = _("Geolocation default")
