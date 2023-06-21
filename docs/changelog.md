[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "Features" project](https://github.com/users/peter88213/projects/1).

### v4.29.2

- Do not create a button bar at the bottom of the project properties window.

Based on PyWriter v12.13.3

### v4.29.1

- Restore status by clicking on the status bar.

Based on PyWriter v12.13.3

### v4.29.0

- Extend the API for the [buttonbar plugin](https://peter88213.github.io/novelyst_buttons).

Based on PyWriter v12.13.2

### v4.28.1

- Fix a regression from v4.28.0 where the contents viewer is not updated when changing the project.

Based on PyWriter v12.13.1

### v4.28.0

- When exporting an ODT document that is not meant for re-import,
convert yWriter comments into footnotes or endnotes.
- Bugfix: Make the contents viewer read-only.

Based on PyWriter v12.13.0

### v4.27.4

- Fix a regression from v4.27.3 where problems may occur if no trashbin chapter exists.

Based on PyWriter v12.11.0

### v4.27.3

- Lock the trashbin's position when automatically moving parts to the Book branch.

Based on PyWriter v12.11.0

### v4.27.2

- Improve ui messaging.
- Refactor the right frame viewer classes.

Based on PyWriter v12.11.0

### v4.27.1

- Add character/location/item image support.
- Change WorkFile description.

Based on PyWriter v12.11.0

### v4.26.0

- Display a cover thumbnail image with the project properties.

Based on PyWriter v12.11.0

### v4.25.0

- Import characters, locations, and items from XML data files.

Based on PyWriter v12.11.0

### v4.24.3

- Exclude the scene marks in the "proofing" document from spell checking.

Based on PyWriter v12.8.5

### v4.24.2

- Fix a regression from v2.24.0 where the "proofing" document export may crash in case no language tags are found.

Based on PyWriter v12.8.3

### v4.24.1

- Fix heading of unnamed scenes in the contents viewer.
- Simplify the "proofread" document's structure.

Based on PyWriter v12.8.2

### v4.24.0

Modify the "Proofing document" classes for ODT exchange document conversion:

- Exclude "Unused", "Notes" and "Todo" scenes from the document export.
- Apply direct formatting instead of the emphasizing character styles.
- Do not apply the "Quotation" paragraph style.

Based on PyWriter v12.8.1

### v4.23.1

- Initialize new project's metadata.

Based on PyWriter v12.7.1

### v4.23.0

- Provide translations for scene related comments in the exported documents. 

Based on PyWriter v12.7.0

### v4.22.1

- Remove the "Project" node. 
- Update help.

Based on PyWriter v12.6.0

### v4.22.0

- Add a "Project" node for the project settings.
- Rename the "Narrative" node to "Book". 

Based on PyWriter v12.6.0

### v4.21.1

- Change the online help link.
- Restructure and extend the online help.

Based on PyWriter v12.6.0

### v4.21.0

- New menu entry: **Tools > Open installation folder**.

Based on PyWriter v12.6.0

### v4.20.2

- Skip "not exported" scenes when collecting chapter display data in the tree view.
- Fix scene position display in the tree view.
- Fix status word count.

Based on PyWriter v12.6.0

### v4.20.1

- Identify "not exported" scenes in the tree view.
- Words in "not exported" scenes don't count.

Based on PyWriter v12.6.0

### v4.20.0

- Extend the Plugin API.
- Do not show "not exported" scenes in the contents viewer.

Based on PyWriter v12.6.0

### v4.19.8

- Fix a regression from v4.13.3 where the "index card" is missing for project notes. 

Based on PyWriter v12.5.1

### v4.19.7

- Make the height of the "index card" and the "Goals/Conflict/Outcome" text boxes configurable.

Based on PyWriter v12.4.1

### v4.19.6

- Save space in the right window for smaller screens.

Based on PyWriter v12.4.1

### v4.19.5

- Remove the indenting spacer from the IndexCard title entry, because it doesn't look good on Linux.

Based on PyWriter v12.4.1

### v4.19.4

- Fix a regression from v4.17.4 where an unhandled exception occurs when reading a project without word count log.

Based on PyWriter v12.4.0

### v4.19.3

- Set the TextBox default font "Courier 10" (applies to Linux).
- Keep the "shebang" line when building the application.

Based on PyWriter v12.4.0

### v4.19.2

- Make the "index card" a widget of its own. 

Based on PyWriter v12.4.0

### v4.18.0

- The API for logging the writing progress is fixed.

Based on PyWriter v12.3.2

### v4.17.4

- Log word counts achieved with other word processors.

Based on PyWriter v12.3.2

### v4.17.3

- Do not touch the log unless "Save word count" is ckecked.

Based on PyWriter v12.3.2

### v4.17.2

- Remove entries with unchanged word count from the log.

Based on PyWriter v12.3.2

### v4.17.1

- Make it work on virtual file systems.

Based on PyWriter v12.3.2

### v4.17.0

- Add an option to delete yWriter-only data when writing .yw7.

Based on PyWriter v12.3.1

### v4.16.7

- Projects can now be saved even if they do not contain chapters.

Based on PyWriter v12.3.1

### v4.16.6

- When suppressing markup in the Text viewer, consider '>' (quoted text).

Based on PyWriter v12.3.0

### v4.16.5

- Fix a bug where cancelling parts did not work.
- Improve error handling.
- Refactor: Make the scene row coloring mode a type checked NovelystTk instance variable.

Based on PyWriter v12.3.0

### v4.16.4

- Store the coloring_mode setting as an integer value to make it locale-independent. 

Based on PyWriter v12.3.0

### v4.16.3

- Show status colors according to the work phase.
- Change the wording: Use "Mode" instead of "Style". 

Based on PyWriter v12.3.0

### v4.15.0

- Chapter word count includes normal scenes only.
- Add word count by scene status and usage to the project properties.

Based on PyWriter v12.3.0

### v4.14.3

- Ctrl-Alt-D toggles detach/dock properties window.
- Save properties when docking or detaching the properties window.
- Save properties on closing the project.
- Update icon.
- Refactor.

Based on PyWriter v12.3.0

### v4.14.2

- Prevent detaching the right pane more than once. 

Based on PyWriter v12.3.0

### v4.14.1

- The right pane (selected element's properties) can now be detached with Ctrl-Alt-D.
- Refactor: Move the _on_select_node() method from the TreeViewer to NovelystTk, and rename it to show_properties(). 

Based on PyWriter v12.3.0

### v4.14.0

- The right pane (selected element's properties) can now be toggled with Ctrl-Alt-T.

Based on PyWriter v12.3.0

### v4.13.3

- Refactor the code for better maintainability.

Based on PyWriter v12.3.0

### v4.13.2

- Refactor and re-organize the the code for better maintainability.

Based on PyWriter v12.2.0

### v4.13.1

- Fix the status setting for the "Characters" tree.

Based on PyWriter v12.1.2

### v4.13.0

- Insert new characters, locations, items, and project notes as specified in the help text.
- API upgrade: Extend the range of keyword arguments for several TreeViewer new node methods.

Based on PyWriter v12.1.2

### v4.12.1

- Add a separator to the "Tools" menu.

Based on PyWriter v12.1.2

### v4.12.0

- API upgrade: When creating a new tree element, the type can be set as a parameter.

Based on PyWriter v12.1.2

### v4.11.0

- API upgrade: When creating a new tree element, the title can be set as a parameter.  

Based on PyWriter v12.1.2

### v4.10.3

- For the correct display in Aeon Timeline 2, arc points get the same date/time as their associated scenes. 

Based on PyWriter v12.1.2

### v4.10.2

- Refactor: Terminate method stubs with return.
- Reduce the memory use by discarding the docstrings on building.

Based on PyWriter v12.1.2

### v4.10.1

- Improve handling of locked project.
- Improve error handling.

Based on PyWriter v12.1.1

### v4.10.0

- Update for PyWriter v12.
- Move the 'Remove custom fields' feature to the novelyst_ywriter plugin.

Based on PyWriter v12.1.0

### v4.9.1

- When joining scenes, add the scene notes.

Based on PyWriter v11.0.2

### v4.9.0

- Allow scene joining. 

Based on PyWriter v11.0.2

### v4.8.2

- Fix a bug where entered scene day is not displayed in the tree after applying changes.

Based on PyWriter v11.0.2

### v4.8.1

- Also generate unspecific date from the previous scene.
- Fix scene duration column.

Based on PyWriter v11.0.2

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

