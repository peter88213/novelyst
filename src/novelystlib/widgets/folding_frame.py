""""Provide a tkinter based folding frame with a "show/hide" button.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk


class FoldingFrame(ttk.Frame):
    """Folding frame with a "show/hide" button.
    """
    _PREFIX_SHOW = '▽  '
    _PREFIX_HIDE = '▷  '

    def __init__(self, parent, buttonText, command, **kw):
        super().__init__(parent, **kw)
        self.buttonText = buttonText
        self._toggleButton = tk.Button(parent, bd=0, relief=tk.FLAT, anchor=tk.W, command=command)
        self._toggleButton['text'] = f'{self._PREFIX_HIDE}{self.buttonText}'
        self._toggleButton.pack(fill=tk.X)

    def show(self, event=None):
        self._toggleButton['text'] = f'{self._PREFIX_SHOW}{self.buttonText}'
        self.pack(after=self._toggleButton, fill=tk.X, pady=5)

    def hide(self, event=None):
        self._toggleButton['text'] = f'{self._PREFIX_HIDE}{self.buttonText}'
        self.pack_forget()

