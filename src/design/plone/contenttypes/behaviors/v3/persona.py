# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IPersonaBehavior(model.Schema):
    # Questo campo per direttive e richieste viene nascosto nella form
    # Lo si tiene perche si vuole evitare di perder dati tra le migrazioni
    # e magari non poter piu' usare la feature collegata, ossia
    # la check persone, in quanto relazioni potrebbero rompersi o perdersi
    organizzazione_riferimento = RelationList(
        title=_(
            "organizzazione_riferimento_label",
            default="Organizzazione di riferimento",
        ),
        description=_(
            "organizzazione_riferimento_help",
            default="Seleziona una lista di organizzazioni a cui la persona"
            " appartiene.",
        ),
        value_type=RelationChoice(
            title=_("Organizzazione di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        default=[],
        required=False,
    )

    form.omitted("organizzazione_riferimento")

    incarichi_persona = RelationList(
        title=_(
            "incarichi_label",
            default="Incarichi",
        ),
        description=_(
            "incarichi_help",
            default="Seleziona l'incarico corrente della persona.",
        ),
        value_type=RelationChoice(
            title=_("Incarichi"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        default=[],
        required=False,
    )

    curriculum_vitae = field.NamedBlobFile(
        title=_("curriculum_vitae_label", default="Curriculum vitae"),
        required=False,
        description=_(
            "curriculum_vitae_help",
            default="Allega un file contenente il curriculum vitae della persona. "
            "Se ha più file da allegare, utilizza questo campo per quello principale "
            'e gli altri mettili dentro alla cartella "Curriculum vitae" che troverai dentro alla Persona.',  # noqa
        ),
    )

    # custom widgets
    form.widget(
        "organizzazione_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    form.widget(
        "incarichi_persona",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Incarico"],
        },
    )

    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "organizzazione_riferimento",
            "incarichi_persona",
        ],
    )

    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=["curriculum_vitae"],
    )

    form.order_before(incarichi_persona="competenze")


@implementer(IPersonaBehavior)
@adapter(IDexterityContent)
class PersonaBehavior(object):
    """ """

    def __init__(self, context):
        self.context = context
