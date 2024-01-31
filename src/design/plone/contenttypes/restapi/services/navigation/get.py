from design.plone.contenttypes.controlpanels.settings import IDesignPloneSettings
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from plone.restapi.services.navigation.get import Navigation as BaseNavigation
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, IDesignPloneContenttypesLayer)
class Navigation(BaseNavigation):
    def __call__(self, expand=False):
        result = super().__call__(expand=expand)
        show_dynamic_folders_in_footer = api.portal.get_registry_record(
            "show_dynamic_folders_in_footer",
            interface=IDesignPloneSettings,
            default=False,
        )
        result["navigation"]["show_in_footer"] = show_dynamic_folders_in_footer
        return result


class NavigationGet(Service):
    def reply(self):
        navigation = Navigation(self.context, self.request)
        return navigation(expand=True)["navigation"]
