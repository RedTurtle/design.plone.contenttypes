Changelog
=========


5.1.16 (2024-09-20)
-------------------

- Return Bando.apertura_bando as null if had been set default("1100-01-01T00:00:00").
  [folix-01]

5.1.15 (2024-09-16)
-------------------

- Backport of #268: Set `file_principale` field as primary, so we call @@download on the content, that file will be downloaded automatically.
  [cekk]


5.1.14 (2024-09-06)
-------------------

- Removed max limit in "dove_rivolgersi" field for Servizio ct.
  [daniele]


5.1.13 (2024-06-17)
-------------------

- Search field for CartellaModulistica c.t.
  [folix-01]


5.1.12 (2024-04-09)
-------------------

- Add *exclude_from_search* indexer and behavior, and enable for Document and Folder.
  [cekk]
- Add custom adapter for IZCatalogCompatibleQuery to force all anonymous @search calls to skip items excluded from search.
  [cekk]
- Set *exclude_from_search* to True in all Documents/Folders automatically created in createSubfolders event handler,
  and add an upgrade-step that fix already created ones.
  [cekk]


5.1.11 (2024-04-08)
-------------------

- locales
  [folix-01]


5.1.10 (2023-07-25)
-------------------

- Use newer template for newsitem_view.
  [folix-01]


5.1.9 (2023-07-11)
------------------

- Add IDesignPloneContentType interface to News and Event to allow a correct SearchableText indexing.
  [cekk]


5.1.8 (2023-06-26)
------------------

- remove preview_caption backport #190
  [mamico]


5.1.7 (2023-04-04)
------------------

- Do not purge allowed_content_types filter for Servizio.
  [cekk]


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
