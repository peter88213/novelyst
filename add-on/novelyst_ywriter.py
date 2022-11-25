"""A yWriter launcher plugin for novelyst.

Adds a 'yWriter' entry to the 'File' menu to launch
yWriter with the current project.
Binds the Ctrl-Alt-Y shortcut to the launcher.

Requirements:
- Windows
- yWriter

For installation, just copy this file into the 'plugin' subdirectory
of your novelyst installation folder (e.g. ~/.pywriter/novelyst).

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

APPLICATION = 'yWriter'
KEY_YWRITER = ('<Control-Alt-y>', 'Ctrl-Alt-Y')


class Plugin:
    """yWriter launcher plugin class. 
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        
    """
    VERSION = '4.0.0'
    NOVELYST_API = '4.0'
    DESCRIPTION = 'Adds a "yWriter" entry to the "File" menu'
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
        self._ui.fileMenu.add_command(label=APPLICATION, accelerator=KEY_YWRITER[1], command=self._launch_yWriter)

        # Add a key binding.
        self._ui.root.bind(KEY_YWRITER[0], self._launch_yWriter)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.fileMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.fileMenu.entryconfig(APPLICATION, state='normal')

    def _launch_yWriter(self, event=None):
        """Launch yWriter with the current project."""
        self._ui.save_project()
        if self._ui.lock():
            os.startfile(os.path.normpath(self._ui.ywPrj.filePath))

