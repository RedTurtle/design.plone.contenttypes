# -*- coding: utf-8 -*-
from plone import api
from Products.Five import BrowserView
from six import StringIO

import csv


class View(BrowserView):
    def __call__(self, *args, **kwargs):
        self.request.response.setHeader("Content-type", "application/csv")
        self.request.response.setHeader(
            "Content-dispsition", "attachment; filename=incarichi.csv"
        )

        sbuf = StringIO()

        fieldnames = ["nome", "incarico", "data inizio", "tipo", "url"]
        writer = csv.DictWriter(sbuf, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        brains = api.content.find(portal_type="Persona")
        for brain in brains:
            ruolo = brain.ruolo and brain.ruolo[0] or ""
            persona = brain.getObject()
            incarico_obj = (
                persona.incarichi_persona
                and persona.incarichi_persona[0].to_object
                or None
            )
            data_inizio = incarico_obj and incarico_obj.data_inizio_incarico or ""
            if data_inizio:
                data_inizio = data_inizio.strftime("%d/%m/%Y")
            tipo_incarico = incarico_obj and incarico_obj.tipologia_incarico or ""
            writer.writerow(
                {
                    "nome": brain.Title,
                    "incarico": ruolo,
                    "data inizio": data_inizio,
                    "tipo": tipo_incarico,
                    "url": brain.getURL(),
                }
            )

        res = sbuf.getvalue()
        sbuf.close()
        return res
