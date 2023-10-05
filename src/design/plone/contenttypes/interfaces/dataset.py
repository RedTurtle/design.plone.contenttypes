# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from plone.namedfile import field
from plone.supermodel import model
from zope import schema


class IDataset(model.Schema):
    """Marker interface for Dataset"""

    # TODO: identificativo dataset

    distribuzione = BlocksField(
        title=_("distribuzione", default="Distribuzione"), required=True
    )

    licenza = schema.TextLine(title=_("licenza", default="Licenza"), required=True)

    dataset = field.NamedBlobFile(title=_("dataset", default="Dataset"), required=True)

    titolare = schema.TextLine(title=_("titolare", default="Titolare"), required=True)

    frequenza_aggiornamento = schema.TextLine(
        title=_("frequenza_aggiornamento", default="Frequenza di aggiornamento"),
        required=True,
    )
