""""Provide a tkinter based display box with a label.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk


class LabelDisp(ttk.Frame):
    """Display box with a label."""

    def __init__(self, parent, text, textvariable, lblWidth=10):
        super().__init__(parent)
        self.pack(fill=tk.X)
        self._leftLabel = ttk.Label(self, text=text, anchor=tk.W, width=lblWidth)
        self._leftLabel.pack(side=tk.LEFT)
        self._rightLabel = ttk.Label(self, textvariable=textvariable, anchor=tk.W)
        self._rightLabel.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def configure(self, text=None):
        """Configure internal widget."""
        if text is not None:
            self._leftLabel['text'] = text
