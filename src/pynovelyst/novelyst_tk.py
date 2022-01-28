#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk

from pywriter.ui.main_tk import MainTk
from pywriter.yw.yw7_file import Yw7File


class NovelystTk(MainTk):
    """A tkinter GUI class for yWriter project processing.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.root.geometry("800x500")

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.chapterMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Chapter', menu=self.chapterMenu)
        self.mainMenu.entryconfig('Chapter', state='disabled')
        self.sceneMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Scene', menu=self.sceneMenu)
        self.mainMenu.entryconfig('Scene', state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Chapter', state='disabled')
        self.mainMenu.entryconfig('Scene', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Chapter', state='normal')
        self.mainMenu.entryconfig('Scene', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self.ywPrj = Yw7File(fileName)
        message = self.ywPrj.read()

        if message.startswith('ERROR'):
            self.close_project()
            self.statusBar.config(text=message)
            return ''

        if self.ywPrj.title:
            titleView = self.ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self.ywPrj.author:
            authorView = self.ywPrj.author

        else:
            authorView = 'Unknown author'

        self.titleBar.config(text=titleView + ' by ' + authorView)
        self.enable_menu()
        return fileName

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super().close_project()
