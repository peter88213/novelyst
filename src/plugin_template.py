"""Plugin template for novelyst.

Compatibility: novelyst v0.6.0 API 
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import messagebox

APPLICATION = 'Example'
PLUGIN = f'{APPLICATION} plugin v@release'


class Plugin():
    """Example plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        
    """

    def __init__(self, ui):
        """Add a submenu to the main menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui

        # Create a submenu
        self._pluginMenu = tk.Menu(self._ui.mainMenu, title='my title', tearoff=0)
        self._ui.mainMenu.add_cascade(label=APPLICATION, menu=self._pluginMenu)
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')
        self._pluginMenu.add_command(label='Say Hello', underline=0, command=self._hello)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='normal')

    def _hello(self):
        message = 'Hello, world!'
        messagebox.showinfo(PLUGIN, message)
