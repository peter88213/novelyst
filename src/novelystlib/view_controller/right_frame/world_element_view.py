"""Provide a tkinter based class for viewing world element properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.view_controller.right_frame.basic_view import BasicView
from novelystlib.widgets.my_string_var import MyStringVar


class WorldElementView(BasicView):
    """Class for viewing world element properties.
    
    Adds to the right pane:
    - An "Aka" entry.
    - A "Tags" entry.   
     
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """
    _INDEXCARD = True
    _ELEMENT_INFO = True
    _NOTES = False
    _BUTTONBAR = True

    def __init__(self, ui, parent):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.
            parent -- Parent widget to display this widget.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, parent)

        self._fullNameFrame = ttk.Frame(self._elementInfoWindow)
        self._fullNameFrame.pack(anchor=tk.W, fill=tk.X)

        # 'AKA' entry.
        self._aka = MyStringVar()
        self._akaEntry = LabelEntry(self._elementInfoWindow, text=_('AKA'), textvariable=self._aka, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

        # 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        # 'AKA' entry.
        self._aka.set(self._element.aka)

        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

    def apply_changes(self):
        """Apply changes of element title, description and notes."""

        # 'AKA' entry.
        aka = self._aka.get()
        if aka or self._element.aka:
            if self._element.aka != aka:
                self._element.aka = aka.strip()
                self._ui.isModified = True
        if self._ui.isModified:
            self._ui.tv.update_prj_structure()

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        super().apply_changes()

