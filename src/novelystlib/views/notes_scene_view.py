"""Provide a tkinter based class for viewing and editing "Notes" scene properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.views.scene_view import SceneView
from novelystlib.widgets.folding_frame import FoldingFrame


class NotesSceneView(SceneView):
    """Class for viewing and editing "Notes" scene properties.
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

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- Frame for date/time/duration.
        self._dateTimeFrame = FoldingFrame(self._elementInfoWindow, _('Date/Time'), self._toggle_dateTimeFrame)
        sceneStartFrame = ttk.Frame(self._dateTimeFrame)
        sceneStartFrame.pack(fill=tk.X)

        self._startDate = tk.StringVar()
        self._startTime = tk.StringVar()

        self._startDays = tk.IntVar()
        self._startHours = tk.IntVar()
        self._startMinutes = tk.IntVar()

        sceneDurationFrame = ttk.Frame(self._dateTimeFrame)
        sceneDurationFrame.pack(fill=tk.X)

        self._lastsDays = tk.IntVar()
        self._lastsHours = tk.IntVar()
        self._lastsMinutes = tk.IntVar()

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        #--- Frame for date/time.
        if self._ui.kwargs['show_date_time']:
            self._dateTimeFrame.show()
        else:
            self._dateTimeFrame.hide()

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """

        super().apply_changes()

    def _toggle_dateTimeFrame(self, event=None):
        """Hide/show the 'Date/Time' frame."""
        if self._ui.kwargs['show_date_time']:
            self._dateTimeFrame.hide()
            self._ui.kwargs['show_date_time'] = False
        else:
            self._dateTimeFrame.show()
            self._ui.kwargs['show_date_time'] = True

