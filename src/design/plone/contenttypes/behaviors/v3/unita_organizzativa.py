# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IUnitaOrganizzativaBehavior(model.Schema):
    competenze = BlocksField(
        title=_("uo_competenze_label", default="Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=True,
    )

    sede = RelationList(
        title=_("sede_label", default="Sede principale"),
        default=[],
        description=_(
            "sede_help",
            default="Seleziona il Luogo in cui questa struttura ha sede. "
            "Se non è presente un contenuto di tipo Luogo a cui far "
            "riferimento, puoi compilare i campi seguenti. Se selezioni un "
            "Luogo, puoi usare comunque i campi seguenti per sovrascrivere "
            "alcune informazioni.",
        ),
        value_type=RelationChoice(
            title=_("Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=True,
    )

    documenti_pubblici = RelationList(
        title=_("documenti_pubblici_label", default="Documenti pubblici"),
        default=[],
        description=_(
            "documenti_pubblici_help",
            default="Documenti pubblici importanti, collegati a questa Unità Organizzativa",  # noqa
        ),
        value_type=RelationChoice(
            title=_("Documenti pubblici"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    form.widget(
        "sede",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 1, "selectableTypes": ["Venue"]},
    )
    form.widget(
        "documenti_pubblici",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Documento"],
        },
    )

    form.order_after(documenti_pubblici="relatedItems")
    form.order_before(sede="sedi_secondarie")

    model.fieldset(
        "cosa_fa",
        label=_("cosa_fa_label", default="Competenze"),
        fields=["competenze"],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["sede"],
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["documenti_pubblici"],
    )

    textindexer.searchable("competenze")


@implementer(IUnitaOrganizzativaBehavior)
@adapter(IDexterityContent)
class UnitaOrganizzativaBehavior(object):
    """ """

    def __init__(self, context):
        self.context = context
