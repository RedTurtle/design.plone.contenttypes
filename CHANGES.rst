Changelog
=========


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
