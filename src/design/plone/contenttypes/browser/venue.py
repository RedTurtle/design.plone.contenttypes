from plone.dexterity.browser import add
from plone.dexterity.browser import edit


class EditForm(edit.DefaultEditForm):
    def updateFields(self):
        super(EditForm, self).updateFields()
        self.fields = self.fields.omit('notes')
    portal_type = 'Venue'


class AddForm(add.DefaultAddForm):
    def updateFields(self):
        super(AddForm, self).updateFields()
        self.fields = self.fields.omit('notes')
    portal_type = 'Venue'

class AddView(add.DefaultAddView):
    form = AddForm