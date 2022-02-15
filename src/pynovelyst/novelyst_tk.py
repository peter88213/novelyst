#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk

from pywriter.pywriter_globals import ERROR
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
        self._root.geometry("800x500")
        self._chapterMenu = None 
        self._sceneMenu = None

        # Create an application window with a chapter and a scene frame.

        self._appWindow = tk.PanedWindow(self._mainWindow, sashrelief=tk.RAISED)
        self._appWindow.pack(expand=True, fill='both')
        self._chapterFrame = tk.Frame(self._appWindow)
        self._appWindow.add(self._chapterFrame)
        self._sceneFrame = tk.Frame(self._appWindow)
        self._appWindow.add(self._sceneFrame)

        # Create a chapter window with a chapter tree and an info box.

        self._chapterWindow = tk.PanedWindow(self._chapterFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._chapterWindow.pack(expand=True, fill='both')
        self._chapterTree = ttk.Treeview(self._chapterWindow, selectmode='browse', columns=['Title', 'Scenes'])
        self._chapterTree['columns'] = ('Scenes')
        self._chapterTree.heading('Scenes', text= 'Scenes')
        
        
        self._chapterWindow.add(self._chapterTree)
        self._chapterInfoWin = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1,  height=4, width=10)
        self._chapterWindow.add(self._chapterInfoWin)

        self._chapterTree.bind('<<TreeviewSelect>>', self._on_chapter_select)

        # Create a scene window with a scene tree and an info box.

        self._sceneWindow = tk.PanedWindow(self._sceneFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._sceneWindow.pack(expand=True, fill='both')
        self._sceneTree = ttk.Treeview(self._sceneWindow, selectmode='browse')
        self._sceneTree['columns'] = ('Words', 'Viewpoint')
        self._sceneTree.heading('Words', text= 'Words')
        self._sceneTree.heading('Viewpoint', text= 'Viewpoint')
        
        self._sceneWindow.add(self._sceneTree)
        self._sceneInfoWin = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1,  height=4, width=10)
        self._sceneWindow.add(self._sceneInfoWin)

        self._sceneTree.bind('<<TreeviewSelect>>', self._on_scene_select)

    def _on_chapter_select(self, event):
        chId = self._chapterTree.selection()[0]
        self._set_scenes(chId)
        self._set_chapter_info(chId)

    def _on_scene_select(self, event):
        scId = self._sceneTree.selection()[0]
        self._set_scene_info(scId)

    def _reset_chapters(self):

        for child in self._chapterTree.get_children(''):
            self._chapterTree.delete(child)

    def _set_chapters(self):
        self._reset_chapters()

        for chId in self._ywPrj.srtChapters:            
            display = [] 
            display.append(len(self._ywPrj.chapters[chId].srtScenes))            
            self._chapterTree.insert('', 'end', chId, text=self._ywPrj.chapters[chId].title, values=display)

    def _reset_scenes(self):

        for child in self._sceneTree.get_children(''):
            self._sceneTree.delete(child)

        self._sceneInfoWin.delete('1.0', tk.END)

    def _set_scenes(self, chId):
        self._reset_scenes()

        for scId in self._ywPrj.chapters[chId].srtScenes:
            display = []
            display.append(self._ywPrj.scenes[scId].wordCount)
            
            try:
                display.append(self._ywPrj.characters[self._ywPrj.scenes[scId].characters[0]].title)
                
            except IndexError:
                display.append('N/A')
                
            self._sceneTree.insert('', 'end', scId, text=self._ywPrj.scenes[scId].title, values=display)

    def _set_chapter_info(self, chId):

        if self._ywPrj.chapters[chId].desc is not None:
            text = self._ywPrj.chapters[chId].desc

        else:
            text = ''

        self._chapterInfoWin.delete('1.0', tk.END)
        self._chapterInfoWin.insert(tk.END, text)

    def _set_scene_info(self, scId):

        if self._ywPrj.scenes[scId].desc is not None:
            text = self._ywPrj.scenes[scId].desc

        else:
            text = ''

        self._sceneInfoWin.delete('1.0', tk.END)
        self._sceneInfoWin.insert(tk.END, text)

    def _extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self._chapterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Chapter', menu=self._chapterMenu)
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._sceneMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Scene', menu=self._sceneMenu)
        self._mainMenu.entryconfig('Scene', state='disabled')

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._mainMenu.entryconfig('Scene', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('Chapter', state='normal')
        self._mainMenu.entryconfig('Scene', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self._ywPrj = Yw7File(fileName)
        message = self._ywPrj.read()

        if message.startswith(ERROR):
            self._close_project()
            self._statusBar.config(text=message)
            return ''

        if self._ywPrj.title:
            titleView = self._ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self._ywPrj.author:
            authorView = self._ywPrj.author

        else:
            authorView = 'Unknown author'

        self._titleBar.config(text=f'{titleView} by {authorView}')
        self._enable_menu()
        self._set_chapters()
        return fileName

    def _close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        self._reset_chapters()
        self._reset_scenes()
        self._chapterInfoWin.delete('1.0', tk.END)
        self._sceneInfoWin.delete('1.0', tk.END)
        super()._close_project()
