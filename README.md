<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Design Plone Content-types](#design-plone-content-types)
- [Features](#features)
- [Tipi di contenuto](#tipi-di-contenuto)
  - [Elenco tipi implementati](#elenco-tipi-implementati)
  - [Cartella Modulistica](#cartella-modulistica)
  - [Documento](#documento)
    - [Campi indicizzati nel SearchableText](#campi-indicizzati-nel-searchabletext)
    - [Evento di creazione](#evento-di-creazione)
  - [Luogo](#luogo)
  - [Modulo](#modulo)
  - [Notizie e comunicati stampa](#notizie-e-comunicati-stampa)
  - [Pagina](#pagina)
  - [Pagina Argomento](#pagina-argomento)
    - [Campi indicizzati nel SearchableText](#campi-indicizzati-nel-searchabletext-1)
  - [Persona](#persona)
    - [Evento di creazione](#evento-di-creazione-1)
    - [Campi indicizzati nel SearchableText](#campi-indicizzati-nel-searchabletext-2)
  - [Servizio](#servizio)
    - [Campi indicizzati nel SearchableText](#campi-indicizzati-nel-searchabletext-3)
  - [Unità Organizzativa](#unità-organizzativa)
    - [Campi indicizzati nel SearchableText](#campi-indicizzati-nel-searchabletext-4)
- [Gestione vocabolari](#gestione-vocabolari)
- [Gestione modulistica](#gestione-modulistica)
- [Endpoint restapi](#endpoint-restapi)
  - [Customizzazione dati relation field](#customizzazione-dati-relation-field)
- [Installazione](#installazione)
- [Traduzioni](#traduzioni)
- [Contribuisci](#contribuisci)
- [Licenza](#licenza)
- [Autori](#autori)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Design Plone Content-types

Pacchetto per la gestione dei content-type per un sito Agid con Plone.

# Features

Installando questo pacchetto, si rendono disponibili diversi content-type per la
gestione di un sito Agid con Plone e Volto.

# Tipi di contenuto

## Elenco tipi implementati

- [ ] **Cartella Modulistica**

  - [x] Definizione campi
  - [x] Ordine campi
  - [ ] Vista su Volto completata

- [ ] **Collegamento**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata
  - [ ] Selezione link interno

- [ ] **Dataset**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Ordine fieldsets
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Documento**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Documento Personale**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Ordine fieldsets
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [x] **Evento**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [ ] **Messaggio**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Ordine fieldsets
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Modulo**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [ ] Vista su Volto completata

- [x] **Notizia**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [x] **Luogo**

  - [x] Definizione campi
  - [x] Abilitare behavior collective.address.address
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata
  - [x] gestione di "è sede di"

- [x] **Pagina Argomento**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [x] **Persona**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [ ] **Pratica**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Ordine fieldsets
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Ricevuta Pagamento**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Ordine fieldsets
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [x] **Servizio**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [x] **Unità Organizzativa**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Ordine fieldsets
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

## Cartella Modulistica

Contenuto folderish (come la Pagina) che serve a raggruppare dei Documenti.

Questo content-type ha sia i blocchi attivati che una vista ad hoc che mostra i Documenti al suo interno con già i link ai file da scaricare.

Se i Documenti vengono raggruppati in Pagine, nella vista verrà mostrato il testo delle pagine contenitori come separatore tra i vari gruppi (solo nella parte Volto).

Nella proprietà @components dell'oggetto CartellaModulistica, viene sempre inviato nella prop modulistica-items l'url dell'endpoint per avere la struttura dati degli elementi da mostrare nella vista della cartella modulistica. Quell'url ritorna sempre una oggetto del tipo {items:[]} dove l'array contiene gli elementi.

## Documento

Ha i campi definiti da Agid (senza quelli specifici per i Bandi, perché li gestiamo con un content-type ad hoc).

Al suo interno può contenere degli oggetti di tipo **Modulo** (che sono i file scaricabili veri e propri).

I Moduli che vengono inseriti dentro al Documento, verranno mostrati nel frontend come lista di documenti scaricabili.

### Campi indicizzati nel SearchableText

- blocchi Volto

### Evento di creazione

Alla creazione di un Documento, un evento genera in automatico una cartella "Multimedia" dove andare ad inserire delle eventuali immagini.

L'evento imposta anche come unico contenuto aggiungibile dentro al Documento, il Modulo.

## Luogo

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

Il campo "**sede_di**" ritornato da restapi è calcolato in base alle Unità Operative che lo referenziano come sede principale o secondaria.

## Modulo

Content-type creabile solo all'interno del Documento. Questo è un File "evoluto".
Ha 3 campi file: uno per il modulo principale, e gli altri due per eventuali formati alternativi.

## Notizie e comunicati stampa

- Tipo base "Notizia" di Plone con alcuni campi aggiuntivi.
- Folderish (grazie a redturtle.volto)
- Può contenere Immagini, Collegamenti, File, Documenti (utile per strutturare i contenuti al suo interno)
- Alla creazione di una Notizia, vengono create automaticamente al suo interno due cartelle
  "Multimedia" e "Documenti allegati" per poter organizzare meglio i contenuti

## Pagina

- Può essere usata anche come pagina di disambiguazione. C'è una behavior attivata (_design.plone.contenttypes.behavior.info_testata_)
  per impostare informazioni aggiuntive per la testata delle pagine di disambiguazione.

## Pagina Argomento

Le pagine argomento hanno i blocchi. plone.restapi ha un indexer per _SearchableText_ per poter indicizzare i blocchi.

Questo va in conflitto con le personalizzazioni fatte con `collective.dexteritytextindexer` perché Plone prende come buono il primo
adapter di SearchableText che trova. Per ovviare a questo problema, abbiamo messo la behavior "volto.blocks" come ultima, in modo
che venisse ignorato il suo indexer, e poi abbiamo registrato un adapter per `IDynamicTextIndexExtender` per replicare l'indicizzazione
dei blocchi anche per le pagine argomento.

### Campi indicizzati nel SearchableText

- blocchi Volto
- unita_amministrative_responsabili
- ulteriori_informazioni

## Persona

Il serializer della persona, ritorna anche i seguenti valori calcolati:

- **strutture_correlate**: elenco di Unità Organizzative in cui la persona è stata aggiunta nel campo "Persone che compongono la struttura"
- **responsabile_di**: elenco di Unità Organizzative in cui la persona è stata aggiunta nel campo "Responsabile"
- **assessore_di**: elenco di Unità Organizzative in cui la persona è stata aggiunta nel campo "Assessore di riferimento"

### Evento di creazione

Alla creazione di una Persona, viene creata anche una struttura predefinita per contenere diversi documenti:

- Foto e attività politica
- Compensi
- Importi di viaggio e/o servizi
- Situazione patrimoniale
- Dichiarazione dei redditi
- Spese elettorali
- Variazione situazione patrimoniale
- Altre cariche

### Campi indicizzati nel SearchableText

- ruolo
- competenze
- deleghe
- tipologia_persona
- telefono
- email
- informazioni_di_contatto

## Servizio

### Campi indicizzati nel SearchableText

- descrizione_estesa
- sottotitolo
- descrizione_destinatari
- chi_puo_presentare
- come_si_fa
- cosa_si_ottiene
- cosa_serve
- ulteriori_informazioni
- tassonomia_argomenti
- copertura_geografica
- costi
- life_event
- servizi_collegati

## Unità Organizzativa

La get di questo content-type, ritorna (nell'attributo "**servizi_offerti**") anche la lista di Servizi che la referenziano nei campi "**ufficio_responsabile**" e "**area**".

### Campi indicizzati nel SearchableText

- street
- city
- zip_code
- country
- quartiere
- circoscrizione
- descrizione_breve
- orario_pubblico
- identificativo_mibac

# Gestione vocabolari

Per diversi tipi di contenuto servono dei vocabolari con una lista di valori predefiniti.

Questi sono configurabili dal pannello di controllo "_Vocabolari Design Plone_".

I vocabolari personalizzabili sono i seguenti:

- Tipologie notizia
- Tipologie unità organizzativa

# Gestione modulistica

Agid prevede un tipo di contenuto **Documento** per gestire i moduli scaricabili.

Abbiamo però sviluppato anche un contenuto chiamato **Cartella Modulistica** che ha il compito di raggruppare in modo logico più Documenti e mostrarli all'utente come faceva il vecchio prodotto **cciaa.modulistica**.

# Endpoint restapi

## Customizzazione dati relation field

C'è una customizzazione dei dati ritornati dal serializer per i relation field (correlati)
per ritornare oltre alle informazioni standard, anche la data di pubblicazione e l'inizio e fine evento.

## @modulistica_items

Endpoint ed expansion per la modulistica.

Nei content-type CartellaModulistica, tra i vari expansion c'è anche `@modulistica_items`.
Questo è utile per la vista di frontend, in quanto se richiamato, ritorna la struttura di dati da mostrare in visualizzazione.

# Installazione

Questo prodotto non è stato pensato per funzionare da solo, ma fa parte della suite "design.plone".

Per utilizzare questo prodotto, fare riferimento a design.plone.policy\_.

.. \_design.plone.policy: https://github.com/RedTurtle/design.plone.policy

# Traduzioni

Per aggiornare le traduzioni, basta usare lo script `update_locales` dentro alla cartella bin::

> bin/update_locales

**N.B.: lo script va chiamato due volte perché al primo giro non aggiorna i file.**

# Contribuisci

- Issue Tracker: https://github.com/redturtle/design.plone.contenttypes/issues
- Codice sorgente: https://github.com/redturtle/design.plone.contenttypes

# Licenza

Questo progetto è rilasciato con licenza GPLv2.

# Autori

Questo progetto è stato sviluppato da **RedTurtle Technology**.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
:alt: RedTurtle Technology Site
:target: http://www.redturtle.it/
