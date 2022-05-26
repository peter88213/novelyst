""""Provide a class for viewing and editing character properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import scrolledtext
from novelystlib.element_view import ElementView
from novelystlib.label_entry import LabelEntry


class CharacterView(ElementView):
    """Class for viewing and editing character properties."""

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)

        # Place a "Full name" entry inside the frame.
        if element.fullName is not None:
            fullName = element.fullName
        else:
            fullName = ''
        self._fullName = tk.StringVar(value=fullName)
        self._fullNameEntry = LabelEntry(self._valuesFrame, text='Full name', textvariable=self._fullName)
        self._fullNameEntry.pack(anchor=tk.W, pady=2)

        # Place a "Bio" window inside the frame.
        tk.Label(self._valuesFrame, text='Bio', anchor=tk.W).pack(fill=tk.X)
        self._bioWindow = scrolledtext.ScrolledText(self._valuesFrame, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=10, width=10, padx=5, pady=5)
        self._bioWindow.pack(fill=tk.X)
        if element.bio:
            self._bioWindow.insert(tk.END, element.bio)

        # Place a "Goals" window inside the frame.
        tk.Label(self._valuesFrame, text='Goals', anchor=tk.W).pack(fill=tk.X)
        self._goalsWindow = scrolledtext.ScrolledText(self._valuesFrame, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=10, width=10, padx=5, pady=5)
        self._goalsWindow.pack(fill=tk.X)
        if element.goals:
            self._goalsWindow.insert(tk.END, element.goals)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        fullName = self._fullName.get()
        if fullName or self._element.fullName:
            if self._element.fullName != fullName:
                self._element.fullName = fullName.strip()
                ui.isModified = True

        bio = self._bioWindow.get('1.0', tk.END).strip(' \n')
        if bio or self._element.bio:
            if self._element.bio != bio:
                self._element.bio = bio
                ui.isModified = True

        goals = self._goalsWindow.get('1.0', tk.END).strip(' \n')
        if goals or self._element.goals:
            if self._element.goals != goals:
                self._element.goals = goals
                ui.isModified = True

        super().apply_changes(ui)

