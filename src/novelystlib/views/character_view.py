"""Provide a class for viewing and editing character properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.views.world_element_view import WorldElementView
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar
from novelystlib.widgets.folding_frame import FoldingFrame
from novelystlib.widgets.text_box import TextBox


class CharacterView(WorldElementView):
    """Class for viewing and editing character properties.

    Adds to the right pane:
    - A "Full name" entry.
    - A "Bio" folding frame.
    - A "Goals" folding frame.
   
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """
    _LBL_X = 15
    # Width of left-placed labels.

    def __init__(self, ui):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui -- NovelystTk: Reference to the user interface.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        #--- 'Full name' entry.
        self._fullName = MyStringVar()
        LabelEntry(self.frame1, text=_('Full name'), textvariable=self._fullName, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- 'Bio' entry
        self._bioFrame = FoldingFrame(self._elementInfoWindow, '', self._toggle_bioWindow)
        self._bioEntry = TextBox(self._bioFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=10,
                width=10,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._bioEntry.pack(fill=tk.X)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- 'Goals' entry.
        self._goalsFrame = FoldingFrame(self._elementInfoWindow, '', self._toggle_goalsWindow)
        self._goalsEntry = TextBox(self._goalsFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=10,
                width=10,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._goalsEntry.pack(fill=tk.X)

    def set_data(self, element):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        # 'Full name' entry.
        self._fullName.set(self._element.fullName)

        #--- 'Bio' entry
        if self._ui.novel.kwVar.get('Field_CustomChrBio', None):
            self._bioFrame.buttonText = self._ui.novel.kwVar['Field_CustomChrBio']
        else:
            self._bioFrame.buttonText = _('Bio')
        if self._ui.kwargs['show_cr_bio']:
            self._bioFrame.show()
        else:
            self._bioFrame.hide()
        self._bioEntry.set_text(self._element.bio)

        #--- 'Goals' entry.
        if self._ui.novel.kwVar.get('Field_CustomChrGoals', None):
            self._goalsFrame.buttonText = self._ui.novel.kwVar['Field_CustomChrGoals']
        else:
            self._goalsFrame.buttonText = _('Goals')
        if self._ui.kwargs['show_cr_goals']:
            self._goalsFrame.show()
        else:
            self._goalsFrame.hide()
        self._goalsEntry.set_text(self._element.goals)

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """

        # 'Full name' entry.
        fullName = self._fullName.get()
        if fullName or self._element.fullName:
            if self._element.fullName != fullName:
                self._element.fullName = fullName.strip()
                self._ui.isModified = True

        # 'Bio' entry
        if self._bioEntry.hasChanged:
            bio = self._bioEntry.get_text()
            if bio or self._element.bio:
                if self._element.bio != bio:
                    self._element.bio = bio
                    self._ui.isModified = True

        # 'Goals' entry.
        if self._goalsEntry.hasChanged:
            goals = self._goalsEntry.get_text()
            if goals or self._element.goals:
                if self._element.goals != goals:
                    self._element.goals = goals
                    self._ui.isModified = True

        if self._ui.isModified:
            self._ui.tv.update_prj_structure()

        super().apply_changes()

    def _toggle_bioWindow(self, event=None):
        """Hide/show the 'Bio' textbox."""
        if self._ui.kwargs['show_cr_bio']:
            self._bioFrame.hide()
            self._ui.kwargs['show_cr_bio'] = False
        else:
            self._bioFrame.show()
            self._ui.kwargs['show_cr_bio'] = True

    def _toggle_goalsWindow(self, event=None):
        """Hide/show the 'Goals' textbox."""
        if self._ui.kwargs['show_cr_goals']:
            self._goalsFrame.hide()
            self._ui.kwargs['show_cr_goals'] = False
        else:
            self._goalsFrame.show()
            self._ui.kwargs['show_cr_goals'] = True

