"""Provide a scene editor plugin for novelyst.

Compatibility: novelyst v0.14.0 API 
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

APPLICATION = 'Scene Editor'
PLUGIN = f'{APPLICATION} plugin v@release'

KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')
KEY_APPLY_CHANGES = ('<Control-s>', 'Ctrl-S')


class Plugin:
    """novelyst scene editor plugin class.
    
    Public methods:
        on_quit() -- apply changes before closing the editor windows.       
    """

    def __init__(self, ui):
        """Add a submenu to the main menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui

        # Add the "Edit" command to novelyst's "Scene" menu.
        self._ui.sceneMenu.add_separator()
        self._ui.sceneMenu.add_command(label='Edit', underline=0, command=self._edit_scene)
        self._ui.tv.tree.bind('<Double-1>', self._edit_scene)
        self.sceneEditors = {}

    def _edit_scene(self, event=None):
        """Create a scene editor window with a menu bar, a text box, and a status bar."""
        if self._ui.isLocked:
            messagebox.showinfo(PLUGIN, 'Cannot edit scenes, because the project is locked.')
            return

        try:
            nodeId = self._ui.tv.tree.selection()[0]
            if nodeId.startswith(self._ui.tv._SC):
                # A scene is selected
                scId = nodeId[2:]
                if scId in self.sceneEditors and self.sceneEditors[scId].isOpen:
                    self.sceneEditors[scId].lift()
                    return

                self.sceneEditors[scId] = SceneEditor(self._ui, scId)
        except IndexError:
            # Nothing selected
            pass

    def on_quit(self, event=None):
        """Close all open scene editor windows."""
        for scId in self.sceneEditors:
            if self.sceneEditors[scId].isOpen:
                self.sceneEditors[scId].on_quit()


class SceneEditor:
    """A separate scene editor window with a menu bar, a text box, and a status bar."""

    def __init__(self, ui, scId):
        self._ui = ui
        self._scene = self._ui.ywPrj.scenes[scId]

        # Create an independent editor window.
        self._editWindow = tk.Toplevel()
        self._editWindow.title(f'{self._ui.ywPrj.title} - Scene ID {scId} ({self._scene.title})')

        # Add a main menu bar to the editor window.
        self._mainMenu = tk.Menu(self._editWindow)

        # Add a "File" Submenu to the editor window.
        self._fileMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='File', underline=0, menu=self._fileMenu)
        self._fileMenu.add_command(label='Apply changes', underline=0, accelerator=KEY_APPLY_CHANGES[1], command=self._apply_changes)
        self._fileMenu.add_command(label='Exit', underline=1, accelerator=KEY_QUIT_PROGRAM[1], command=self.on_quit)
        self._editWindow.config(menu=self._mainMenu)

        # Add a text editor with scrollbar to the editor window.
        self._sceneEditor = TextBox(self._editWindow, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=25, width=60, padx=5, pady=5)
        self._sceneEditor.pack(expand=True, fill=tk.BOTH)

        # Add a status bar to the editor window.
        self._statusBar = tk.Label(self._editWindow, text='', anchor='w', padx=5, pady=2)
        self._statusBar.pack(expand=False, fill='both')

        # Load the scene content into the text editor.
        if self._ui.ywPrj.scenes[scId].sceneContent:
            self._sceneEditor.insert(tk.END, self._scene.sceneContent)

        # Event bindings.
        self._editWindow.bind(KEY_APPLY_CHANGES[0], self._apply_changes)
        self._editWindow.bind(KEY_QUIT_PROGRAM[0], self.on_quit)
        self._editWindow.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.isOpen = True

    def show_status(self, message=None):
        """Display a message on the status bar."""
        self._statusBar.config(text=message)

    def _apply_changes(self, event=None):
        """Write the editor content to the project, if possible."""
        sceneText = self._sceneEditor.get('1.0', tk.END).strip(' \n')
        if sceneText or self._scene.sceneContent:
            if self._scene.sceneContent != sceneText:
                if self._ui.isLocked:
                    messagebox.showinfo(PLUGIN, 'Cannot apply scene changes, because the project is locked.')
                    return

                self._scene.sceneContent = sceneText
                self._ui.isModified = True

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        sceneText = self._sceneEditor.get('1.0', tk.END).strip(' \n')
        if sceneText or self._scene.sceneContent:
            if self._scene.sceneContent != sceneText:
                if self._ui.ask_yes_no('Apply scene changes?'):
                    if self._ui.isLocked:
                        if self._ui.ask_yes_no('Cannot apply scene changes, because the project is locked.\nUnlock and apply changes?'):
                            self._ui.unlock()
                            self._scene.sceneContent = sceneText
                            self._ui.isModified = True
                    else:
                        self._scene.sceneContent = sceneText
                        self._ui.isModified = True
        self._editWindow.destroy()
        self.isOpen = False

    def lift(self):
        """Bring window to the foreground"""
        self._editWindow.lift()


class TextBox(scrolledtext.ScrolledText):
    """If a more sophisticated text box is needed, create it here."""
