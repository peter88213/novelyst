""""Provide a tkinter entry box with a label.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk


class LabelEntry(tk.Frame):
    """Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable):
        super().__init__(parent)
        self.pack(fill=tk.X)
        lbl = tk.Label(self, text=text, anchor='w')
        lbl.pack(side=tk.LEFT)
        entry = tk.Entry(self, textvariable=textvariable)
        entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
