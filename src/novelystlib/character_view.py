""""Provide a class for viewing and editing character properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import scrolledtext
from novelystlib.element_view import ElementView


class CharacterView(ElementView):
    """A class for viewing and editing character properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)

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

