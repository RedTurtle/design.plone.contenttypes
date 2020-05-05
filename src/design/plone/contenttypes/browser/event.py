# -*- coding: utf-8 -*-
from plone.dexterity.browser import add
from plone.dexterity.browser import edit


class EditForm(edit.DefaultEditForm):
    # def updateFields(self):
    #     super(EditForm, self).updateFields()
    #     source = CatalogSource(portal_type='Luogo')
    #     print(source)

    portal_type = 'Event'


class AddForm(add.DefaultAddForm):
    def updateFields(self):
        super(AddForm, self).updateFields()

    portal_type = 'Event'


class AddView(add.DefaultAddView):
    form = AddForm
