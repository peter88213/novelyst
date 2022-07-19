""""Provide a tkinter based class for viewing and editing scene properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from novelystlib.basic_view import BasicView
from novelystlib.label_combo import LabelCombo
from novelystlib.label_entry import LabelEntry


class SceneView(BasicView):
    """Class for viewing and editing scene properties."""
    _GCO_Y = 1
    # height of the Goals/Conflict/Outcome text boxes

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)
        # Place a "Tags" entry inside the frame.
        if element.tags is not None:
            tags = ';'.join(element.tags)
        else:
            tags = ''
        self._tags = tk.StringVar(value=tags)
        self._tagsEntry = LabelEntry(self._valuesFrame, text='Tags', textvariable=self._tags)
        self._tagsEntry.pack(anchor=tk.W, pady=2)

        # "Append to previous scene" checkbox.
        self._appendToPrev = tk.BooleanVar(value=element.appendToPrev)
        self._appendToPrevCheckbox = ttk.Checkbutton(self._valuesFrame, text='Append to previous scene',
                                         variable=self._appendToPrev, onvalue=True, offvalue=False)
        self._appendToPrevCheckbox.pack(anchor=tk.W, pady=2)

        # "Notes" window.
        if element.sceneNotes is not None:
            ui.notesWindow.insert(tk.END, element.sceneNotes)

        # "Scene viewpoint" combobox.
        charList = []
        for crId in ui.ywPrj.srtCharacters:
            charList.append(ui.ywPrj.characters[crId].title)
        if element.characters:
            vp = ui.ywPrj.characters[element.characters[0]].title
        else:
            vp = ''
        self._viewpoint = tk.StringVar(value=vp)
        self._characterCombobox = LabelCombo(self._valuesFrame, text='Viewpoint', textvariable=self._viewpoint, values=charList)
        self._characterCombobox.pack(anchor=tk.W, pady=2)

        # "Action/Reaction Scene" radiobuttons.
        if element.isReactionScene:
            pacingType = 1
        else:
            pacingType = 0
        self._isReactionScene = tk.IntVar(value=pacingType)
        pacingFrame = tk.Frame(self._valuesFrame)
        pacingFrame.pack(anchor=tk.W)
        tk.Radiobutton(pacingFrame, text='Action scene',
                                         variable=self._isReactionScene, value=0, command=self._set_action_scene).pack(side=tk.LEFT, anchor=tk.W, pady=2)

        tk.Radiobutton(pacingFrame, text='Reaction scene',
                                         variable=self._isReactionScene, value=1, command=self._set_reaction_scene).pack(anchor=tk.W, pady=2)

        # Place a "Goal/Reaction" window inside its own frame.
        goalFrame = tk.Frame(self._valuesFrame)
        self._goalLabel = tk.Label(goalFrame, text='', anchor=tk.W, width=self._LBL_X)
        self._goalLabel.pack(side=tk.LEFT)
        self._goalWindow = scrolledtext.ScrolledText(goalFrame, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=self._GCO_Y, padx=5, pady=5)
        self._goalWindow.pack(fill=tk.X, side=tk.LEFT)
        if element.goal:
            self._goalWindow.insert(tk.END, element.goal)
        goalFrame.pack(anchor=tk.W)

        # Place a "Conflict/Dilemma" window inside its own frame.
        conflictFrame = tk.Frame(self._valuesFrame)
        self._conflictLabel = tk.Label(conflictFrame, text='', anchor=tk.W, width=self._LBL_X)
        self._conflictLabel.pack(side=tk.LEFT)
        self._conflictWindow = scrolledtext.ScrolledText(conflictFrame, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=self._GCO_Y, padx=5, pady=5)
        self._conflictWindow.pack(fill=tk.X, side=tk.LEFT)
        if element.conflict:
            self._conflictWindow.insert(tk.END, element.conflict)
        conflictFrame.pack(anchor=tk.W)

        # Place an "Outcome/Choice" window inside its own frame.
        outcomeFrame = tk.Frame(self._valuesFrame)
        self._outcomeLabel = tk.Label(outcomeFrame, text='', anchor=tk.W, width=self._LBL_X)
        self._outcomeLabel.pack(side=tk.LEFT)
        self._outcomeWindow = scrolledtext.ScrolledText(outcomeFrame, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=self._GCO_Y, padx=5, pady=5)
        self._outcomeWindow.pack(fill=tk.X, side=tk.LEFT)
        if element.outcome:
            self._outcomeWindow.insert(tk.END, element.outcome)
        outcomeFrame.pack(anchor=tk.W)

        # Configure the labels.
        if pacingType == 0:
            self._set_action_scene()
        else:
            self._set_reaction_scene()

        # Place an "Arcs" entry (if any) inside the frame.
        if element.kwVar['Field_SceneArcs']:
            arcs = element.kwVar['Field_SceneArcs']
        else:
            arcs = ''
        self._arcs = tk.StringVar(value=arcs)
        self._arcsEntry = LabelEntry(self._valuesFrame, text='Arcs', textvariable=self._arcs)
        self._arcsEntry.pack(anchor=tk.W, pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self._element.tags:
            elementTags = ';'.join(self._element.tags)
        else:
            elementTags = None
        newTags = self._tags.get()
        if elementTags or newTags:
            if newTags != elementTags:
                self._element.tags = newTags.split(';')
                ui.isModified = True

        # Append to previous scene.
        appendToPrev = self._appendToPrev.get()
        if self._element.appendToPrev or appendToPrev:
            if self._element.appendToPrev != appendToPrev:
                self._element.appendToPrev = appendToPrev
                ui.isModified = True

        # Scene notes.
        notes = ui.notesWindow.get('1.0', tk.END).strip(' \n')
        if notes or self._element.sceneNotes:
            if self._element.sceneNotes != notes:
                self._element.sceneNotes = notes
                ui.isModified = True

        # Scene viewpoint.
        option = self._characterCombobox.current()
        if self._element.characters:
            oldVpId = self._element.characters[0]
        else:
            oldVpId = None
        if option >= 0:
            newVpId = ui.ywPrj.srtCharacters[option]
            if oldVpId:
                if newVpId != oldVpId:
                    try:
                        self._element.characters.remove(newVpId)
                    except:
                        pass
                    self._element.characters.insert(0, newVpId)
                    ui.isModified = True
            else:
                self._element.characters = []
                self._element.characters.append(newVpId)
                ui.isModified = True

        # Pacing type
        isReactionScene = self._isReactionScene.get() == 1
        if self._element.isReactionScene != isReactionScene:
            self._element.isReactionScene = isReactionScene
            ui.isModified = True

        # Goal/Reaction
        goal = self._goalWindow.get('1.0', tk.END).strip(' \n')
        if goal or self._element.goal:
            if self._element.goal != goal:
                self._element.goal = goal
                ui.isModified = True

        # Conflict/Dilemma
        conflict = self._conflictWindow.get('1.0', tk.END).strip(' \n')
        if conflict or self._element.conflict:
            if self._element.conflict != conflict:
                self._element.conflict = conflict
                ui.isModified = True

        # Outcome/Choice
        outcome = self._outcomeWindow.get('1.0', tk.END).strip(' \n')
        if outcome or self._element.outcome:
            if self._element.outcome != outcome:
                self._element.outcome = outcome
                ui.isModified = True

        # Arcs the scene belongs to.
        if self._update_field_str(self._arcs, 'Field_SceneArcs'):
            ui.isModified = True

        super().apply_changes(ui)

    def _set_action_scene(self, event=None):
        self._goalLabel.config(text='Goal')
        self._conflictLabel.config(text='Conflict')
        self._outcomeLabel.config(text='Outcome')

    def _set_reaction_scene(self, event=None):
        self._goalLabel.config(text='Reaction')
        self._conflictLabel.config(text='Dilemma')
        self._outcomeLabel.config(text='Choice')
