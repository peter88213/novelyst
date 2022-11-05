""""Provide a class for viewing and editing "Todo" scene properties.

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


class TodoSceneView(BasicView):
    """Class for viewing and editing "Todo" scene properties.
    
    If one story arc is assigned to a "Todo" scene, this scene is used 
    for describing this arc. In this case, there is an extra display:    
    - The number of normal scenes assigned to this arc.
    - A button to remove all scene assigments to this arc.
    """

    def __init__(self, ui):
        """Extends the superclass constructor."""
        super(). __init__(ui)

        # 'Arc reference' entry.
        self._arcs = MyStringVar()
        self._arcsEntry = LabelEntry(self._elementInfoWindow, text=_('Arc reference'), textvariable=self._arcs, lblWidth=22)
        self._arcsEntry.pack(anchor=tk.W, pady=2)

        # Frame for arc specific widgets.
        self._arcFrame = ttk.Frame(self._elementInfoWindow)
        self._nrScenes = ttk.Label(self._arcFrame)
        self._nrScenes.pack(side=tk.LEFT, pady=2)
        ttk.Button(self._arcFrame, text=_('Remove scene assignments'), command=self._removeArcRef).pack(padx=1, pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        # Count the scenes assigned to this arc.
        self._scenesAssigned = []
        arc = self._element.kwVar.get('Field_SceneArcs', None)
        if arc:
            for scId in self._ui.ywPrj.scenes:
                if self._ui.ywPrj.scenes[scId].scType == 0:
                    if arc in string_to_list(self._ui.ywPrj.scenes[scId].kwVar.get('Field_SceneArcs', '')):
                        self._scenesAssigned.append(scId)
        else:
            arc = ''

        # 'Arc reference' entry.
        self._arcs.set(arc)

        # Frame for arc specific widgets.
        if len(self._scenesAssigned) > 0:
            self._nrScenes['text'] = f'{_("Number of scenes")}: {len(self._scenesAssigned)}'
            if not self._arcFrame.winfo_manager():
                self._arcFrame.pack(after=self._arcsEntry, pady=2, fill=tk.X)
        else:
            if self._arcFrame.winfo_manager():
                self._arcFrame.pack_forget()

        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

    def _removeArcRef(self):
        """Remove arc reference from all scenes"""
        arc = self._arcs.get()
        if arc and self._ui.ask_yes_no(f'{_("Remove all scenes from the story arc")} "{arc}"?'):
            for scId in self._scenesAssigned:
                if self._ui.ywPrj.scenes[scId].kwVar.get('Field_SceneArcs', None):
                    newArcs = []
                    arcs = string_to_list(self._ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs'])
                    for scArc in arcs:
                        if not scArc == arc:
                            newArcs.append(scArc)
                        else:
                            self._ui.isModified = True
                    self._ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs'] = list_to_string(newArcs)
            self._scenesAssigned = []
            self._arcFrame.pack_forget()
            if self._ui.isModified:
                self._ui.tv.update_prj_structure()

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        # 'Arc reference' entry.
        if self._update_field_str(self._arcs, 'Field_SceneArcs'):
            arc = self._element.kwVar['Field_SceneArcs']

            # Use the arc as scene title suffix.
            newTitle = f'{arc} - {self._ui.elementTitle.get()}'
            self._ui.elementTitle.set(newTitle)
            self._ui.isModified = True

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        super().apply_changes()

