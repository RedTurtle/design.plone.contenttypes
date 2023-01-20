# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces import IDesignPloneContentType
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


# TODO: migration script for these commented fields towards PDC
# contact_info
# Probabilmente non possibile trattandosi di un campo a blocchi
# preferirei si arrangiassero le redazioni. Altrimenti si defaulta
# ad un tipo a caso + tutto il testo e poi si arrangiano comunque
class IUnitaOrganizzativa(model.Schema, IDesignPloneContentType):
    """Marker interface for content type UnitaOrganizzativa"""

    competenze = BlocksField(
        title=_("uo_competenze_label", default="Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=True,
    )

    legami_con_altre_strutture = RelationList(
        title=_(
            "legami_altre_strutture_label", default="Strutture o uffici di riferimento"
        ),
        default=[],
        description=_(
            "legami_con_altre_strutture_help",
            default="Selezionare la lista di strutture e/o uffici collegati"
            " a questa unità organizzativa.",
        ),
        value_type=RelationChoice(
            title=_("Struttura"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    responsabile = RelationList(
        title=_("responsabile_label", default="Responsabile"),
        value_type=RelationChoice(
            title=_("Responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "responsabile_help",
            default="Selezionare il/i responsabile/i della struttura.",
        ),
        default=[],
        required=False,
    )

    assessore_riferimento = RelationList(
        title="Assessore di riferimento",
        # vocabolario di riferimento sara' dinamico con i content type
        # persona presenti all'interno della macro Amministrazione"
        value_type=RelationChoice(
            title=_("Assessore di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "assessore_riferimento_help",
            default="Inserire l'assessore di riferimento della struttura,"
            " se esiste.",
        ),
        required=False,
        default=[],
    )

    # vocabolario di riferimento sara' dinamico con i content type persona
    persone_struttura = RelationList(
        title=_(
            "persone_struttura_label", default="Persone che compongono la struttura"
        ),
        default=[],
        value_type=RelationChoice(
            title=_("Persone della struttura"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_struttura_help",
            default="Seleziona la lista delle persone che compongono" " la struttura.",
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

    sedi_secondarie = RelationList(
        title=_("sedi_secondarie_label", default="Altre sedi"),
        default=[],
        description=_(
            "sedi_secondarie_help",
            default="Seleziona una lista di eventuali contenuti di tipo Luogo"
            " che sono sedi secondarie di questa struttura. "
            "Per queste sedi non sarà possibile sovrascrivere i dati. "
            "Nel caso servano informazioni diverse, è possibile usare il campo"
            " sottostante.",
        ),
        value_type=RelationChoice(
            title=_("Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
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

    #  custom widgets
    form.widget(
        "documenti_pubblici",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Documento"],
        },
    )
    form.widget(
        "persone_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"], "maximumSelectionSize": 50},
    )
    form.widget(
        "legami_con_altre_strutture",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )
    form.widget(
        "assessore_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )
    form.widget(
        "sede",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 1, "selectableTypes": ["Venue"]},
    )
    form.widget(
        "sedi_secondarie",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Venue"],
            # "basePath": "/servizi",
        },
    )

    # custom fieldsets and order
    model.fieldset(
        "cosa_fa",
        label=_("cosa_fa_label", default="Competenze"),
        fields=["competenze"],
    )
    model.fieldset(
        "struttura",
        label=_("struttura_label", default="Struttura"),
        fields=[
            "legami_con_altre_strutture",
            "responsabile",
            "assessore_riferimento",
        ],
    )
    model.fieldset(
        "persone",
        label=_("persone_label", default="Persone"),
        fields=["persone_struttura"],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["sede", "sedi_secondarie"],
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["documenti_pubblici"],
    )

    form.order_after(sedi_secondarie="IContattiUnitaOrganizzativa.orario_pubblico")
    form.order_after(documenti_pubblici="relatedItems")
    # form.order_after(contact_info="sedi_secondarie")

    # SearchableText indexers
    textindexer.searchable("competenze")
    textindexer.searchable("assessore_riferimento")
    textindexer.searchable("responsabile")
