""""Provide a class for viewing and editing story arc properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from novelystlib.basic_view import BasicView
from novelystlib.label_entry import LabelEntry


class ArcView(BasicView):
    """Class for viewing and editing story arc properties."""

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)

        self._scenesAssigned = []
        arc = element.kwVar['Field_SceneArcs']
        if arc:
            for scId in ui.ywPrj.scenes:
                if ui.ywPrj.scenes[scId].isTodoScene:
                    continue
                if ui.ywPrj.scenes[scId].isNotesScene:
                    continue
                if ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs']:
                    if arc in ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs'].split(';'):
                        self._scenesAssigned.append(scId)
        else:
            arc = ''

        # Place an "Arc" entry inside the frame.
        self._arcs = tk.StringVar(value=arc)
        self._arcsEntry = LabelEntry(self._valuesFrame, text='Arc reference', textvariable=self._arcs)
        self._arcsEntry.pack(anchor=tk.W, pady=2)
        if len(self._scenesAssigned) > 0:
            self._nrScenes = tk.Label(self._valuesFrame, text=f'Number of scenes: {len(self._scenesAssigned)}')
            self._nrScenes.pack(anchor=tk.W, pady=2)
            self._removeButton = tk.Button(self._valuesFrame, text='Remove scene assignments', command=lambda: self._removeArcRef(arc, ui))
            self._removeButton.pack(anchor=tk.W, pady=2)

    def _removeArcRef(self, arc, ui):
        """Remove arc reference from all scenes"""
        if arc and ui.ask_yes_no(f'Remove all scenes from the "{arc}" story arc?'):
            for scId in self._scenesAssigned:
                if ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs']:
                    newArcs = []
                    arcs = ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs'].split(';')
                    for scArc in arcs:
                        if not scArc == arc:
                            newArcs.append(scArc)
                        else:
                            ui.isModified = True
                    ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs'] = ';'.join(newArcs)
            self._scenesAssigned = []
            self._nrScenes.destroy()
            self._removeButton.destroy()
            if ui.isModified:
                ui.tv._update_tree()

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        # Arc.
        if self._update_field_str(self._arcs, 'Field_SceneArcs'):
            arc = self._element.kwVar['Field_SceneArcs']

            # Change the first character of the title to the arc's first character.
            newTitle = f'{arc[0]}{ui.elementTitle.get()[1:]}'
            ui.elementTitle.set(newTitle)
            ui.isModified = True

        super().apply_changes(ui)

