# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
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

    unita_amministrativa_responsabile = RelationList(
        title=_(
            u"unita_amministrativa_responsabile",
            default=u"Unità amministrativa responsabile",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Unità amministrativa responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "unita_amministrativa_responsabile_help",
            default="Seleziona la lista delle unità amministrative"
            " responsabili di questo argomento.",
        ),
    )
    form.widget(
        "unita_amministrativa_responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
            # "basePath": "/amministrazione",
        },
    )

    box_aiuto = RichText(
        title=_(u"box_aiuto", default=u"Box di aiuto"),
        required=False,
        description=_(
            "box_aiuto_help",
            default="Eventuali contatti di supporto all'utente.",
        ),
    )
