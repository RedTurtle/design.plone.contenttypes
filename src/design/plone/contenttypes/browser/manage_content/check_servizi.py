from design.plone.contenttypes import _
from plone import api
from plone.z3cform.layout import wrap_form
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


class ISearchForm(Interface):
    """
    Form to search Servizio by path
    """

    path = schema.TextLine(
        title=_(
            "licenza_distribuzione_label",
            default="Seleziona il percorso sotto il quale cercare",
        ),
        required=False,
    )


@implementer(ISearchForm)
class CheckServizi(form.Form):

    ignoreContext = True
    # template = ViewPageTemplateFile("templates/check_servizi.pt")
    prefix = ""
    brains = []
    fields = field.Fields(ISearchForm)
    method = "GET"

    def search_servizi(self):
        pc = api.portal.get_tool("portal_catalog")
        query = {"portal_type": "Servizio", "sort_on": "sortable_title"}
        if self.request.form.get("widgets.path") and self.request.form.get(
            "buttons.action_search"
        ):
            path = self.request.form.get("widgets.path")
            prefix = api.portal.get().getId()
            if not path.startswith(f"/{prefix}"):
                path = f"/{prefix}/{path}"
            query["path"] = {"query": path}
        brains = pc(**query)
        servizi = [brain.getObject() for brain in brains]
        results = []
        for servizio in servizi:
            results.append(
                {
                    "title": servizio.title,
                    "url": "/".join(servizio.getPhysicalPath()),
                    "breadcrumbs": getMultiAdapter(
                        (servizio, self.request), name="breadcrumbs_view"
                    ).breadcrumbs(),
                }
            )
        return results

    def updateWidgets(self):
        super(CheckServizi, self).updateWidgets()
        for k, v in self.request.form.items():
            if k in self.widgets:
                self.widgets[k].value = v

    @button.buttonAndHandler(_("action_search", default="Cerca"))
    def action_search(self, action):
        """
        Search in prenotazioni SearchableText
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

    @button.buttonAndHandler(_("move_back_message", default="Reset"))
    def action_cancel(self, action):
        """
        Cancel and go back to the week view
        """
        target = self.context.absolute_url() + "/check_servizi"
        return self.request.response.redirect(target)


WrappedCheckServiziForm = wrap_form(CheckServizi)
