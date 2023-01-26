[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "features" project](https://github.com/users/peter88213/projects/1).

### v4.8.0

- Provide a button to set the date and time that follows the previous scene.

Based on PyWriter v11.0.2

### v4.7.0

- Provide tree navigation in the right pane.

Based on PyWriter v11.0.2

### v4.6.2

- Add buttons for clearing scene start/duration data.
- Enable clearing the duration entries.
- Improve entry checks.

Based on PyWriter v11.0.2

### v4.6.1

- Fix error handling for time and day entry.

Based on PyWriter v11.0.1

### v4.6.0

- Make scene date/time information editable.

Based on PyWriter v11.0.1

### v4.5.1

- Put the "Arc" part of the "Todo" scene view into a folding frame.
- Add the "Relationships" frame to the "Notes" and "Todo" scene views.

Based on PyWriter v10.0.1

### v4.5.0

- Add "Arcs" document export. 

Based on PyWriter v10.0.1

### v4.4.4

- If a scene's arc assignment is cleared, automatically clear the corresponding point assignments. 

Based on PyWriter v10.0.1

### v4.4.3

- Put auto-generated arc definitions into a new part in the "Planning" subtree.

Based on PyWriter v10.0.1

### v4.4.2

- Provide "Apply changes" button at the bottom of the right pane.
- No longer accept the assignment of non-existent arcs to scenes.
- Update the "Arcs" help page.

Based on PyWriter v10.0.1

### v4.4.1

- When clearing arc references, remove also all scene associations from the children points.
- Make sure that each arc is defined by a unique chapter.
- Fix a regression from v4.4.0 where arc defining chapters may be duplicated due to chapter field renaming.

Based on PyWriter v10.0.1

### v4.4.0

- Structure arcs with points.

Based on PyWriter v10.0.1

### v4.3.0

- Use chapters instead of scenes for arc description.

Based on PyWriter v10.0.1

### v4.2.5

- Make it run on old Windows versions.

Based on PyWriter v10.0.1

### v4.2.4

- View date/time of "Notes" scenes.

Based on PyWriter v9.0.5

### v4.2.3

- Fix a bug where the project view is not cleared when closing the project and saving changes.

Based on PyWriter v9.0.5

### v4.2.2

- When reading yw7 files, fix missing scene status as a tribute to defensive programming.

Based on PyWriter v9.0.5

### v4.2.1 Speed up the program start

IMPORTANT: 
- If you have a desktop shortcut to start novelyst, please change the target from "novelyst.pyw" to "run.pyw".
- If you use the Windows Explorer context menu entry, please re-run the registry scripts after setup.

- Rename "novelyst.pyw" --> "novelyst.py".
- Create a start-up script "run.pyw" during setup.
- Add a header to the "has notes" column.

Based on PyWriter v9.0.5

### v4.1.0

- New program setting: Change the order of the columns.

Based on PyWriter v9.0.5

### v4.0.3

- Improve code quality and documentation.

Based on PyWriter v9.0.5

### v4.0.2 Bugfix

- Fix a regression from v2.0.3 where wrong language markers are imported
from the "proofread" document.

Based on PyWriter v9.0.5

### v4.0.1 Bugfix

- Fix a regression where changes are not saved when "Save word count" is checked.

Based on PyWriter v9.0.4

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

