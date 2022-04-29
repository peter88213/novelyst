""""Provide a class for viewing and editing scene properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
from novelystlib.element_view import ElementView


class SceneView(ElementView):
    """A class for viewing and editing scene properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)
        self._appendToPrev = tk.BooleanVar(value=element.appendToPrev)
        self._appendToPrevCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Append to previous scene',
                                         variable=self._appendToPrev, onvalue=True, offvalue=False)
        self._appendToPrevCheckbox.pack(anchor='w', padx=5, pady=2)
        if element.sceneNotes is not None:
            ui.notesWindow.insert(tk.END, element.sceneNotes)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        appendToPrev = self._appendToPrev.get()
        if self._element.appendToPrev or appendToPrev:
            if self._element.appendToPrev != appendToPrev:
                self._element.appendToPrev = appendToPrev
                ui.isModified = True
        notes = ui.notesWindow.get('1.0', tk.END).strip(' \n')
        if notes or self._element.sceneNotes:
            if self._element.sceneNotes != notes:
                self._element.sceneNotes = notes
                ui.isModified = True
        super().apply_changes(ui)

    def close(self, ui):
        """Remove widgets from the valuesWindow.
        
        Extends the superclass method.
        """
        super().close(ui)
        self._appendToPrevCheckbox.destroy()
