Changelog
=========

6.3.6 (2025-04-09)
------------------

- Fixed upgrade steps for Persona CT to prevent breakage due to ConstrainTypes restrictions
  [lucabel]


6.3.5 (2025-04-02)
------------------

- Fix upgrade step; we can't update types due to customer customizations;
  we need to fix single parts of type profiles
  [lucabel]
- Remove limit to "assessore_di_riferimento" in UO
  [lucabel]
- Add upgrade-step to add missing metadata for image captions.
  [cekk]
- Add "data fine effettiva" for events, to order listing correctly
  [lucabel]
- Fix typo in Venue serializer that didn't return the right history version.
  [cekk]
- Add "Emolumenti a carico della finanza pubblica" to Persona
  Add "Dichiarazioni di insussistenza e incompatibilità" to Persona
  [lucabel]


6.3.4 (2025-03-07)
------------------

- Added download xlsx of users in design-utils
  [mamico]
- Change number of related assessore_riferimento
  [lucabel]
- Add File to CT Documento but hide it from volto add menu
  [lucabel]
  


6.3.3 (2025-02-20)
------------------

- Refactor retrieveContentsOfFolderDeepening to be compliant with https://github.com/RedTurtle/redturtle.bandi/pull/25.
  [cekk]
- Return None in geolocation converter also if coordinates are 0.0.
  [cekk]


6.3.2 (2025-02-06)
------------------

- Added the metadata preview_caption and image_caption. An upgrade step is not necessary because the metadata will primarily be used for new content.
  [mamico]
- add SEO behavior to File
  [mamico]
- Fix sorting in @scadenziario-day endpoint.
  [folix-01]
- Check servizi view: remove illegal characters.
  [daniele]
- Removed Document from addable types of Documento CT.
- Removed moduli limitation on Documento CT serializer.
  [eikichi18]

6.3.1 (2024-12-12)
------------------

- Update it translations
  [lucabel]


6.3.0 (2024-12-05)
------------------

- Add dependency with collective.volto.blocksfield >= 2.2.0 and install it to have all blocks indexed in block_types index.
  [cekk]
- Do not use eea.api.taxonomy because it is deprecated.
  [cekk]


6.2.24 (2024-11-26)
-------------------

- Add fields end and recurrence on event summary serializer
  [eikichi18]


6.2.23 (2024-11-22)
-------------------

- Override BandoView: in io-Comune we add new children on Folder Deepening content
  and we need to proper handle it
  [lucabel]
- update serializer for documento ct adding more information about modulo children
  [lucabel]

6.2.22 (2024-10-30)
-------------------

- Aggiunto indice per gestire correttamente i confronti rispetto
  alla data di inizio; start viene trattato in modo customizzato
  [lucabel]


6.2.21 (2024-10-23)
-------------------

- Fix tests: do not import collective.volto.cookieconsent.
  [cekk]


6.2.20 (2024-10-17)
-------------------

- Fix upgrade step 
  [lucabel]
- Avoid acquisition problem in *onModify* event handler: now try to reindex children only if context is folderish.
  [cekk]
- Add sort_on sortable_title to event_location, uo_location, ufficio_responsabile vocabularies 
  [lucabel]

6.2.19 (2024-09-23)
-------------------

- Return Bando.apertura_bando as null if had been set default("1100-01-01T00:00:00").
  [folix-01]
- Add link to "find-broken-links" in design-utils view (need dependency with redturtle.volto>=5.5.3).
- Fix a bug introduced by changes in 6.2.16
  AttributeError: 'NoneType' object has no attribute 'absolute_url'
  [mamico]

6.2.18 (2024-09-06)
-------------------

- Refactor ServizioTextLineFieldSerializer adapter to check eventually a content type
  [lucabel]


6.2.17 (2024-09-06)
-------------------

- The permission to view the ModelloPratica has been made parametric.
  [lucabel]


6.2.16 (2024-09-06)
-------------------

