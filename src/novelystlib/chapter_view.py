""""Provide a class for viewing and editing chapter properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
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
            self._noNumber = tk.BooleanVar(value=element.kwVar['Field_NoNumber'])
            self._noNumberCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Do not auto-number this chapter',
                                             variable=self._noNumber, onvalue=True, offvalue=False)
            self._noNumberCheckbox.pack(anchor='w', padx=5, pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """

        def update_field(tkValue, fieldname):
            """Update a custom field if changed.
            
            Positional arguments:
                tkValue -- widget variable holding a value that is not None.
                fieldname -- keyword of a custom field whose value might be None.
            """
            entry = tkValue.get()
            if self._element.kwVar[fieldname] or entry:
                if self._element.kwVar[fieldname] != entry:
                    self._element.kwVar[fieldname] = entry
                    ui.isModified = True

        if not self._element.isTrash:
            update_field(self._noNumber, 'Field_NoNumber')
        super().apply_changes(ui)

    def close(self, ui):
        """Remove widgets from the valuesWindow.
        
        Extends the superclass method.
        """
        super().close(ui)
        try:
            self._noNumberCheckbox.destroy()
        except:
            pass
