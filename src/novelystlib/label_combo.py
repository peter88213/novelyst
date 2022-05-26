""""Provide a tkinter based combobox with a label.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class LabelCombo(tk.Frame):
    """Combobox with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, values, lblWidth=10):
        super().__init__(parent)
        self.pack(fill=tk.X)
        tk.Label(self, text=text, anchor=tk.W, width=lblWidth).pack(side=tk.LEFT)
        self.combo = ttk.Combobox(self, textvariable=textvariable, values=values)
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def current(self):
        return self.combo.current()
