"""Plugin template for novelyst.

Adds an 'Example' entry to the 'Tools' menu to open a submenu.
The 'Say Hello' command in this submenu opens a message box.

For installation, just copy this file into the 'plugin' subdirectory
of your novelyst installation folder (e.g. ~/.pywriter/novelyst).

Compatibility: novelyst v1.0 API 
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import messagebox

APPLICATION = 'Example plugin'


class Plugin():
    """Example plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        
    """
    VERSION = '@release'
    NOVELYST_API = '1.0'
    DESCRIPTION = 'Example plugin'
    URL = 'https://peter88213.github.io/novelyst'

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui

        # Create a submenu
        self._pluginMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._ui.toolsMenu.add_cascade(label=APPLICATION, menu=self._pluginMenu)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._pluginMenu.add_command(label='Say Hello', underline=0, command=self._hello)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def _hello(self):
        message = 'Hello, world!'
        messagebox.showinfo(APPLICATION, message)
