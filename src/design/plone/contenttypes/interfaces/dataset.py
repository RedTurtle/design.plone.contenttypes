# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.namedfile import field
from plone.supermodel import model
from zope import schema


class IDataset(model.Schema):
    """ Marker interface for Dataset
    """

    # TODO: aggiungere tassonomia e vocabolario rilevante fornito nelle linee guida  # noqa
    temi = schema.Choice(
        title=_(u"temi", default=u"Temi"),
        vocabulary="design.plone.contenttypes.temi_dataset",
        required=True,
    )

    # TODO: identificativo dataset

    distribuzione = RichText(
        title=_(u"distribuzione", default=u"Distribuzione"), required=True
    )

    licenza = schema.TextLine(
        title=_(u"licenza", default=u"Licenza"), required=True
    )

    dataset = field.NamedBlobFile(
        title=_(u"dataset", default=u"Dataset"), required=True
    )

    titolare = schema.TextLine(
        title=_(u"titolare", default=u"Titolare"), required=True
    )

    frequenza_aggiornamento = schema.TextLine(
        title=_(
            u"frequenza_aggiornamento", default=u"Frequenza di aggiornamento"
        ),
        required=True,
    )
