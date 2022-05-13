""""Provide a class for viewing and editing scene properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
from novelystlib.element_view import ElementView
from novelystlib.label_combo import LabelCombo


class SceneView(ElementView):
    """A class for viewing and editing scene properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)

        # "Append to previous scene" checkbox.
        self._appendToPrev = tk.BooleanVar(value=element.appendToPrev)
        self._appendToPrevCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Append to previous scene',
                                         variable=self._appendToPrev, onvalue=True, offvalue=False)
        self._appendToPrevCheckbox.pack(anchor='w', padx=5, pady=2)

        # "Notes" window.
        if element.sceneNotes is not None:
            ui.notesWindow.insert(tk.END, element.sceneNotes)

        # "Scene viewpoint" combobox.
        charList = []
        for crId in ui.ywPrj.srtCharacters:
            charList.append(ui.ywPrj.characters[crId].title)
        if element.characters:
            vp = ui.ywPrj.characters[element.characters[0]].title
        else:
            vp = ''
        self._viewpoint = tk.StringVar(value=vp)
        self._characterCombobox = LabelCombo(ui._valuesWindow, text='Viewpoint', textvariable=self._viewpoint, values=charList)
        self._characterCombobox.pack(anchor='w', padx=5, pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        # Append to previous scene.
        appendToPrev = self._appendToPrev.get()
        if self._element.appendToPrev or appendToPrev:
            if self._element.appendToPrev != appendToPrev:
                self._element.appendToPrev = appendToPrev
                ui.isModified = True

        # Scene notes.
        notes = ui.notesWindow.get('1.0', tk.END).strip(' \n')
        if notes or self._element.sceneNotes:
            if self._element.sceneNotes != notes:
                self._element.sceneNotes = notes
                ui.isModified = True

        # Scene viewpoint.
        option = self._characterCombobox.current()
        if self._element.characters:
            oldVpId = self._element.characters[0]
        else:
            oldVpId = None
        if option >= 0:
            newVpId = ui.ywPrj.srtCharacters[option]
            if oldVpId:
                if newVpId != oldVpId:
                    try:
                        self._element.characters.remove(newVpId)
                    except:
                        pass
                    self._element.characters.insert(0, newVpId)
                    ui.isModified = True
            else:
                self._element.characters = []
                self._element.characters.append(newVpId)
                ui.isModified = True

        super().apply_changes(ui)

    def close(self, ui):
        """Remove widgets from the valuesWindow.
        
        Extends the superclass method.
        """
        super().close(ui)
        self._appendToPrevCheckbox.destroy()
        self._characterCombobox.destroy()
