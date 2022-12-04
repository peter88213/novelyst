""""Provide a tkinter based class for viewing and editing "Notes" scene properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from pywriter.pywriter_globals import *
from novelystlib.views.basic_view import BasicView
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar


class NotesSceneView(BasicView):
    """Class for viewing and editing "Notes" scene properties.
       
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """

    def __init__(self, ui):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui -- NovelystTk: Reference to the user interface.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        # 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

        super().set_data(element)

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        super().apply_changes()