- On CT Servizio don't want to see 'unauthorized' for anonymous user when click on
  "Accedi al servizio" but prefer to see an 'access' label, which can be obtained using
  {url}/login. For this reason, we want to ensure that if the current user doesn't have
  permission to view the target of the 'access the service' button, a link with /login
  will be used instead.
  [lucabel]

6.2.15 (2024-09-04)
-------------------

- Workaround for empty contacts UO summaryserializer
  [mamico]
- Add design.plone.contenttypes.behavior.news_base behavior (news metadata, without blocks)
  [mamico]
- Add folder creation (multimedia + allegati) for "ComunicatiStampa" CT (if exists)
  [mamico]
- Add "Emolumenti a carico della finanza pubblica" to Persona
  Add "Dichiarazioni di insussistenza e incompatibilità" to Persona
  [lucabel]

6.2.14 (2024-07-11)
-------------------

- Fix security problems for bandit.
  [cekk]
- Fix `to_7306`` upgrade-step to be more specific on types configuration.
  [cekk]


6.2.13 (2024-07-08)
-------------------

- Set `file_principale` field as primary, so we call @@download on the content, that file will be downloaded automatically.
  [cekk]
- Override listing.pt from plone.app.contenttypes due to error rendering event
  [lucabel]


6.2.12 (2024-06-24)
-------------------

- Fix problem with upgrade step to 7305
  [lucabel]


6.2.11 (2024-06-24)
-------------------

- Disallower other objs creation in Persona and Incarico ct.
- Fix limit in query for service in ScadenziarioDayPost service
  [eikichi18]


6.2.10 (2024-06-11)
-------------------

- Add importi_viaggio_servizio field as block field in Incarico response
  [eikichi18]
- Add rassegna index to events
  [lucabel]
- Remove File from addable type in Servizio / modulistica folder. As stated
  by AGID team we can't add File in this folder but link to modules in
  "Documenti e Dati" section
  [lucabel]

6.2.9 (2024-05-21)
------------------

- Add this folder "Altri Documenti" under "Persona pubblica"
  [lucabel]
- Code porting to work with both plone 6.0.10.x and 6.0.11
  due to some core egg update
  Code porting to work with the new plone.restapi 9.6.1 version
  [lucabel]

6.2.8 (2024-04-22)
------------------

- Add start metadata to event summary serialization;
  useful when create event with children event: in items list we
  have subevents with missing start date
  [lucabel]


6.2.7 (2024-04-22)
------------------

- Fix change_news_type view; Taxonomy doesn't index values not present in
  the taxonomy vocabulary, so we had lot of old values not indexed and not listed
  as available type to change.
  [lucabel]
- Do not break News serialzier if `tipologia_notizia` attribute is missing.
  [cekk]


6.2.6 (2024-04-18)
------------------

- improved check on relation.
  [daniele]


6.2.5 (2024-04-17)
------------------

- check-servizi: fixed check on relation title.
  [daniele]


6.2.4 (2024-04-16)
------------------

- converted some file and image fields as blob fields
  [mamico]


6.2.3 (2024-04-16)
------------------

- Image are no longer required in venue
  [lucabel]


6.2.2 (2024-03-19)
------------------

- @@check-servizi: provides also the full list of servizi.
  [daniele]
- UnitaOrganizzativa.assessore_riferimento title internationalize.
  [folix-01]

6.2.1 (2024-03-07)
------------------

- Added check for blocks field in check_luoghi view.
  [eikichi18]


6.2.0 (2024-03-06)
------------------

- Remove unused behavior (design.plone.contenttypes.behavior.geolocation_uo).
  [cekk]
- Standardize subfolders creations in events.
  [cekk]
- Do not return a fieldset if it has all fields hidden (maybe after a schema tweak).
  [cekk]
- Improve types test for their schema, required fields, fieldsets.
  [cekk]
- Add *exclude_from_search* indexer and behavior, and enable for Document and Folder.
  [cekk]
- Add custom adapter for IZCatalogCompatibleQuery to force all anonymous @search calls to skip items excluded from search.
  [cekk]
- Set *exclude_from_search* to True in all Documents/Folders automatically created in createSubfolders event handler,
  and add an upgrade-step that fix already created ones.
  [cekk]

6.1.14 (2024-02-20)
-------------------

- Fix in @scadenziario endpoint: return future events if afterToday criteria is set.
  [cekk]
- Set base view to News Item, to do not break on Classic Plone.
  [cekk]
- Change description for field sede in UnitaOrganizzativa CT.
- Fixed typo in update_note field description.
  [eikichi18]


6.1.13 (2024-02-08)
-------------------

- Handle missing `show_dynamic_folders_in_footer` in registry entry.
  [cekk]


6.1.12 (2024-02-06)
-------------------

- Remove un-needed commit in upgrade-step.
  [cekk]


6.1.11 (2024-01-29)
-------------------

- Added new indexer, catalog index and query operation for canale_digitale_link field of Servizio CT
[deodorhunter]

- Fixed script to update pdc with description
  [eikichi18]
- Add getObjSize info in File field serializer.
  [cekk]
- Add new flag in settings needed to choose to show or not auto-generated footer columns.
  [cekk]
- Customize @navigation endpoint to expose also the new flag for frontend.
  [cekk]

6.1.10 (2024-01-16)
-------------------

- Added description to PDC fields
  [pnicolli]
- Added upgrade step to update PDC fields description
  [lucabel]
- Added new widget for event luoghi_correlati
  [pnicolli]
- Added UID for all summary obj
  [eikichi18]


6.1.9 (2024-01-11)
------------------

- Add UID to UOJSONSummarySerializer
  [eikichi18]


6.1.8 (2023-12-22)
------------------

- Add behavior argomento to Link CT
  [lucabel]
- Removed maximumSelectionSize from all fields that had it greater than 0
  [pnicolli]


6.1.7 (2023-12-20)
------------------

- Improved "Check notizie" view adding a way to set "a cura di" field
  [lucabel]
- Fixed label for tassonomia_evento taxonomies.
  [eikichi18]


6.1.6 (2023-12-15)
------------------

- Improved "Buone pratiche" view for Event: checking both for relation with Venue and coordinates.
  [daniele]


6.1.5 (2023-12-13)
------------------

- Allow reorder of data grid fields.
  [pnicolli]


6.1.4 (2023-12-04)
------------------

- Fix check_persone. When there are no relation.
  [mamico]


6.1.3 (2023-11-28)
------------------

- "Buone pratiche" views: fixed check on Competenze field. Excluding expired events and news.
  [daniele]

6.1.2 (2023-11-27)
------------------

- Added utility views: @@check-notizie and @@download-check-notizie.
  [daniele]
- Fix event for obj parent update.
  [eikichi18]

- Added utility views: @@check-eventi and @@download-check-eventi.
  [daniele]

- Added utility views for Venue: @@check-luoghi and @@download-check-luoghi.
  [daniele]

- Added utility view for Documento:  @@check-documenti and @@download-check-documenti.
  [daniele]

- Added utils view for UO:  @@check-uo and @@download-check-uo.
  [daniele]

- Added utility views for Persona: @@check-persone and @@download-check-persone.
  [daniele]

6.1.1 (2023-11-21)
------------------

- Update default summary serializer to better handle geolocation information.
  [lucabel]


6.1.0 (2023-11-07)
------------------

- Optionally add image_scales and image_field in Summary serializer.
  [mamico]

- Add @@design-utils view that shows all available utility views.
  [cekk]

- Add user action that points to @@design-utils view.
  [cekk]

- Add @@export-incarichi view that allows to download a csv file with all Persona and their roles.
  [cekk]

- Add tipologia_bando to summary serializer.
  [cekk]

6.0.21 (2023-10-30)
-------------------

- Handle cost with empty text block in previous upgrade-step.
  [cekk]


6.0.20 (2023-10-30)
-------------------

- Add upgrade-step to set a default cost text for events.
  [cekk]


6.0.19 (2023-10-25)
-------------------

- Set event tickets cost as required field
  [pnicolli]


6.0.18 (2023-09-20)
-------------------

- Add permission check to solve problem accessing private resources with
  anonymous user
  [lucabel]


6.0.17 (2023-09-06)
-------------------

- Added dates for incarico persona.
  [deodorhuter]


6.0.16 (2023-08-24)
-------------------

- chaged migration of compensi and importi_di_viaggio field on Incaricto ct
  creation.
  [eikichi18]
- Fixed relation between person and uo.
  [deodorhunter]


6.0.15 (2023-07-19)
-------------------

- fix check_servizi handling "condizioni di servizio".
  [lucabel]


6.0.14 (2023-07-19)
-------------------

- Update check_servizi view to add service download
- Add contact information to check_servizi view
- Fix bug with "tempi e scadenze" error message
  [lucabel]


6.0.13 (2023-07-04)
-------------------

- Update check_servizi to skip private and expired services
  [lucabel]

6.0.12 (2023-07-03)
-------------------

- Add IDesignPloneContentType interface to News and Event to allow a correct
  SearchableText indexing
  [lucabel]


6.0.11 (2023-06-20)
-------------------

- Added image_scales field in service of ScadenziarioDay
- summary serializer to make it more roboust
  [mamico]


6.0.10 (2023-06-19)
-------------------

- remove preview_caption
  [mamico]
- removed required from persone_struttura field in uo
  interface.
  [eikichi18]


6.0.9 (2023-05-25)
------------------

- Added time to start date in service of ScadenziarioDay.
  [sabrina-bongiovanni]
- Fix url in check_servizi
  [mamico]

6.0.8 (2023-05-04)
------------------

- Fix problem with Persona summary and deleted incarico object.
  [lucabel]


6.0.7 (2023-05-04)
------------------

- Fix check_servizi view and made optional canale_fisico in Servizio
  [lucabel]


6.0.6 (2023-04-28)
------------------

- Added images serialization to the summary serializer of the UO content type;
  If both the image and preview image are present, the 'image_field' attribute
  is forced to contain 'preview_image'.
  [lucabel]

6.0.5 (2023-04-28)
------------------

- Remove address, city, zip_code, nome_sede, title,
  quartiere, circoscrizione, street from UO summary
  serializer and add sede in thery place in the
  UO summary serializer
  [lucabel]
- Re-add FileFieldViewModeSerializer accidentally deleted.
  [cekk]
- Fix broken tests.
  [cekk]

6.0.4 (2023-04-19)
------------------

- Remove redturtle.prenotazioni integration.
  [cekk]
- Fix syndication.
  [lucabel]


6.0.3 (2023-04-18)
------------------

- Change check_servizi making optional the check for
  field "condizioni_di_servizio" and removing the check for
  the "contact_info" field.
  Import a fontawesome cdn in this view to show the "V" icon.
  Change some minor style in the check_servizi view.
  [lucabel]


6.0.2 (2023-04-11)
------------------

- Fix condizioni_di_servizio field, no more required.
  [eikichi18]


6.0.1 (2023-04-06)
------------------

- Fix None type itereation attempt in relation field adapter
  [foxtrot-dfm1]
- Add serializer/deserializer for canale_digitale_link to handle internal/external links like remoteURL field.
  [cekk]
- Force canale_digitale_link return `url` widget in Servizio schema.
  [cekk]
- Do not purge allowed_content_types filter for Servizio.
  [cekk]

- Fix patch/post validations for required fields: do not return errors when sorting items.
  [cekk]
- Add "Atto di nomina" link in incarico summary serializer
  [lucabel]

6.0.0 (2023-03-23)
------------------
- improve upgrade step
  [lucabel]

6.0.0a22 (2023-03-07)
---------------------

- timeline_tempi_scadenze non più obbligatorio
  [pnicolli]


6.0.0a21 (2023-03-01)
---------------------

- Better handle default language in upgrade-step
  [cekk]


6.0.0a20 (2023-02-27)
---------------------

- Add a new upgrade step to rename "multimedia" in "immagini"
  under an event and add the new "video" folder.
  [lucabel]


6.0.0a19 (2023-02-27)
---------------------

- Change event schema: "patrocinato da"  right now is a
  rich text
  [lucabel]


6.0.0a18 (2023-02-22)
---------------------

- First release of check_service view; need to test on
  a staging
  [lucabel]


6.0.0a17 (2023-02-20)
---------------------

- Start implement a view to check service for new data
  [lucabel]
- Improved check for taxonomy data.
  [sabrina-bongiovanni]


6.0.0a16 (2023-02-08)
---------------------

- Improved github action for automatic deploy.
- Fixed tipologia_notizia in serializer.
  [eikichi18]


6.0.0a15 (2023-02-08)
---------------------

- Fixed tipologia_notizia in serializer.
  [eikichi18]


6.0.0a14 (2023-02-08)
---------------------

- Fixed design_italia_meta_type data in summary for News Item.
  [eikichi18]


6.0.0a13 (2023-02-06)
---------------------

- Fix field description
  Fix bug with taxonomies for old contenttypes
  Change field fieldset
  [lucabel]


6.0.0a12 (2023-02-06)
---------------------

- Cambiato descrizione tempi e scadenze
  [lucabel]


6.0.0a11 (2023-02-03)
---------------------

- Fix upgrade step.


6.0.0a10 (2023-02-03)
---------------------

- Update some tickets to show or hide fields
  in Servizo and UO.
  Fix problems with taxonomies
  upgrade steps to clean catalog
  [lucabel]


6.0.0a9 (2023-02-02)
--------------------
- New view 'change_news_type'
  [foxtrot-dfm1]
-  New view 'move_news_items'
  [foxtrot-dfm1]


6.0.0a8 (2023-01-23)
--------------------

- Fixed some field in event and news ct.
- Add news argomenti_evento behavior for event.
- Remove old argomenti behavior for news item.
  [eikichi18]


6.0.0a7 (2023-01-20)
--------------------

- Fix persona role handling: take the role from the connected incarico object
  [lucabel]


6.0.0a6 (2023-01-20)
--------------------
- various fixes
- add Event summary serializer to get image information
  also on parent
- merge with last master update
  [lucabel]


6.0.0a5 (2023-01-19)
--------------------

- Fix patch for collective.taxonomy.
  [eikichi18]


6.0.0a4 (2023-01-19)
--------------------

- add image to event summary.
  [lucabel]
- fix datagrid field frontend widget declaration.
  [roman]
- removed unused field evento_genitore e appuntamenti from event ct.
  [eikichi18]


6.0.0a3 (2023-01-13)
--------------------

- Update upgrade steps to change types information
  according to new AGID AI
  [lucabel]


6.0.0a2 (2023-01-12)
--------------------

- Fixed upgrade step
- minor fix
  [lucabel]


6.0.0a1 (2023-01-12)
--------------------

- Remove collective.dexteritytextindexer dependency (it's in core).
  [cekk]
- Adjustments to the pnrr.
  [deodorhunter, lucabel, eikichi18]

5.1.7 (unreleased)
------------------

- Optional integration with redturtle.prenotazioni
  [foxtrot-dfm1]
- Update upgrade step after some more use case [lucabel]

5.1.6 (2023-03-16)
------------------

- Enable plone.excludefromnavigation for Venue ct.
  [cekk]


5.1.5 (2023-02-15)
------------------

- @modulistica-items honors the currently logged-in user roles to access inactive contents (expired and not yet published).
  [cekk]


5.1.4 (2023-02-07)
------------------

- Fix lables.
  [foxtrot-dfm1]

5.1.3 (2023-02-06)
------------------

- Fix label of CartellaModulisitica visualize_files field.
  [foxtrot-dfm1]


5.1.2 (2023-02-06)
------------------

- All the file fields download link view method of child contents depends
  on the CartellaModulistica c.t. visualize_files field.
  [foxtrot-dfm1]


5.1.1 (2023-01-18)
------------------

- New view 'change_news_type'.
  [foxtrot-dfm1]
- New view 'move_news_items'.
  [foxtrot-dfm1]


5.1.0 (2023-01-03)
------------------

- Remove selection limit in ufficio_responsabile field for Servizio.
  [foxtrot-dfm1]
- Add new indexer "tassonomia_argomenti_uid" that indexes related Argomenti UIDs.
  [cekk]
- Change collection criteria to use new index.
  [cekk]
- Upgrade-step to convert old blocks with new criteria.
  [cekk]

5.0.3 (2022-12-07)
------------------

- Fix date format in related_news_serializer.
  [cekk]
- Remove plone.tableofcontents behavior from Document.
  [cekk]

5.0.2 (2022-09-19)
------------------

- Handle missing attribute in pagina_argomento event handler.
  [cekk]


5.0.1 (2022-08-16)
------------------

- Backref of UO to Servizio
  [foxtrot-dfm1]
- Remove unused import in tests.
  [cekk]

5.0.0 (2022-08-12)
------------------

- Fix content-types behaviors for plone.volto update (re-disable volto.blocks in News Items and Events).
  [cekk]
- Field tipologia_organizzazione in Unita Organizzativa ct. changed to required
  [foxtrot-dfm1]

4.4.2 (2022-07-01)
------------------

- Index Bando text.
  [cekk]


4.4.1 (2022-05-31)
------------------

- Handle new Bando field: apertura_bando.
  [cekk]


4.4.0 (2022-05-31)
------------------

- Enable versioning also for: CartellaModulistica, Documento, Link, Pagina Argomento, Persona, Servizio, Unità Organizzativa, Venue.
  [cekk]


4.3.3 (2022-05-22)
------------------

- Fix SearchableText indexing for Venues.
  [cekk]


4.3.2 (2022-05-17)
------------------

- Add volto.preview_image behavior in Bando portal_type.
  [cekk]


4.3.1 (2022-04-21)
------------------

- Add missing msgids to Unita Organizzativa fields.
  [cekk]


4.3.0 (2022-04-05)
------------------

- Add custom expand_events method in scadenziario endpoints, because in plone.app.events >= 3.2.13
  that method changed and breaks our integration. We keep previous version of that method to
  not re-implement scadenziario endpoints.
  [cekk]


4.2.1 (2022-03-26)
------------------

- Add behavior for update note additional field.
  [cekk]
- Fix servizi_collegati labels.
  [cekk]


4.2.0 (2022-03-21)
------------------

- Add new criteria for tipologia_organizzazione field/index.
  [cekk]


4.1.1 (2022-03-16)
------------------

- Fix summary serializers for specific types.
  [cekk]


4.1.0 (2022-03-14)
------------------

- Do not return related items in serializer, if they're published but the date is in the future and the current user can't edit current context.
  [cekk]
- Add default folders when creating a new Bando.
  [cekk]
- Align summary serializer with latest redturtle.volto changes (pr #53).
  [cekk]

4.0.6 (2022-02-25)
------------------

- Fix common indexers to work with also non-folderish contents.
  [cekk]


4.0.5 (2022-02-02)
------------------

- Fix geolocation hack.
  [cekk]


4.0.4 (2022-02-01)
------------------

- Add "geolocation" info in Summary serializer for backward compatibility with some block templates.
  [cekk]


4.0.3 (2022-01-31)
------------------

- Add right widget to scadenza_domande_bando field.
  [cekk]
- Remove all u" from strings because they are un-needed in Python3 (and new black does not support python2 anymore).
  [cekk]

4.0.2 (2022-01-27)
------------------

- Fix miniature dimension to be the same as design.plone.policy ones.
  [cekk]


4.0.1 (2022-01-27)
------------------

- Fix upgrade-step to rename Document childrens with "image" as id.
  [cekk]
- Add new metadata "icona" for Pagina Argomento.
  [cekk]
- Remove broken template customization.
  [cekk]


4.0.0 (2022-01-26)
------------------

- Add new metadata for Volto 14 support: we need some extra infos in blocks without getting the full object.
  [cekk]
- Add preview_image in all contents (from plone.volto).
  [cekk]
- Customized summary serializer to add more infos for listing blocsk.
  [cekk]


3.9.2 (2022-01-24)
------------------

- Bandi folder deepening now returns actual children order in parent instead of being ordered by title.
  [deodorhunter]
- Added default values for Persona roles.
  [daniele]


3.9.1 (2022-01-13)
------------------

- Fix publication when adding events.
  [daniele]


3.9.0 (2021-12-27)
------------------

- Add default blocks in automatic created documents.
  [cekk]


3.8.3 (2021-12-17)
------------------

- Added criteria and indexes for Persona
  [daniele]


3.8.2 (2021-11-26)
------------------

- Create additional folder in Persona for curriculum vitae.
  [cekk]


3.8.1 (2021-11-22)
------------------

- Fix scadenziario sort_order
  [pnicolli]
- Add plone.constraintypes behavior for Document.
  [cekk]

3.8.0 (2021-10-22)
------------------

- Export children and parent UO in UO details.
  [cekk]
- Export more infos in UO summary adapter.
  [cekk]
- ufficio_responsabile in Servizio allows now 10 items.
  [cekk]
- *ruolo* is now a Choice field and can be configured in control panel.
  [cekk]

3.7.4 (2021-10-21)
------------------

- Add *ruolo* metadata for Persona and export it in summary serializer.
  [cekk]


3.7.3 (2021-10-15)
------------------

- Fix addable content-types for Venue.
  [cekk]


3.7.2 (2021-10-14)
------------------

- Import p.a.caching.
  [cekk]


3.7.1 (2021-10-10)
------------------

- Fix typo.
  [cekk]

3.7.0 (2021-10-10)
------------------

- p.a.caching rules for rest api services.
  [cekk]

3.6.2 (2021-10-05)
------------------

- [fix] Do not duplicate default folders in UO and Persona when copy/paste them.
  [cekk]


3.6.1 (2021-10-01)
------------------

- Enable kitconcept.seo beaviour for a set of CT.
  [daniele]


3.6.0 (2021-09-21)
------------------

- Add link_siti_esterni to SearchableText index.
  [cekk]
- showModifiedDefaultValue compatible with plone.restapi >= 8.9.1
  [cekk]
- All content-types extends **IDesignPloneContentType** marker interface.
  [cekk]
- Register custom TextBlockSearchableText adapter to index all text blocks in IDesignPloneContentType contents.
  [cekk]
- Customize some Bando and Bando Folder Deepenings fields and allowed types.
  [cekk]
- Add **ufficio_responsabile_bando** and **Subject_bando** indexes to speedup @bandi-search-filters endpoint.
  [cekk]
- Upgrade step to enable kitconcept.seo behavior on contents.
  [daniele]
- Refactor @types endpoint to be more extensible.
  [cekk]
- *show_modified_default* is **True** by default.
  [cekk]

3.5.0 (2021-08-24)
------------------

- Add new index: uo_location.
  [cekk]
- Add new fields to be indexed in SearchableText for UO: nome_sede, email, pec, web
  [cekk]
- Do not break if there are extra fieldsets that comes from non standard addons: just append them to the default ordered list.
  [cekk]

3.4.2 (2021-08-03)
------------------

- Remove required from *ufficio_responsabile* and *area_responsabile* in **Documento** contents.
  [cekk]


3.4.1 (2021-07-30)
------------------

- You can now add "File" content type inside a CartellaModulistica.
  [arsenico13]


3.4.0 (2021-07-07)
------------------

- Convert File into Modulo when trying to do a massive upload inside a Documento.
  [cekk]
- Fix description for "a_cura_di_persone" field.
  [cekk]
- Added "maximumSelectionSize" in RelatedItemsFieldWidget
  [giulia]
- Add mostra_bottoni_condivisione field.
- Change block @type: newsHome -> highlitedContent
  [cekk]

3.3.2 (2021-06-25)
------------------

- Enabled "trasparenza" behavior. It's back!
  [arsenico13]


3.3.1 (2021-06-17)
------------------

- Handle contents with old Richtext values in volto13 migration.
  [cekk]


3.3.0 (2021-06-17)
------------------

- Volto 13 compatibility.
  [cekk]


3.2.0 (2021-06-08)
------------------

- Add new behavior "design.plone.contenttypes.behavior.show_modified".
  [cekk]


3.1.1 (2021-05-28)
------------------

- Removed field "Accedere al servizio" from Documento ct.
  [daniele]

3.1.0 (2021-05-26)
------------------

- Add `design.plone.contenttypes.behavior.argomenti_document` behavior to **Document**.
  [cekk]
- *correlato_in_evidenza* field now return also icon value in restapi calls.
  [cekk]
- Add leadimage to **CartellaModulistica**.
  [cekk]

3.0.3 (2021-05-20)
------------------

- Added criteria for ente bando and ufficio responsabile.
  [daniele]

3.0.2 (2021-05-17)
------------------

- Added backreferences to Documento and Cartella Modulistica for related services.
  [daniele]
- Documento now set b_size=200 by default to show more than 25 items when getting its data.
  [cekk]


3.0.1 (2021-05-04)
------------------

- Fix upgrade-step.
  [cekk]


3.0.0 (2021-04-30)
------------------

- Rename controlpanel.
  [cekk]
- Now controlpanel settings entries can be multilanguage.
  [cekk]
- *organizzazione_riferimento* field for Persona no more required.
  [cekk]
- servizi_offerti in UO serializer now returns only related Servizi.
  [cekk]

2.0.6 (2021-04-16)
------------------

- Fix Venue fields order.
  [cekk]


2.0.5 (2021-04-16)
------------------

- Add `plone.app.dexterity.behaviors.id.IShortName`behavior to Venue content-type to allow renaming.
  [cekk]


2.0.4 (2021-04-15)
------------------

- Fix typo.
  [cekk]

2.0.3 (2021-04-08)
------------------

- Added behavior `plone.translatable` by default on almost all the content
  types.
  [arsenico13]


2.0.2 (2021-03-24)
------------------

- Now you can customize tipologie_persona from the control panel.
  [arsenico13]


2.0.1 (2021-03-24)
------------------

- Fix defaults for vocabularies.
  [cekk]
- Add remoteUrl to summarize serialization for Link content-type.
  [cekk]


2.0.0 (2021-03-02)
------------------

- BREAKING CHANGE: use blocks editor also in other "text" fields.
  [cekk]


1.0.9 (2021-02-25)
------------------

- Add search_sections field in control panel.
  [cekk]
- Can add Images into Cartella Modulistica (to be able to add image blocks in it).
  [cekk]
- Customizable tipologie_documento.
  [cekk]


1.0.8 (2021-02-19)
------------------

- Fix typo.
  [cekk]


1.0.7 (2021-02-19)
------------------

- Do not run dependencies when upgrading plone.app.registry.
  [cekk]


1.0.6 (2021-02-15)
------------------

- Handle Servizio tabs in both cases: with Trasparenza enabled or not.
  [cekk]


1.0.5 (2021-02-08)
------------------

- Disable trasparenza behavior by default.
  [deodorhunter]
- Remove reference limit in "persone_struttura" field.
  [cekk]


1.0.4 (2021-02-05)
------------------

- Add upgrade-step to cleanup Bando behaviors.
  [cekk]


1.0.3 (2021-01-20)
------------------

- **BREAKING CHANGE** Convert RichText fields into BlocksField.
- Upgrade-step to fix unused listing block template.
  [cekk]


1.0.2 (2020-12-17)
------------------

- Fix rolemap for new types.
  [cekk]
- Do not break *eventoCreateHandler* when copying and event.
  [cekk]


1.0.1 (2020-12-14)
------------------

- Add `immagine_testata` new field in *design.plone.contenttypes.behavior.info_testata* behavior.
  [cekk]
- Add `correlato_in_evidenza` new field in *design.plone.contenttypes.behavior.argomenti* behavior.
  [cekk]


1.0.0 (2020-12-07)
------------------

- Initial release.
  [RedTurtle]
