from plone.dexterity.browser import add
from plone.dexterity.browser import edit


class EditForm(edit.DefaultEditForm):
    def updateFields(self):
        super(EditForm, self).updateFields()
        self.fields["IRichTextBehavior.text"].field.title = u"Corpo news"
        self.fields["IRichTextBehavior.text"].field.required = True
    portal_type = 'News Item'


class AddForm(add.DefaultAddForm):
    def updateFields(self):
        super(AddForm, self).updateFields()
        self.fields["IRichTextBehavior.text"].field.title = u"Corpo news"
        self.fields["IRichTextBehavior.text"].field.required = True
        # import pdb; pdb.set_trace()
    portal_type = 'News Item'

class AddView(add.DefaultAddView):
    form = AddForm