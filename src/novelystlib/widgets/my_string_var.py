"""Provide a custom variant of the tkinter StringVar class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk


class MyStringVar(tk.StringVar):

    def set(self, value):
        """Replace None by an empty string.
        
        Extends the superclass method.
        """
        if value is None:
            value = ''
        super().set(value)
