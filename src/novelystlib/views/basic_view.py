""""Provide a generic class for viewing tree element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk


class BasicView:
    """Generic class for viewing tree element properties."""
    _LBL_X = 10
    # Width of left-placed labels.

    def __init__(self, ui):
        """Display element title, description and notes."""
        self._ui = ui
        self._element = None
        self._tagsStr = ''

        # Window for element specific information.
        self._elementInfoWindow = ttk.Frame(self._ui.infoFrame)

    def show(self, element):
        """Make the widgets visible."""
        self._element = element

        # "Index card" with title and description.
        if not self._ui.indexCard.winfo_manager():
            self._ui.indexCard.pack(expand=False, fill=tk.BOTH)

        # Window for element specific information.
        self._ui.infoFrame.pack(after=self._ui.indexCard, expand=False, fill=tk.BOTH)
        self._elementInfoWindow.pack(fill=tk.X)

        # Notes entry (if any).
        if hasattr(self._element, 'notes'):
            self._ui.notesWindow.pack(after=self._ui.infoFrame, expand=True, fill=tk.BOTH)

    def set_data(self, element):
        """Update the widgets with element's data."""
        self._tagsStr = ''
        self._element = element
        if self._element is not None:

            # Title entry.
            if self._element.title is not None:
                self._ui.elementTitle.set(self._element.title)
            else:
                self._ui.elementTitle.set('')

            # Description entry.
            self._ui.descWindow.clear()
            self._ui.descWindow.set_text(self._element.desc)

            # Notes entry (if any).
            self._ui.notesWindow.clear()
            if hasattr(self._element, 'notes'):
                self._ui.notesWindow.set_text(self._element.notes)

    def _update_field_str(self, tkValue, fieldname):
        """Update a custom field and return True if changed. 
               
        Positional arguments:
            tkValue -- widget variable holding a string that is not None.
            fieldname -- keyword of a custom field whose value might be None.
        """
        entry = tkValue.get()
        if self._element.kwVar.get(fieldname, None) or entry:
            if self._element.kwVar.get(fieldname, None) != entry:
                self._element.kwVar[fieldname] = entry
                return True
        return False

    def _update_field_bool(self, tkValue, fieldname):
        """Update a custom field and return True if changed.
        
        Positional arguments:
            tkValue -- widget variable holding a boolean value.
            fieldname -- keyword of a custom field.
            
        Custom field value convention:
        '1' means True
        None means False 
        """
        entry = tkValue.get()
        if entry:
            value = '1'
        else:
            value = None
        if self._element.kwVar.get(fieldname, None) or value:
            if self._element.kwVar.get(fieldname, None) != value:
                self._element.kwVar[fieldname] = value
                return True
        return False

    def apply_changes(self):
        """Apply changes of element title, description and notes."""
        if self._element is not None:

            # Title entry.
            title = self._ui.elementTitle.get()
            if title or self._element.title:
                if self._element.title != title:
                    self._element.title = title.strip()
                    self._ui.isModified = True

            # Description entry.
            if self._ui.descWindow.hasChanged:
                desc = self._ui.descWindow.get_text()
                if desc or self._element.desc:
                    if self._element.desc != desc:
                        self._element.desc = desc
                        self._ui.isModified = True

            # Notes entry (if any).
            if self._ui.notesWindow.hasChanged:
                notes = self._ui.notesWindow.get_text()
                if hasattr(self._element, 'notes'):
                    if notes or self._element.notes:
                        if self._element.notes != notes:
                            self._element.notes = notes
                            self._ui.isModified = True

        if self._ui.isModified:
            self._ui.tv.update_prjStructure()

    def hide(self):
        """Apply changes and clear the text boxes."""
        self._ui.elementTitle.set('')
        self._ui.descWindow.delete('1.0', tk.END)
        self._ui.notesWindow.pack_forget()
        self._ui.infoFrame.pack_forget()
        self._elementInfoWindow.pack_forget()

