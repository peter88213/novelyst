"""Provide a tkinter based class for viewing and editing scene properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pywriter.pywriter_globals import *
from novelystlib.views.basic_view import BasicView
from novelystlib.widgets.label_combo import LabelCombo
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar
from novelystlib.widgets.folding_frame import FoldingFrame
from novelystlib.widgets.text_box import TextBox


class SceneView(BasicView):
    """Class for viewing and editing scene properties.
       
    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """
    _GCO_Y = 5
    # height of the Goals/Conflict/Outcome text boxes
    _REL_Y = 2
    # height of the Relations text boxes

    def __init__(self, ui):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui -- NovelystTk: Reference to the user interface.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        #--- 'Viewpoint' combobox.
        self._viewpoint = MyStringVar()
        self._characterCombobox = LabelCombo(self._elementInfoWindow, text=_('Viewpoint'), textvariable=self._viewpoint, values=[])
        self._characterCombobox.pack(anchor=tk.W, pady=2)

        #--- 'Arcs' entry (if any).
        self._arcs = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Arcs'), textvariable=self._arcs).pack(anchor=tk.W, pady=2)

        #--- 'Arc points' label.
        self._arcPointsDisplay = ttk.Label(self._elementInfoWindow)
        self._arcPointsDisplay.pack(anchor=tk.W, pady=2)

        #--- 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor=tk.W, pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- 'Append to previous scene' checkbox.
        self._appendToPrev = tk.BooleanVar()
        self._appendToPrevCheckbox = ttk.Checkbutton(self._elementInfoWindow, text=_('Append to previous scene'),
                                         variable=self._appendToPrev, onvalue=True, offvalue=False)
        self._appendToPrevCheckbox.pack(anchor=tk.W, pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- Frame for 'Action'/'Reaction'/'Custom'.
        self._pacingFrame = FoldingFrame(self._elementInfoWindow, _('Action/Reaction'), self._toggle_pacingFrame)

        # 'Action'/'Reaction'/'Custom' radiobuttons.
        selectionFrame = ttk.Frame(self._pacingFrame)
        self._customGoal = ''
        self._customConflict = ''
        self._customOutcome = ''
        self._scenePacingType = tk.IntVar()
        ttk.Radiobutton(selectionFrame, text=_('Action'),
                                         variable=self._scenePacingType, value=0, command=self._set_action_scene).pack(side=tk.LEFT, anchor=tk.W, pady=2)
        ttk.Radiobutton(selectionFrame, text=_('Reaction'),
                                         variable=self._scenePacingType, value=1, command=self._set_reaction_scene).pack(side=tk.LEFT, anchor=tk.W, pady=2)
        ttk.Radiobutton(selectionFrame, text=_('Custom'),
                                         variable=self._scenePacingType, value=2, command=self._set_custom_ar_scene).pack(anchor=tk.W, pady=2)
        selectionFrame.pack(fill=tk.X)

        # 'Goal/Reaction' window. The labels are configured dynamically.
        self._goalLabel = ttk.Label(self._pacingFrame)
        self._goalLabel.pack(anchor=tk.W)
        self._goalWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._GCO_Y,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._goalWindow.pack(fill=tk.X)

        # 'Conflict/Dilemma' window. The labels are configured dynamically.
        self._conflictLabel = ttk.Label(self._pacingFrame)
        self._conflictLabel.pack(anchor=tk.W)
        self._conflictWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._GCO_Y,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._conflictWindow.pack(fill=tk.X)

        # 'Outcome/Choice' window. The labels are configured dynamically.
        self._outcomeLabel = ttk.Label(self._pacingFrame)
        self._outcomeLabel.pack(anchor=tk.W)
        self._outcomeWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._GCO_Y,
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._outcomeWindow.pack(fill=tk.X)

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

        # 'Viewpoint' combobox.
        charList = []
        for crId in self._ui.novel.srtCharacters:
            charList.append(self._ui.novel.characters[crId].title)
        self._characterCombobox.configure(values=charList)
        if self._element.characters:
            vp = self._ui.novel.characters[self._element.characters[0]].title
        else:
            vp = ''
        self._viewpoint.set(value=vp)

        # 'Arcs' entry (if any).
        if self._element.scnArcs is not None:
            arcs = self._element.scnArcs
        else:
            arcs = ''
        self._arcs.set(arcs)

        # 'Arc points' label.
        arcPoints = []
        arcPointIds = string_to_list(self._element.kwVar.get('Field_SceneAssoc', None))
        for scId in arcPointIds:
            arcPoints.append(self._ui.novel.scenes[scId].title)
        self._arcPointsDisplay.config(text=list_to_string(arcPoints))

        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

        # 'Append to previous scene' checkbox.
        self._appendToPrev.set(self._element.appendToPrev)

        # Customized Goal/Conflict/Outcome configuration.
        if self._ui.novel.kwVar.get('Field_CustomGoal', None):
            self._customGoal = self._ui.novel.kwVar['Field_CustomGoal']
        else:
            self._customGoal = _('N/A')

        if self._ui.novel.kwVar.get('Field_CustomConflict', None):
            self._customConflict = self._ui.novel.kwVar['Field_CustomConflict']
        else:
            self._customConflict = _('N/A')

        if self._ui.novel.kwVar.get('Field_CustomOutcome', None):
            self._customOutcome = self._ui.novel.kwVar['Field_CustomOutcome']
        else:
            self._customOutcome = _('N/A')

        #--- Frame for 'Action'/'Reaction'/'Custom'.
        if self._ui.kwargs['show_action_reaction']:
            self._pacingFrame.show()
        else:
            self._pacingFrame.hide()

        # 'Action'/'Reaction'/'Custom' radiobuttons.
        if self._element.kwVar.get('Field_CustomAR', None):
            pacingType = 2
        elif self._element.isReactionScene:
            pacingType = 1
        else:
            pacingType = 0
        self._scenePacingType.set(pacingType)

        # 'Goal/Reaction' window.
        self._goalWindow.set_text(self._element.goal)

        # 'Conflict/Dilemma' window.
        self._conflictWindow.set_text(self._element.conflict)

        # 'Outcome/Choice' window.
        self._outcomeWindow.set_text(self._element.outcome)

        # Configure the labels.
        if pacingType == 2:
            self._set_custom_ar_scene()
        elif pacingType == 1:
            self._set_reaction_scene()
        else:
            self._set_action_scene()

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
        # 'Viewpoint' combobox.
        option = self._characterCombobox.current()
        if self._element.characters:
            oldVpId = self._element.characters[0]
        else:
            oldVpId = None
        if option >= 0:
            newVpId = self._ui.novel.srtCharacters[option]
            if oldVpId:
                if newVpId != oldVpId:
                    try:
                        self._element.characters.remove(newVpId)
                    except:
                        pass
                    self._element.characters.insert(0, newVpId)
                    self._ui.isModified = True
            else:
                self._element.characters = []
                self._element.characters.append(newVpId)
                self._ui.isModified = True

        # 'Arcs' entry (if any).
        newArcs = self._arcs.get()
        if self._element.scnArcs or newArcs:
            if self._element.scnArcs != newArcs:
                self._element.scnArcs = newArcs
                self._ui.isModified = True

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        # 'Append to previous scene' checkbox.
        appendToPrev = self._appendToPrev.get()
        if self._element.appendToPrev or appendToPrev:
            if self._element.appendToPrev != appendToPrev:
                self._element.appendToPrev = appendToPrev
                self._ui.isModified = True

        # 'Action'/'Reaction'/'Custom' radiobuttons.
        isReactionScene = self._scenePacingType.get() == 1
        if self._element.isReactionScene != isReactionScene:
            self._element.isReactionScene = isReactionScene
            self._ui.isModified = True
        if self._scenePacingType.get() == 2:
            value = '1'
        else:
            value = None
        if self._element.kwVar.get('Field_CustomAR', None) or value:
            if self._element.kwVar['Field_CustomAR'] != value:
                self._element.kwVar['Field_CustomAR'] = value
                self._ui.isModified = True

        # 'Goal/Reaction' window.
        if self._goalWindow.hasChanged:
            goal = self._goalWindow.get_text()
            if goal or self._element.goal:
                if self._element.goal != goal:
                    self._element.goal = goal
                    self._ui.isModified = True

        # 'Conflict/Dilemma' window.
        if self._conflictWindow.hasChanged:
            conflict = self._conflictWindow.get_text()
            if conflict or self._element.conflict:
                if self._element.conflict != conflict:
                    self._element.conflict = conflict
                    self._ui.isModified = True

        # 'Outcome/Choice' window.
        if self._outcomeWindow.hasChanged:
            outcome = self._outcomeWindow.get_text()
            if outcome or self._element.outcome:
                if self._element.outcome != outcome:
                    self._element.outcome = outcome
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
                        messagebox.showerror(_('Input rejected'), f'{_("Wrong name")}: "{elemTitle}"')
                return elemIds

        return None

    def _set_action_scene(self, event=None):
        self._goalLabel.config(text=_('Goal'))
        self._conflictLabel.config(text=_('Conflict'))
        self._outcomeLabel.config(text=_('Outcome'))

    def _set_reaction_scene(self, event=None):
        self._goalLabel.config(text=_('Reaction'))
        self._conflictLabel.config(text=_('Dilemma'))
        self._outcomeLabel.config(text=_('Choice'))

    def _set_custom_ar_scene(self, event=None):
        self._goalLabel.config(text=self._customGoal)
        self._conflictLabel.config(text=self._customConflict)
        self._outcomeLabel.config(text=self._customOutcome)

    def _toggle_pacingFrame(self, event=None):
        """Hide/show the 'A/R/C' frame."""
        if self._ui.kwargs['show_action_reaction']:
            self._pacingFrame.hide()
            self._ui.kwargs['show_action_reaction'] = False
        else:
            self._pacingFrame.show()
            self._ui.kwargs['show_action_reaction'] = True

    def _toggle_relationFrame(self, event=None):
        """Hide/show the 'Relationships' frame."""
        if self._ui.kwargs['show_relationships']:
            self._relationFrame.hide()
            self._ui.kwargs['show_relationships'] = False
        else:
            self._relationFrame.show()
            self._ui.kwargs['show_relationships'] = True

