"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.view_controller.right_frame.basic_view import BasicView


class ChapterView(BasicView):
    """Class for viewing and editing chapter properties.
      
    Adds to the right pane:
    - A "Do not auto-number" checkbox.

    Public methods:
        apply_changes() -- Apply changes.   
        set_data() -- Update the view with element's data.
    """

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

        # 'Do not auto-number...' checkbutton.
        self._noNumber = tk.BooleanVar()
        self._noNumberButton = ttk.Checkbutton(self._elementInfoWindow, variable=self._noNumber, onvalue=True, offvalue=False)

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self._element.isTrash:
            return

        # 'Do not auto-number...' checkbutton.
        if self._update_field_bool(self._noNumber, 'Field_NoNumber'):
            self._ui.isModified = True
        super().apply_changes()

    def set_data(self, element):
        """Update the view with element's data.
        
        - Hide the info window, if the chapter ist the "trash bin". 
        - Show/hide the "Do not auto-number" button, depending on the chapter type.       
        - Configure the "Do not auto-number" button, depending on the chapter level.       
        Extends the superclass constructor.
        """
        super().set_data(element)

        # 'Do not auto-number...' checkbutton.
        noNumber = self._element.kwVar.get('Field_NoNumber', '') == '1'
        self._noNumber.set(noNumber)

        if self._element.isTrash:
            self._elementInfoWindow.pack_forget()
            return

        if not self._elementInfoWindow.winfo_manager():
            self._elementInfoWindow.pack(fill='x')

        if self._element.chType == 0:
            if self._element.chLevel == 1:
                labelText = _('Do not auto-number this part')
            else:
                labelText = _('Do not auto-number this chapter')
            self._noNumberButton.configure(text=labelText)
            if not self._noNumberButton.winfo_manager():
                self._noNumberButton.pack(anchor='w', pady=2)
        elif self._noNumberButton.winfo_manager():
            self._noNumberButton.pack_forget()

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_button_bar()

