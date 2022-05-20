""""Provide a class for viewing tree element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from novelystlib.label_entry import LabelEntry


class ElementView:
    """A generic class for viewing tree element properties.
    """

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

            # Place a "Tags" entry (if any) inside the frame.
            if hasattr(element, 'tags'):
                if element.tags is not None:
                    tags = ui.tv._LIST_SEPARATOR.join(element.tags)
                else:
                    tags = ''
                self._tags = tk.StringVar(value=tags)
                self._tagsEntry = LabelEntry(self._valuesFrame, text='Tags', textvariable=self._tags)
                self._tagsEntry.pack(anchor=tk.W, pady=2)

            # Place an "AKA" entry (if any) inside the frame.
            if hasattr(element, 'aka'):
                if element.aka is not None:
                    aka = element.aka
                else:
                    aka = ''
                self._aka = tk.StringVar(value=aka)
                self._akaEntry = LabelEntry(self._valuesFrame, text='AKA', textvariable=self._aka)
                self._akaEntry.pack(anchor=tk.W, pady=2)

            # Set element's notes (if any).
            if hasattr(element, 'notes'):
                if element.notes is not None:
                    ui.notesWindow.insert(tk.END, element.notes)

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
            if hasattr(self._element, 'tags'):
                if self._element.tags:
                    elementTags = ui.tv._LIST_SEPARATOR.join(self._element.tags)
                else:
                    elementTags = None
                newTags = self._tags.get()
                if elementTags or newTags:
                    if newTags != elementTags:
                        self._element.tags = newTags.split(ui.tv._LIST_SEPARATOR)
                        ui.isModified = True
            if hasattr(self._element, 'aka'):
                aka = self._aka.get()
                if aka or self._element.aka:
                    if self._element.aka != aka:
                        self._element.aka = aka.strip()
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
