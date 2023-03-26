"""Provide a tkinter based class for viewing and editing scene properties.

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
from novelystlib.widgets.folding_frame import FoldingFrame
from novelystlib.widgets.text_box import TextBox


class SceneView(BasicView):
    """Class for viewing and editing scene properties.
       
    Adds to the right pane:
    - A "Tags" entry.
    - A folding frame for relationships (characters/locations/items)
       
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """
    _REL_Y = 2
    # height of the Relations text boxes

    def __init__(self, ui):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        #--- 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

        self.frame2 = ttk.Frame(self._elementInfoWindow)
        self.frame2.pack(anchor=tk.W, fill=tk.X)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- Frame for 'Relationships'.
        self._relationFrame = FoldingFrame(self._elementInfoWindow, _('Relationships'), self._toggle_relationFrame)

        # 'Characters' window.
        self._crTitles = ''
        self._characterLabel = ttk.Label(self._relationFrame, text=_('Characters'))
        self._characterLabel.pack(anchor=tk.W)
        self._characterWindow = TextBox(self._relationFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._REL_Y,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._characterWindow.pack(fill=tk.X)

        # 'Locations' window.
        self._lcTitles = ''
        self._locationLabel = ttk.Label(self._relationFrame, text=_('Locations'))
        self._locationLabel.pack(anchor=tk.W)
        self._locationWindow = TextBox(self._relationFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._REL_Y,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._locationWindow.pack(fill=tk.X)

        # 'Items' window.
        self._itTitles = ''
        self._itemLabel = ttk.Label(self._relationFrame, text=_('Items'))
        self._itemLabel.pack(anchor=tk.W)
        self._itemWindow = TextBox(self._relationFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._REL_Y,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._itemWindow.pack(fill=tk.X)

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

        #--- Frame for 'Relationships'.
        if self._ui.kwargs['show_relationships']:
            self._relationFrame.show()
        else:
            self._relationFrame.hide()

        # 'Characters' window.
        self._crTitles = self._get_relation_title_string(element.characters, self._ui.novel.characters)
        self._characterWindow.set_text(self._crTitles)

        # 'Locations' window.
        self._lcTitles = self._get_relation_title_string(element.locations, self._ui.novel.locations)
        self._locationWindow.set_text(self._lcTitles)

        # 'Items' window.
        self._itTitles = self._get_relation_title_string(element.items, self._ui.novel.items)
        self._itemWindow.set_text(self._itTitles)

    def _get_relation_title_string(self, elemIds, elements):
        """Write element titles to a text box and return the text.
        
        Positional arguments:
        elemIds -- list of IDs of elements related to the scene (character/location/item IDs)
        elements -- list of element objects (characters/locations/items) on the project level.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(elements[elemId].title)
                except:
                    pass
        titleStr = list_to_string(elemTitles)
        return titleStr

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        # 'Characters' window.
        if self._characterWindow.hasChanged:
            newCharacters = self._get_relation_id_list(self._characterWindow.get_text().strip(';'), self._crTitles, self._ui.novel.characters)
            if newCharacters is not None:
                if self._element.characters != newCharacters:
                    self._element.characters = newCharacters
                    self._ui.isModified = True

        # 'Locations' window.
        if self._locationWindow.hasChanged:
            newLocations = self._get_relation_id_list(self._locationWindow.get_text().strip(';'), self._lcTitles, self._ui.novel.locations)
            if newLocations is not None:
                if self._element.locations != newLocations:
                    self._element.locations = newLocations
                    self._ui.isModified = True

        # 'Items' window.
        if self._itemWindow.hasChanged:
            newItems = self._get_relation_id_list(self._itemWindow.get_text().strip(';'), self._itTitles, self._ui.novel.items)
            if newItems is not None:
                if self._element.items != newItems:
                    self._element.items = newItems
                    self._ui.isModified = True

        super().apply_changes()

    def _get_relation_id_list(self, newTitleStr, oldTitleStr, elements):
        """Return a list of valid IDs from a string containing semicolon-separated titles."""
        if newTitleStr or oldTitleStr:
            if oldTitleStr != newTitleStr:
                elemIds = []
                for elemTitle in string_to_list(newTitleStr):
                    for elemId in elements:
                        if elements[elemId].title == elemTitle:
                            elemIds.append(elemId)
                            break
                    else:
                        # No break occurred: there is no element with the specified title
                        self._ui.show_error(f'{_("Wrong name")}: "{elemTitle}"', title=_('Input rejected'))
                return elemIds

        return None

    def _toggle_relationFrame(self, event=None):
        """Hide/show the 'Relationships' frame."""
        if self._ui.kwargs['show_relationships']:
            self._relationFrame.hide()
            self._ui.kwargs['show_relationships'] = False
        else:
            self._relationFrame.show()
            self._ui.kwargs['show_relationships'] = True

