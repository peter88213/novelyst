"""Provide a tkinter based class for viewing and editing "Normal" scene properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.view_controller.right_frame.notes_scene_view import NotesSceneView
from novelystlib.widgets.label_combo import LabelCombo
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar
from novelystlib.widgets.folding_frame import FoldingFrame
from novelystlib.widgets.text_box import TextBox


class NormalSceneView(NotesSceneView):
    """Class for viewing and editing scene properties.
       
    Adds to the right pane:
    - A combobox for viewpoint character selection.
    - A checkbox "append to previous".
    - A "Plot" folding frame for arcs and arc point associations.
    - An "Action/Reaction" folding frame for Goal/Reaction/Outcome.

    Public methods:
        apply_changes() -- Apply changes.   
        set_data() -- Update the view with element's data.
    """

    def __init__(self, ui, parent):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.
            parent -- Parent widget to display this widget.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, parent)

        #--- 'Viewpoint' combobox.
        self._viewpoint = MyStringVar()
        self._characterCombobox = LabelCombo(self._sceneExtraFrame, text=_('Viewpoint'), textvariable=self._viewpoint, values=[])
        self._characterCombobox.pack(anchor='w', pady=2)

        #--- 'Append to previous scene' checkbox.
        self._appendToPrev = tk.BooleanVar()
        self._appendToPrevCheckbox = ttk.Checkbutton(self._sceneExtraFrame, text=_('Append to previous scene'),
                                         variable=self._appendToPrev, onvalue=True, offvalue=False)
        self._appendToPrevCheckbox.pack(anchor='w', pady=2)

        ttk.Separator(self._sceneExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for arcs and plot.
        self._arcFrame = FoldingFrame(self._sceneExtraFrame, _('Plot'), self._toggle_arcFrame)

        # 'Arcs' entry (if any).
        self._arcs = MyStringVar()
        LabelEntry(self._arcFrame, text=_('Arcs'), textvariable=self._arcs).pack(anchor='w')

        #--- 'Arc points' label.
        self._arcPointsDisplay = tk.Label(self._arcFrame, anchor='w', bg='white')
        self._arcPointsDisplay.pack(anchor='w', fill='x')

        ttk.Separator(self._sceneExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Action'/'Reaction'/'Custom'.
        self._pacingFrame = FoldingFrame(self._sceneExtraFrame, _('Action/Reaction'), self._toggle_pacingFrame)

        # 'Action'/'Reaction'/'Custom' radiobuttons.
        selectionFrame = ttk.Frame(self._pacingFrame)
        self._customGoal = ''
        self._customConflict = ''
        self._customOutcome = ''
        self._scenePacingType = tk.IntVar()
        ttk.Radiobutton(selectionFrame, text=_('Action'),
                                         variable=self._scenePacingType, value=0, command=self._set_action_scene).pack(side='left', anchor='w')
        ttk.Radiobutton(selectionFrame, text=_('Reaction'),
                                         variable=self._scenePacingType, value=1, command=self._set_reaction_scene).pack(side='left', anchor='w')
        ttk.Radiobutton(selectionFrame, text=_('Custom'),
                                         variable=self._scenePacingType, value=2, command=self._set_custom_ar_scene).pack(anchor='w')
        selectionFrame.pack(fill='x')

        # 'Goal/Reaction' window. The labels are configured dynamically.
        self._goalLabel = ttk.Label(self._pacingFrame)
        self._goalLabel.pack(anchor='w')
        self._goalWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._ui.kwargs['gco_height'],
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._goalWindow.pack(fill='x')

        # 'Conflict/Dilemma' window. The labels are configured dynamically.
        self._conflictLabel = ttk.Label(self._pacingFrame)
        self._conflictLabel.pack(anchor='w')
        self._conflictWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._ui.kwargs['gco_height'],
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._conflictWindow.pack(fill='x')

        # 'Outcome/Choice' window. The labels are configured dynamically.
        self._outcomeLabel = ttk.Label(self._pacingFrame)
        self._outcomeLabel.pack(anchor='w')
        self._outcomeWindow = TextBox(self._pacingFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=self._ui.kwargs['gco_height'],
                padx=5,
                pady=5,
                bg=ui.kwargs['color_text_bg'],
                fg=ui.kwargs['color_text_fg'],
                insertbackground=ui.kwargs['color_text_fg'],
                )
        self._outcomeWindow.pack(fill='x')

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

                # Refresh the "points" display in case an arc has been removed.
                self._ui.tv.update_prj_structure()
                self.set_data(self._element)

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

        super().apply_changes()

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

        #--- Frame for narrative arcs.
        if self._ui.kwargs['show_arcs']:
            self._arcFrame.show()
        else:
            self._arcFrame.hide()

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

    def _set_action_scene(self, event=None):
        self._goalLabel.config(text=_('Goal'))
        self._conflictLabel.config(text=_('Conflict'))
        self._outcomeLabel.config(text=_('Outcome'))

    def _set_custom_ar_scene(self, event=None):
        self._goalLabel.config(text=self._customGoal)
        self._conflictLabel.config(text=self._customConflict)
        self._outcomeLabel.config(text=self._customOutcome)

    def _set_reaction_scene(self, event=None):
        self._goalLabel.config(text=_('Reaction'))
        self._conflictLabel.config(text=_('Dilemma'))
        self._outcomeLabel.config(text=_('Choice'))

    def _toggle_arcFrame(self, event=None):
        """Hide/show the narrative arcs frame."""
        if self._ui.kwargs['show_arcs']:
            self._arcFrame.hide()
            self._ui.kwargs['show_arcs'] = False
        else:
            self._arcFrame.show()
            self._ui.kwargs['show_arcs'] = True

    def _toggle_pacingFrame(self, event=None):
        """Hide/show the 'A/R/C' frame."""
        if self._ui.kwargs['show_action_reaction']:
            self._pacingFrame.hide()
            self._ui.kwargs['show_action_reaction'] = False
        else:
            self._pacingFrame.show()
            self._ui.kwargs['show_action_reaction'] = True

