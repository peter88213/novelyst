""""Provide a class for viewing tree element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk


class ElementView:
    """A generic class for viewing tree element properties.
    """

    def __init__(self, ui, element):
        """Display element title, description and notes."""
        self._element = element
        title = ''
        desc = ''
        notes = ''
        if element is not None:
            if element.title is not None:
                title = element.title
            if element.desc is not None:
                desc = element.desc
            if hasattr(element, 'sceneNotes'):
                if element.sceneNotes is not None:
                    notes = element.sceneNotes
            elif hasattr(element, 'notes'):
                if element.notes is not None:
                    notes = element.notes
        ui.elementTitle.set(title)
        ui.descWindow.insert(tk.END, desc)
        ui.notesWindow.insert(tk.END, notes)

    def apply_changes(self, ui):
        """Apply changes of element title, description and notes."""
        if self._element is not None:
            title = ui.elementTitle.get()
            if title or self._element.title:
                if self._element.title != title:
                    self._element.title = title.strip()
                    ui.isModified = True
            desc = ui.descWindow.get('1.0', tk.END).strip(' \n')
            if desc or self._element.desc:
                if self._element.desc != desc:
                    self._element.desc = desc
                    ui.isModified = True
            notes = ui.notesWindow.get('1.0', tk.END).strip(' \n')
            if hasattr(self._element, 'notes'):
                if notes or self._element.notes:
                    if self._element.notes != notes:
                        self._element.notes = notes
                        ui.isModified = True

    def close(self, ui):
        """Apply changes and clear the text boxes."""
        self.apply_changes(ui)
        ui.elementTitle.set('')
        ui.descWindow.delete('1.0', tk.END)
        ui.notesWindow.delete('1.0', tk.END)
        del self
