"""Provide a tkinter Rich Text box class with a ttk scrollbar and a change flag.

Copyright (c) 2023 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class TextBox(tk.Text):
    """A text box with a ttk scrollbar and a change flag.
    """

    def __init__(self, master=None, **kw):
        """Define some tags for novelyst-specific colors.
        
        Copied from tkinter.scrolledtext and modified (use ttk widgets).
        Extends the supeclass constructor.
        """
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        kw.update({'yscrollcommand': self.vbar.set})
        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

        # This part is project-specific:
        self.hasChanged = False
        self.bind('<KeyRelease>', self._on_edit)

    def _on_edit(self, event=None):
        """Event handler to indicate changes."""
        self.hasChanged = True

    def get_text(self):
        return self.get('1.0', tk.END).strip(' \n')

    def set_text(self, text):
        self.clear()
        if text:
            self.insert(tk.END, text)
            self.edit_reset()
            # this is to prevent the user from clearing the box with Ctrl-Z

    def clear(self):
        self.delete('1.0', tk.END)
        self.hasChanged = False

