#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk

from pywriter.ui.main_tk import MainTk
from pywriter.yw.yw7_file import Yw7File


class NovelystTk(MainTk):
    """A tkinter GUI class for yWriter project processing.

    Show titles, descriptions, and contents in a text box.
    """

    def reset_chapters(self):

        for child in self.chapterTree.get_children(''):
            self.chapterTree.delete(child)

    def set_chapters(self):
        self.reset_chapters()

        for chId in self.ywPrj.srtChapters:
            self.chapterTree.insert('', 'end', chId, text=self.ywPrj.chapters[chId].title)

    def reset_scenes(self):

        for child in self.sceneTree.get_children(''):
            self.sceneTree.delete(child)

    def set_scenes(self, event):
        chId = self.chapterTree.identify('item', event.x, event.y)
        self.reset_scenes()

        for scId in self.ywPrj.chapters[chId].srtScenes:
            self.sceneTree.insert('', 'end', scId, text=self.ywPrj.scenes[scId].title)

    def set_chapter_info(self, event):
        chId = self.chapterTree.identify('item', event.x, event.y)

        if self.ywPrj.chapters[chId].desc:
            text = self.ywPrj.chapters[chId].desc

        else:
            text = '(No chapter description available)'

        self.chapterInfoWin.delete('1.0', tk.END)
        self.chapterInfoWin.insert(tk.END, text)

    def set_scene_info(self, event):
        scId = self.sceneTree.identify('item', event.x, event.y)

        if self.ywPrj.scenes[scId].desc:
            text = self.ywPrj.scenes[scId].desc

        else:
            text = '(No scene description available)'

        self.sceneInfoWin.delete('1.0', tk.END)
        self.sceneInfoWin.insert(tk.END, text)

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.root.geometry("800x500")

        # Create an application window with a chapter and a scene frame.

        self.appWindow = tk.PanedWindow(self.mainWindow, sashrelief=tk.RAISED)
        self.appWindow.pack(expand=True, fill='both')
        self.chapterFrame = tk.Frame(self.appWindow)
        self.appWindow.add(self.chapterFrame)
        self.sceneFrame = tk.Frame(self.appWindow)
        self.appWindow.add(self.sceneFrame)

        # Create a chapter window with a chapter tree and an info label..

        self.chapterWindow = tk.PanedWindow(self.chapterFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.chapterWindow.pack(expand=True, fill='both')
        self.chapterTree = ttk.Treeview(self.chapterWindow)
        self.chapterWindow.add(self.chapterTree)
        self.chapterInfoWin = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1)
        self.chapterWindow.add(self.chapterInfoWin)

        self.chapterTree.bind('<1>', self.set_scenes)
        self.chapterTree.bind('<Double-1>', self.set_chapter_info)

        # Create a scene window with a scene tree and an info label..

        self.sceneWindow = tk.PanedWindow(self.sceneFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.sceneWindow.pack(expand=True, fill='both')
        self.sceneTree = ttk.Treeview(self.sceneWindow)
        self.sceneWindow.add(self.sceneTree)
        self.sceneInfoWin = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1)
        self.sceneWindow.add(self.sceneInfoWin)

        self.sceneTree.bind('<Double-1>', self.set_scene_info)

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
        self.set_chapters()
        return fileName

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        self.reset_chapters()
        self.reset_scenes()
        self.chapterInfoWin.delete('1.0', tk.END)
        self.sceneInfoWin.delete('1.0', tk.END)
        super().close_project()
