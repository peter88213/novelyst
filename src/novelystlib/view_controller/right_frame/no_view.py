"""Provide a class for clearing the right frame.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from novelystlib.view_controller.right_frame.basic_view import BasicView


class NoView(BasicView):
    """Class for clearing the right frame.
    
        Public methods:
        show() -- Remove the "index card" with title and description.
        hide() -- Clear the text boxes and restore the "Index card".
        set_data() -- Do nothing.
        apply_changes() -- Do nothing.   
    """

    def __init__(self, ui):
        """Initialize the instance variable.

        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.
        
        Overrides the superclass constructor.
        """
        self._ui = ui

    def show(self, element):
        """Remove the "index card" with title and description.
        
        Overrides the superclass method.
        """
        if self._ui.indexCard.winfo_manager():
            self._ui.indexCard.pack_forget()

    def hide(self):
        """Clear the text boxes and restore the "Index card".

        Overrides the superclass method.
        """
        self._ui.elementTitle.set('')
        self._ui.descWindow.delete('1.0', tk.END)
        self._ui.notesWindow.pack_forget()
        self._ui.infoFrame.pack_forget()

        # "Index card" with title and description.
        if not self._ui.indexCard.winfo_manager():
            self._ui.indexCard.pack(expand=False, fill=tk.BOTH)

    def set_data(self, element):
        """Do nothing.
        
        Overrides the superclass method.
        """
        return

    def apply_changes(self):
        """Do nothing.
        
        Overrides the superclass method.
        """
        return

