"""A yWriter service plugin for novelyst.

Adds a 'yWriter' entry to the 'File' menu to launch
yWriter with the current project.
Binds the Ctrl-Alt-Y shortcut to the launcher.

Adds a 'Remove custom fields' entry to the 'File' menu to 
remove all the novelyst specific fields from the project file.

Requirements:
- Windows
- yWriter

For installation, just copy this file into the 'plugin' subdirectory
of your novelyst installation folder (e.g. ~/.pywriter/novelyst).

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

APPLICATION = 'yWriter'
KEY_YWRITER = ('<Control-Alt-y>', 'Ctrl-Alt-Y')


def reset_custom_variables(prjFile):
    """Set custom keyword variables of a File instance to an empty string.
    
    Positional arguments:
        prjFile -- File instance to process.
    
    Thus the Yw7File.write() method will remove the associated custom fields
    from the .yw7 XML file. 
    Return True, if a keyword variable has changed (i.e information is lost).
    """
    hasChanged = False
    for field in prjFile.PRJ_KWVAR:
        if prjFile.novel.kwVar.get(field, None):
            prjFile.novel.kwVar[field] = ''
            hasChanged = True
    for chId in prjFile.novel.chapters:
        # Deliberatey not iterate srtChapters: make sure to get all chapters.
        for field in prjFile.CHP_KWVAR:
            if prjFile.novel.chapters[chId].kwVar.get(field, None):
                prjFile.novel.chapters[chId].kwVar[field] = ''
                hasChanged = True
    for scId in prjFile.novel.scenes:
        for field in prjFile.SCN_KWVAR:
            if prjFile.novel.scenes[scId].kwVar.get(field, None):
                prjFile.novel.scenes[scId].kwVar[field] = ''
                hasChanged = True
    for crId in prjFile.novel.characters:
        for field in prjFile.CRT_KWVAR:
            if prjFile.novel.characters[crId].kwVar.get(field, None):
                prjFile.novel.characters[crId].kwVar[field] = ''
                hasChanged = True
    for lcId in prjFile.novel.locations:
        for field in prjFile.LOC_KWVAR:
            if prjFile.novel.locations[lcId].kwVar.get(field, None):
                prjFile.novel.locations[lcId].kwVar[field] = ''
                hasChanged = True
    for itId in prjFile.novel.items:
        for field in prjFile.ITM_KWVAR:
            if prjFile.novel.items[itId].kwVar.get(field, None):
                prjFile.novel.items[itId].kwVar[field] = ''
                hasChanged = True
    for pnId in prjFile.novel.projectNotes:
        for field in prjFile.PNT_KWVAR:
            if prjFile.novel.projectnotes[pnId].kwVar.get(field, None):
                prjFile.novel.projectnotes[pnId].kwVar[field] = ''
                hasChanged = True
    return hasChanged


class Plugin:
    """yWriter launcher plugin class. 
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        
    """
    VERSION = '4.10.0'
    NOVELYST_API = '4.10'
    DESCRIPTION = 'yWriter service plugin'
    URL = 'https://peter88213.github.io/novelyst'

    def install(self, ui):
        """Add a 'yWriter' entry to the 'File' menu and bind a key shortcut.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        if os.name != 'nt':
            raise ValueError('This plugin is only for Windows')

        self._ui = ui

        # Create a menu entry.
        self._ui.fileMenu.add_separator()
        self._ui.fileMenu.add_command(label='Remove custom fields', command=self._remove_custom_fields)
        self._ui.fileMenu.add_command(label=APPLICATION, accelerator=KEY_YWRITER[1], command=self._launch_yWriter)

        # Add a key binding.
        self._ui.root.bind(KEY_YWRITER[0], self._launch_yWriter)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.fileMenu.entryconfig(APPLICATION, state='disabled')
        self._ui.fileMenu.entryconfig('Remove custom fields', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.fileMenu.entryconfig(APPLICATION, state='normal')
        self._ui.fileMenu.entryconfig('Remove custom fields', state='normal')

    def _launch_yWriter(self, event=None):
        """Launch yWriter with the current project."""
        self._ui.save_project()
        if self._ui.lock():
            os.startfile(os.path.normpath(self._ui.ywPrj.filePath))

    def _remove_custom_fields(self, event=None):
        """Remove custom fields from the .yw7 file and save the project.
        
        Remove custom fields to restore a "yWriter only" file
        -----------------------------------------------------
        novelyst customizes the .yw7 file format in a compatible way. 
        However, if you don't want to use your project witn novelyst any more, 
        you can "clean up" your project, removing all custom extensions 
        from the project file, with "File > Remove custom fields". 
        You will get a warning before novelyst-only data is deleted.

        Warning: This command will remove the novelyst specific project settings, 
        such as auto-numbering mode and renamings. This will also remove 
        special scene properties such as arc and style assignments.
        """
        if self._ui.prjFile is not None:
            if self._ui.ask_yes_no('Remove novelyst project settings and save?'):
                self._ui.tv.tree.selection_set('')
                self._ui.view_nothing()
                if reset_custom_variables(self._ui.prjFile):
                    try:
                        self._ui.prjFile.write()
                    except Exception as ex:
                        self.set_info_how(f'!{str(ex)}')
                    else:
                        self._ui.reload_project()

