""""Provide a generic class for viewing tree element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk


class BasicView:
    """Generic class for viewing tree element properties."""
    _LBL_X = 10

    def __init__(self, ui, element):
        """Display element title, description and notes."""

        # Place a frame that can be easily deleted into the Values window.
        self._valuesFrame = tk.Frame(ui._valuesWindow)
        self._valuesFrame.pack(fill=tk.X)
        self._element = element
        if element is not None:
            # Set element's title.
            if element.title is not None:
                ui.elementTitle.set(element.title)

            # Set element's description.
            if element.desc is not None:
                ui.descWindow.insert(tk.END, element.desc)

            # Set element's notes (if any).
            if hasattr(element, 'notes'):
                if element.notes is not None:
                    ui.notesWindow.insert(tk.END, element.notes)

    def _update_field_str(self, tkValue, fieldname):
        """Update a custom field and return True if changed. 
               
        Positional arguments:
            tkValue -- widget variable holding a string that is not None.
            fieldname -- keyword of a custom field whose value might be None.
        """
        entry = tkValue.get()
        if self._element.kwVar[fieldname] or entry:
            if self._element.kwVar[fieldname] != entry:
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
        if self._element.kwVar[fieldname] or value:
            if self._element.kwVar[fieldname] != value:
                self._element.kwVar[fieldname] = value
                return True
        return False

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
        if ui.isModified:
            ui.tv._update_tree()

    def close(self, ui):
        """Apply changes and clear the text boxes."""
        self.apply_changes(ui)
        ui.elementTitle.set('')
        ui.descWindow.delete('1.0', tk.END)
        ui.notesWindow.delete('1.0', tk.END)
        self._valuesFrame.destroy()
        del self
