"""Provide a class for viewing and editing "Todo" chapter properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.view_controller.right_frame.basic_view import BasicView
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar


class TodoChapterView(BasicView):
    """Class for viewing and editing chapter properties.
    
    Adds to the right pane:
    - An "Arc" entry.
      
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   

    If one story arc is assigned to a "Todo" chapter, this chapter is used 
    for defining this arc. In this case, there is an extra display:    
    - The number of normal scenes assigned to this arc.
    - A button to remove all scene assigments to this arc.
    """
    _INDEXCARD = True
    _ELEMENT_INFO = True
    _NOTES = False
    _BUTTONBAR = True

    def __init__(self, ui):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        self._lastSelected = ''

        # 'Arc namee' entry.
        self._arcs = MyStringVar()
        self._arcsEntry = LabelEntry(self._elementInfoWindow, text=_('Arc name'), textvariable=self._arcs, lblWidth=22)
        self._arcsEntry.pack(anchor=tk.W, pady=2)

        # Frame for arc specific widgets.
        self._arcFrame = ttk.Frame(self._elementInfoWindow)
        self._nrScenes = ttk.Label(self._arcFrame)
        self._nrScenes.pack(side=tk.LEFT, pady=2)
        ttk.Button(self._arcFrame, text=_('Clear scene assignments'), command=self._removeArcRef).pack(padx=1, pady=2)

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
            if not self._arcFrame.winfo_manager():
                self._arcFrame.pack(after=self._arcsEntry, pady=2, fill=tk.X)
        else:
            if self._arcFrame.winfo_manager():
                self._arcFrame.pack_forget()

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        # 'Arc name' entry.
        oldArc = self._element.kwVar['Field_ArcDefinition']
        newArc = self._arcs.get().replace(';', '')
        if oldArc or newArc:
            if oldArc != newArc:
                # Assign new arc to all children.
                for scId in self._element.srtScenes:
                    self._ui.novel.scenes[scId].scnArcs = newArc

                # Rename scene arc assignments,if necessary.
                if oldArc:
                    for scId in self._ui.novel.scenes:
                        if self._ui.novel.scenes[scId].scType == 0:
                            scnArcs = string_to_list(self._ui.novel.scenes[scId].scnArcs)
                            try:
                                scnArcs.remove(oldArc)
                            except ValueError:
                                pass
                            else:
                                scnArcs.append(newArc)
                                self._ui.novel.scenes[scId].scnArcs = list_to_string(scnArcs)

                self._element.kwVar['Field_ArcDefinition'] = newArc

                # Use the arc as scene title suffix.
                newTitle = f'{self._element.kwVar["Field_ArcDefinition"]} - {self._elementTitle.get()}'
                self._elementTitle.set(newTitle)
                self._ui.isModified = True

        super().apply_changes()

    def _removeArcRef(self):
        """Remove arc reference from all scenes.
        
        Remove also all scene associations from the children points.
        """
        self._lastSelected = self._ui.tv.tree.selection()[0]
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
            self._arcFrame.pack_forget()

            # Unlink the children points from the narrative scenes.
            for scId in self._element.srtScenes:
                self._ui.novel.scenes[scId].kwVar['Field_SceneAssoc'] = None

            if self._ui.isModified:
                self._ui.tv.update_prj_structure()
                self._ui.tv.refresh_tree()
                self._ui.tv.tree.see(self._lastSelected)
                self._ui.tv.tree.selection_set(self._lastSelected)

