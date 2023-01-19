"""Provide a class for viewing and editing "Todo" scene properties.

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
          
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   

    If one story arc is assigned to a "Todo" scene, this scene is used 
    for describing this arc. In this case, there is an extra display:    
    - The number of normal scenes assigned to this arc.
    - A button to remove all scene assigments to this arc.
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
        self._associatedScene = None
        self._lastSelected = ''
        self._treeSelectBinding = None
        self._uiEscBinding = None

        # 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- Frame for arc specific widgets.
        self._plotFrame = ttk.Frame(self._elementInfoWindow)

        # Associated scene title display.
        self._sceneFrame = ttk.Frame(self._plotFrame)
        self._sceneFrame.pack(anchor=tk.W, fill=tk.X)
        self._associatedSceneTitle = ttk.Label(self._sceneFrame)
        self._associatedSceneTitle.pack(anchor=tk.W, pady=2)
        ttk.Button(self._sceneFrame, text=_('Assign scene'), command=self._pick_scene).pack(side=tk.LEFT, padx=1, pady=2)
        ttk.Button(self._sceneFrame, text=_('Clear assignment'), command=self._clear_assignment).pack(side=tk.LEFT, padx=1, pady=2)

        # Arc display.
        self._arc = ttk.Label(self._plotFrame)
        self._arc.pack(anchor=tk.W, pady=2)

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

        # Frame for arc point specific widgets.
        if self._element.scnArcs:
            # Arc display.
            self._arc.config(text=f'{_("Arc")}: {self._element.scnArcs}')

            # Associated scene display.
            try:
                self._associatedScene = self._element.kwVar.get('Field_SceneAssoc', None)
                sceneTitle = self._ui.novel.scenes[self._associatedScene].title
            except:
                self._associatedScene = None
                sceneTitle = ''
            self._associatedSceneTitle['text'] = sceneTitle

            if not self._plotFrame.winfo_manager():
                self._plotFrame.pack(pady=2, fill=tk.X)
        else:
            if self._plotFrame.winfo_manager():
                self._plotFrame.pack_forget()

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        # 'Arc name' entry.
        if  self._element.kwVar.get('Field_SceneAssoc', None) != self._associatedScene:
            self._element.kwVar['Field_SceneAssoc'] = self._associatedScene
            self._ui.isModified = True

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        super().apply_changes()

    def _pick_scene(self):
        """Enter the "associate scene" selection mode.
        
        Change the mouse cursor to "+" and expand the "Narrative" subtree.
        Now the tree selection does not trigger the viewer, 
        but tries to associate the selected node to the Arc point.  
        
        To end the "associate scene" selection mode, either select any node, 
        or press the Escape key.
        """
        self._lastSelected = self._ui.tv.tree.selection()[0]
        self._ui.tv.config(cursor='plus')
        self._ui.tv.open_children('')
        self._ui.tv.tree.see(self._ui.tv.NV_ROOT)
        self._treeSelectBinding = self._ui.tv.tree.bind('<<TreeviewSelect>>')
        self._ui.tv.tree.bind('<<TreeviewSelect>>', self._assign_scene)
        self._uiEscBinding = self._ui.root.bind('<Esc>')
        self._ui.root.bind('<Escape>', self._assign_scene)

    def _assign_scene(self, event=None):
        """Associate the selected scene with the Arc point.
        
        Restore the previous scene selection mode. 
        """
        # Restore the previous scene selection mode.
        self._ui.tv.tree.bind('<<TreeviewSelect>>', self._treeSelectBinding)
        self._ui.root.bind('<Escape>', self._uiEscBinding)
        self._ui.tv.config(cursor='arrow')

        # Assign the selected scene and its arc to the point, if applicable.
        nodeId = self._ui.tv.tree.selection()[0]
        if nodeId.startswith(self._ui.tv.SCENE_PREFIX):
            scId = nodeId[2:]
            if self._ui.novel.scenes[scId].scType == 0:

                # Make sure the scene is also associated with the arc.
                scnArcs = string_to_list(self._ui.novel.scenes[scId].scnArcs)
                if not self._element.scnArcs in scnArcs:
                    scnArcs.append(self._element.scnArcs)
                    self._ui.novel.scenes[scId].scnArcs = list_to_string(scnArcs)

                # Associate the point with the scene.
                self._associatedScene = scId

                self.apply_changes()
                self.set_data(self._element)
                # this shall create a backward reference from the scene to the point
        self._ui.tv.tree.see(self._lastSelected)
        self._ui.tv.tree.selection_set(self._lastSelected)

    def _clear_assignment(self):
        """Unassign a scene from the Arc point
        
        Get the ID of a "normal" scene selected by the user. 
        """
        self._associatedScene = None
        self.apply_changes()
        self.set_data(self._element)
        self._ui.tv.tree.see(self._lastSelected)
        self._ui.tv.tree.selection_set(self._lastSelected)

