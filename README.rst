.. |check| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck| raw:: html

    <input disabled="" type="checkbox">

==========================
Design Plone Content-types
==========================

Pacchetto per la gestione dei content-type per un sito Agid con Plone.

.. contents::

Features
========

Installando questo pacchetto, si rendono disponibili diversi content-type per la
gestione di un sito Agid con Plone e Volto.

Tipi di contenuto
=================

Elenco tipi implementati
------------------------

- Notizia: |check|
  - Definizione campi: |check|
  - Ordine campi: |check|
  - Indicizzazione testo: |uncheck|

- Luogo: |uncheck|
  - Definizione campi: |check|
  - Ordine campi: |uncheck|
  - Indicizzazione testo: |uncheck|

- Servizio: |uncheck|
  - Definizione campi: |check|
  - Ordine campi: |uncheck|
  - Indicizzazione testo: |uncheck|


Notizie e comunicati stampa
---------------------------

- Tipo base "Notizia" di Plone con alcuni campi aggiuntivi.
- Folderish (grazie a redturtle.volto)
- Può contenere Immagini, Collegamenti, File, Documenti (utile per strutturare i contenuti al suo interno)
- Alla creazione di una Notizia, vengono create automaticamente al suo interno due cartelle 
  "Multimedia" e "Documenti allegati" per poter organizzare meglio i contenuti

Luogo
-----

Esiste un deserializer per plone.restapi per il campo di tipo "GeolocationField" che si occupa di trasformare
le coordinate in input, in un oggetto corretto per quel campo.

Accetta un valore del tipo::

    {
      "latitude": 10.0000,
      "longitude": 20.0000,
    }

Alcuni campi della geolocalizzazione hanno dei valori predefiniti quando viene richiesto lo schema mediante plone.restapi:

- city
- street
- geolocation
- country

Sono pre-popolati con la sede di AGID a Roma.


Gestione vocabolari
===================

Per diversi tipi di contenuto servono dei vocabolari con una lista di valori predefiniti.

Questi sono configurabili dal pannello di controllo "*Vocabolari Design Plone*".

I vocabolari personalizzabili sono i seguenti:

- Tipologie notizia
- Tipologie unità organizzativa

Installazione
=============

Questo prodotto non è stato pensato per funzionare da solo, ma fa parte della suite "design.plone".

Per utilizzare questo prodotto, fare riferimento a design.plone.policy_.

.. _design.plone.policy: https://github.com/RedTurtle/design.plone.policy

Traduzioni
==========

Per aggiornare le traduzioni, basta usare lo script `update_locales` dentro alla cartella bin::

  > bin/update_locales

**N.B.: lo script va chiamato due volte perché al primo giro non aggiorna i file.**


Contribuisci
============

- Issue Tracker: https://github.com/redturtle/design.plone.contenttypes/issues
- Codice sorgente: https://github.com/redturtle/design.plone.contenttypes


Licenza
=======

Questo progetto è rilasciato con licenza GPLv2.

Autori
======

Questo progetto è stato sviluppato da **RedTurtle Technology**.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
