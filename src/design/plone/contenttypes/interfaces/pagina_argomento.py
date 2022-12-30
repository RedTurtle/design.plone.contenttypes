# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.schema import TextLine


class IPaginaArgomento(model.Schema, IDesignPloneContentType):
    """Marker interface for PaginaArgomento"""

    ulteriori_informazioni = RichText(
        title=_("ulteriori_informazioni", default="Ulteriori informazioni"),
        description=_(
            "ulteriori_informazioni_help",
            default="Ulteriori informazioni non contemplate" " dai campi precedenti.",
        ),
        required=False,
    )

    icona = TextLine(
        title=_("icona", default="Icona"),
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
            "unita_amministrative_responsabili",
            default="Unità amministrative responsabili",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Unità amministrative responsabili"),
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

    model.fieldset(
        "informazioni",
        label=_("informazioni_label", default="Ulteriori informazioni"),
        fields=["ulteriori_informazioni"],
    )

    # SearchableText fields
    textindexer.searchable("ulteriori_informazioni")
    textindexer.searchable("unita_amministrative_responsabili")
