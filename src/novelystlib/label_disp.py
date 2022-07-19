""""Provide a tkinter based display box with a label.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk


class LabelDisp(tk.Frame):
    """Display box with a label."""

    def __init__(self, parent, text, textvariable, lblWidth=10):
        super().__init__(parent)
        self.pack(fill=tk.X)
        tk.Label(self, text=text, anchor=tk.W, width=lblWidth).pack(side=tk.LEFT)
        tk.Label(self, textvariable=textvariable, anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True)
