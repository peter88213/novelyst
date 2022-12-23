"""Provide a tkinter based combobox with a label.

Copyright (c) 2022 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class LabelCombo(ttk.Frame):
    """Combobox with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, values, lblWidth=10):
        super().__init__(parent)
        self.pack(fill=tk.X)
        self._label = ttk.Label(self, text=text, anchor=tk.W, width=lblWidth)
        self._label.pack(side=tk.LEFT)
        self._combo = ttk.Combobox(self, textvariable=textvariable, values=values)
        self._combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def current(self):
        """Return the combobox selection."""
        return self._combo.current()

    def configure(self, text=None, values=None):
        """Configure internal widgets."""
        if text is not None:
            self._label['text'] = text
        if values is not None:
            self._combo['values'] = values
