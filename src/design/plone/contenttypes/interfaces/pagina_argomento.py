# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.schema import TextLine


class IPaginaArgomento(model.Schema):
    """ Marker interface for PaginaArgomento
    """

    icona = TextLine(
        title=_(u"icona", default=u"Icona"),
        description=_(
            "icona_help",
            default="Puoi selezionare un’icona fra quelle proposte nel menu a"
            " tendina oppure puoi scrivere/incollare nel campo di testo il"
            " nome di un’icona di fontawsome 5",
        ),
        required=False,
    )

    unita_amministrative_responsabili = RelationList(
        title=_(
            u"unita_amministrative_responsabili",
            default=u"Unità amministrative responsabili",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Unità amministrative responsabili"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "unita_amministrative_responsabili_help",
            default="Seleziona la lista delle unità amministrative"
            " responsabili di questo argomento.",
        ),
    )
    form.widget(
        "unita_amministrative_responsabili",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    form.order_after(
        unita_amministrative_responsabili="ILeadImageBehavior.image_caption"
    )

    # SearchableText fields
    dexteritytextindexer.searchable("unita_amministrative_responsabili")
