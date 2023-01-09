"""Provide a class for viewing and editing "Todo" chapter properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.views.basic_view import BasicView
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar


class TodoChapterView(BasicView):
    """Class for viewing and editing chapter properties.
      
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """

    def __init__(self, ui):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui -- NovelystTk: Reference to the user interface.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        # 'Arc namee' entry.
        self._arcs = MyStringVar()
        self._arcsEntry = LabelEntry(self._elementInfoWindow, text=_('Arc name'), textvariable=self._arcs, lblWidth=22)
        self._arcsEntry.pack(anchor=tk.W, pady=2)

        # Frame for arc specific widgets.
        self._plotFrame = ttk.Frame(self._elementInfoWindow)
        self._nrScenes = ttk.Label(self._plotFrame)
        self._nrScenes.pack(side=tk.LEFT, pady=2)
        ttk.Button(self._plotFrame, text=_('Remove scene assignments'), command=self._removeArcRef).pack(padx=1, pady=2)

    def set_data(self, element):
        """Update the view with element's data.
        
        - Hide the info window, if the chapter ist the "trash bin". 
        - Show/hide the "Do not auto-number" button, depending on the chapter type.       
        - Configure the "Do not auto-number" button, depending on the chapter level.       
        Extends the superclass constructor.
        """
        super().set_data(element)

        # Count the scenes assigned to this arc.
        self._scenesAssigned = []
        arc = self._element.kwVar['Field_ArcDefinition']
        if arc:
            for scId in self._ui.novel.scenes:
                if self._ui.novel.scenes[scId].scType == 0:
                    if arc in string_to_list(self._ui.novel.scenes[scId].scnArcs):
                        self._scenesAssigned.append(scId)
        else:
            arc = ''

        # 'Arc name' entry.
        self._arcs.set(arc)

        # Frame for arc specific widgets.
        if len(self._scenesAssigned) > 0:
            self._nrScenes['text'] = f'{_("Number of scenes")}: {len(self._scenesAssigned)}'
            if not self._plotFrame.winfo_manager():
                self._plotFrame.pack(after=self._arcsEntry, pady=2, fill=tk.X)
        else:
            if self._plotFrame.winfo_manager():
                self._plotFrame.pack_forget()

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        # 'Arc name' entry.
        newArcs = self._arcs.get().replace(';', '')
        if self._element.kwVar['Field_ArcDefinition'] or newArcs:
            if self._element.kwVar['Field_ArcDefinition'] != newArcs:
                for scId in self._element.srtScenes:
                    self._ui.novel.scenes[scId].scnArcs = newArcs
                self._element.kwVar['Field_ArcDefinition'] = newArcs

                # Use the arc as scene title suffix.
                newTitle = f'{self._element.kwVar["Field_ArcDefinition"]} - {self._ui.elementTitle.get()}'
                self._ui.elementTitle.set(newTitle)
                self._ui.isModified = True

        super().apply_changes()

    def _removeArcRef(self):
        """Remove arc reference from all scenes"""
        arc = self._arcs.get()
        if arc and self._ui.ask_yes_no(f'{_("Remove all scenes from the story arc")} "{arc}"?'):
            for scId in self._scenesAssigned:
                if self._ui.novel.scenes[scId].scnArcs is not None:
                    newArcs = []
                    arcs = string_to_list(self._ui.novel.scenes[scId].scnArcs)
                    for scArc in arcs:
                        if not scArc == arc:
                            newArcs.append(scArc)
                        else:
                            self._ui.isModified = True
                    self._ui.novel.scenes[scId].scnArcs = list_to_string(newArcs)
            self._scenesAssigned = []
            self._plotFrame.pack_forget()
            if self._ui.isModified:
                self._ui.tv.update_prj_structure()

