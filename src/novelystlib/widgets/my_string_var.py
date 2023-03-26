"""Provide a custom variant of the tkinter StringVar class.

Copyright (c) 2023 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
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
