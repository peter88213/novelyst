""""Provide a class for viewing world element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from novelystlib.label_entry import LabelEntry
from novelystlib.basic_view import BasicView


class ElementView(BasicView):
    """A class for viewing world element properties.
    """
    _LBL_X = 10

    def __init__(self, ui, element):
        """Display element title, description and notes."""
        super(). __init__(ui, element)
        # Place a "Tags" entry inside the frame.
        if element.tags is not None:
            tags = ui.tv._LIST_SEPARATOR.join(element.tags)
        else:
            tags = ''
        self._tags = tk.StringVar(value=tags)
        self._tagsEntry = LabelEntry(self._valuesFrame, text='Tags', textvariable=self._tags)
        self._tagsEntry.pack(anchor=tk.W, pady=2)

        # Place an "AKA" entry inside the frame.
        if element.aka is not None:
            aka = element.aka
        else:
            aka = ''
        self._aka = tk.StringVar(value=aka)
        self._akaEntry = LabelEntry(self._valuesFrame, text='AKA', textvariable=self._aka)
        self._akaEntry.pack(anchor=tk.W, pady=2)

    def apply_changes(self, ui):
        """Apply changes of element title, description and notes."""
        if self._element is not None:
            if self._element.tags:
                elementTags = ui.tv._LIST_SEPARATOR.join(self._element.tags)
            else:
                elementTags = None
            newTags = self._tags.get()
            if elementTags or newTags:
                if newTags != elementTags:
                    self._element.tags = newTags.split(ui.tv._LIST_SEPARATOR)
                    ui.isModified = True
            aka = self._aka.get()
            if aka or self._element.aka:
                if self._element.aka != aka:
                    self._element.aka = aka.strip()
                    ui.isModified = True
        if ui.isModified:
            ui.tv._update_tree()

        super().apply_changes(ui)

