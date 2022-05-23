""""Provide a class for viewing and editing chapter properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
from novelystlib.element_view import ElementView


class ChapterView(ElementView):
    """A class for viewing and editing chapter properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)
        if not element.isTrash:
            noNumber = element.kwVar['Field_NoNumber'] == '1'
            self._noNumber = tk.BooleanVar(value=noNumber)
            self._noNumberCheckbox = ttk.Checkbutton(self._valuesFrame, text='Do not auto-number this chapter',
                                             variable=self._noNumber, onvalue=True, offvalue=False)
            self._noNumberCheckbox.pack(anchor='w', pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """

        if not self._element.isTrash:
            if self._update_field_bool(self._noNumber, 'Field_NoNumber'):
                ui.isModified = True
        super().apply_changes(ui)

