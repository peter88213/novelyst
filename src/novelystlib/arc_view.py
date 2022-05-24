""""Provide a class for viewing and editing story arc properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from novelystlib.basic_view import BasicView
from novelystlib.label_entry import LabelEntry


class ArcView(BasicView):
    """A class for viewing and editing story arc properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)

        # Place an "Arc" entry inside the frame.
        if element.kwVar['Field_SceneArcs']:
            arcs = element.kwVar['Field_SceneArcs']
        else:
            arcs = ''
        self._arcs = tk.StringVar(value=arcs)
        self._arcsEntry = LabelEntry(self._valuesFrame, text='Arc reference', textvariable=self._arcs)
        self._arcsEntry.pack(anchor=tk.W, pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        # Arc.
        if self._update_field_str(self._arcs, 'Field_SceneArcs'):
            arc = self._element.kwVar['Field_SceneArcs']
            newTitle = f'{arc[0]}{ui.elementTitle.get()[1:]}'
            ui.elementTitle.set(newTitle)
            ui.isModified = True

        super().apply_changes(ui)

