[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "features" project](https://github.com/users/peter88213/projects/1).

### v4.0.0

Upgrade API:
- Add  the PluginCollection.on_close method. 
- Call NovelystTk.on_close when closing a project. 
- Call NovelystTk.on_quit when closing novelyst.

Based on PyWriter v9.0.4

### v3.1.1

- Prepare RichTextYw for dark mode.

Based on PyWriter v9.0.4

### v3.1.0

- Make text box colors customizable for dark mode.
- Rework the novelyst_awdark plugin.

Based on PyWriter v9.0.4

### v3.0.2

- Code optimization and library update. 

Based on PyWriter v9.0.4

### v2.0.5

- Fix a bug where attempting to save a write-protected file raises an uncaught exception.
- API upgrade: Remove the global ERROR constant.
- Code optimization and library update.
- Restore status before creating a report or an export.
- Assign "no language" to the chapter/scene markers for the  proof reading document.
- When converting to ODT format, apply all XML predefined entities.

Based on PyWriter v8.0.8

### v1.6.3

- Fix a bug in odt manuscript export, where the "Quotation" style is not
applied at scene start.

Based on PyWriter v7.14.1

### v1.6.2

- Fix a bug where the wrong file date is displayed after opening an existing document.
- Do not warn the user if an up-to-date existing document is opened.
- Inform the user if the project cannot be saved due to locking.
- Refactor.
- Update docstrings.

Based on PyWriter v7.14.0

### v1.6.1

- Document export: Improve the "Overwrite/Open existing document?" dialog. 

Based on PyWriter v7.14.0

### v1.6.0

Count words like in LibreOffice. See:
https://help.libreoffice.org/latest/en-GB/text/swriter/guide/words_count.html

Document export:
- Only ask for opening existing documents, if rewritable.
- Add obfuscated text for word count.

Based on PyWriter v7.14.0

### v1.5.0

- Remove the "Open with yWriter" command.
- Provide a yWriter launcher plugin instead.

Based on PyWriter v7.13.1

### v1.4.1

- Reorganize the project settings.

Based on PyWriter v7.13.1

### v1.4.0

- Replace the custom fields by project variables. Thus make language/country accessible in yWriter.
- Fix a bug in PyWriter where empty codes are replaced with "no locale" instead of "system locale".

Based on PyWriter v7.12.2

### v1.3.3 Bugfix release

- Fix a regression from v1.3.2 where some document types are not exported.
- When exporting a re-importable document, lock the project only on success.

Based on PyWriter v7.11.4

### v1.3.2

- Make sure to apply changes before creating a report or exporting a document.

Based on PyWriter v7.11.4

### v1.3.1

Introduce a notation for assigning text passages to another language/country. This is mainly for spell checking in Office Writer.

Based on PyWriter v7.11.2

### v1.2.1

- Support "no document language" settings.

Based on PyWriter v7.10.2

### v1.2.0

- Fix a regression where a new project cannot be created due to a renamed variable.
- Put the project's writing progress data in a folding frame.
- Add entries for the document's language and country codes.

Based on PyWriter v7.8.0

### v1.0.1

- Make the "folding frames" look better when applying themes.

Based on PyWriter v7.4.9

### v1.0.0

- Release under the GPLv3 license.

Based on PyWriter v7.4.9

