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

        # Frame for arc specific widgets.
        self._arcFrame = ttk.Frame(self._elementInfoWindow)

        # Arc display.
        self._arc = ttk.Label(self._arcFrame)
        self._arc.pack(anchor=tk.W, pady=2)

        # Associated scene title display.
        self._associatedSceneTitle = ttk.Label(self._arcFrame)
        self._associatedSceneTitle.pack(anchor=tk.W, pady=2)
        ttk.Button(self._arcFrame, text=_('Choose scene'), command=self._associateScene).pack(side=tk.LEFT, padx=1, pady=2)
        ttk.Button(self._arcFrame, text=_('Clear scene'), command=self._disassociateScene).pack(side=tk.LEFT, padx=1, pady=2)

        self._arcFramePlace = ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL)
        self._arcFramePlace.pack(fill=tk.X)

        # 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

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
            if not self._arcFrame.winfo_manager():
                self._arcFrame.pack(before=self._arcFramePlace, pady=2, fill=tk.X)
        else:
            if self._arcFrame.winfo_manager():
                self._arcFrame.pack_forget()

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

    def _associateScene(self):
        """Associate a scene to the Arc point
        
        Get the ID of a "normal" scene selected by the user. 
        """
        scId = '1'
        self._associatedScene = scId
        self.apply_changes()
        self.set_data(self._element)

    def _disassociateScene(self):
        """Associate a scene to the Arc point
        
        Get the ID of a "normal" scene selected by the user. 
        """
        scId = None
        self._associatedScene = scId
        self.apply_changes()
        self.set_data(self._element)

