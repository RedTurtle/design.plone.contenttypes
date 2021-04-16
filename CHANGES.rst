Changelog
=========


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
