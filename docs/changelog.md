[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### Planned features

See the [GitHub "features" project](https://github.com/peter88213/novelyst/projects/1).

### v0.16.4 Beta release

- Fix setup script for Linux.
- Undo changes of v0.16.3
- Change requirements: Needs Python 3.9.10+

Based on PyWriter v5.16.1

### v0.16.3 Beta release

- Make the treeview colors display properly with Python versions prior to 3.9.10 on Windows.

Based on PyWriter v5.16.1

### v0.16.2 Beta release

- Fix word counting considering ellipses.

Based on PyWriter v5.12.4

### v0.16.1 Beta release

- Fix word counting considering comments, hyphens, and dashes.

Based on PyWriter v5.12.3

### v0.16.0 Beta release

- Enable multiple nodes selection.
- Move nodes using "Alt" instead of "Shift".
- When changing type or status, set "changed" only in case of actual changes.

Based on PyWriter v5.12.0

### v0.14.7 Beta release

- Do not lock the project when exporting "export only" documents.

Based on PyWriter v5.10.2

### v0.14.6 Beta release

- Make the data frame width configurable.

Based on PyWriter v5.10.0

### v0.14.5 Beta release

- Expand the Narrative subtree when opening a project.
- Add a View option "Chapter level".

Based on PyWriter v5.10.0

### v0.14.4 Beta release

- Add a middle window. Its width is controlled by its children, if any.
- Make the right window fixed width.

Based on PyWriter v5.8.0

### v0.14.3 Beta release

- Extend API by making all NovelystTk frames "public".

Based on PyWriter v5.8.0

### v0.14.2 Beta release

- Fix a bug where the application cannot be closed.

Based on PyWriter v5.8.0

### v0.14.1 Beta release

- Extend the API for a new [scene editor plugin](https://github.com/peter88213/novelyst_editor).

Based on PyWriter v5.8.0

### v0.14.0 Beta release

- Extend the API for a new scene editor plugin.

Based on PyWriter v5.8.0

### v0.12.0 Beta release

- Fix a bug where new projects cannot be created.
- Add Author entry.
- Assign scenes to arcs.
- Use "Todo" type scenes for defining arcs.

Based on PyWriter v5.8.0

### v0.10.2 Beta release

- Adjust entry fields.
- Extend reading and writing custom keyword variables for features to come.

Based on PyWriter v5.6.1

### v0.10.1 Beta release

- Fix a bug in item selection handler.
- Add "AKA" entry.
- Add character "Full name" entry.
- Resize the description text box.
- Expand labeled widgets.

Based on PyWriter v5.6.1

### v0.10.0 Beta release

- Add scene date/time/duration display.

Based on PyWriter v5.6.1

### v0.8.0 Beta release

- Add Character Bio and Goals entry.
- Add Scene pacing data entry.

Based on PyWriter v5.6.1

### v0.6.3 Alpha release

- Add "Remove custom fields" option. 

Based on PyWriter v5.6.1

### v0.6.2 Alpha release

- Show chapter viewpoints.

Based on PyWriter v5.6.1

### v0.6.1 Alpha release

- The scene viewpoint can be changed.

Based on PyWriter v5.6.1

### v0.6.0 Alpha release

- Change the way plugins are imported. `__init__.py` isn't required any longer.

Based on PyWriter v5.6.1

### v0.4.3 Alpha release

- Remove multiple characters/locations/items (as created due to a bug by yw-timeline) when reading .yw7 files.

Based on PyWriter v5.6.1

### v0.4.2 Alpha release

- Extend the API.

Based on PyWriter v5.6.0

### v0.4.1 Alpha release

- Extend the plugin framework.

Based on PyWriter v5.6.0

### v0.4.0 Alpha release

- Implement a plugin framework.

Based on PyWriter v5.6.0

### v0.2.3 Alpha release

- Add a "Tags" entry.
- Fix a bug in enabling/disabling tree context menu commands.
- Display tags the same way as yWriter.

Based on PyWriter v5.4.3

### v0.2.2 Alpha release

Change key bindings

- promote a chapter to a part: Shift-Left
- demote a part to a chapter: Shift-Right

Based on PyWriter v5.4.3

### v0.2.1 Alpha release

Add new functions to

- promote a chapter to a part,
- demote a part to a chapter

Based on PyWriter v5.4.3

### v0.2.0 Alpha release

- Add "Open with yWriter" feature.
- Provide Windows registry setup for "Open with novelyst" in the .yw7 Explorer context menu.

Based on PyWriter v5.4.3

### v0.1.11 Development version

- Add a "Cancel Part" feature that deletes a part while keeping its chapters (Shift-Delete).

### v0.1.9 Development version

- Add some chapter and scene settings.

### v0.1.5 Development version

- Save settings for chapter renumbering as custom fields in the yw7 file.

### v0.1.4 Development version

- Renumber chapters and parts when refreshing the tree. Options and settings are stored as custom fields in the *.yw7* file.

### v0.1.1 Development version

- Apply changes of title, description and notes when changing the selection.

Based on PyWriter v5.2.0

