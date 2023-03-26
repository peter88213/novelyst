"""Provide a tkinter based entry box with a label.

Copyright (c) 2023 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class LabelEntry(ttk.Frame):
    """Entry box with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, lblWidth=10):
        super().__init__(parent)
        self.pack(fill=tk.X)
        self._label = ttk.Label(self, text=text, anchor=tk.W, width=lblWidth)
        self._label.pack(side=tk.LEFT)
        self._entry = ttk.Entry(self, textvariable=textvariable)
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def set(self, value):
        """Replace None by an empty string.
        
        Extends the superclass method.
        """
        if value is None:
            value = ''
        self._entry.set(value)

    def configure(self, text=None):
        """Configure internal widget."""
        if text is not None:
            self._label['text'] = text
