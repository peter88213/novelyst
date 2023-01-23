"""Provide a tkinter based class for viewing and editing "Notes" scene properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from datetime import date
from datetime import time
from pywriter.pywriter_globals import *
from novelystlib.views.scene_view import SceneView
from novelystlib.widgets.folding_frame import FoldingFrame
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.my_string_var import MyStringVar


class NotesSceneView(SceneView):
    """Class for viewing and editing "Notes" scene properties.

    Adds to the right pane:
    - A folding frame for date/time.

    Public methods:
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes.   
    """
    _DATE_TIME_LBL_X = 15
    # Width of left-placed labels.

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
        ttk.Label(sceneStartFrame, text=_('Start')).pack(anchor=tk.W, pady=2)

        # 'Start date' entry.
        self._startDate = MyStringVar()
        LabelEntry(sceneStartFrame,
                   text=_('Date'),
                   textvariable=self._startDate,
                   lblWidth=self._DATE_TIME_LBL_X).pack(anchor=tk.W, pady=2)

        # 'Start time' entry.
        self._startTime = MyStringVar()
        LabelEntry(sceneStartFrame,
                   text=_('Time'),
                   textvariable=self._startTime,
                   lblWidth=self._DATE_TIME_LBL_X).pack(anchor=tk.W, pady=2)

        # 'Start day' entry.
        self._startDay = MyStringVar()
        LabelEntry(sceneStartFrame,
                   text=_('Day'),
                   textvariable=self._startDay,
                   lblWidth=self._DATE_TIME_LBL_X).pack(anchor=tk.W, pady=2)

        ttk.Separator(self._dateTimeFrame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)

        sceneDurationFrame = ttk.Frame(self._dateTimeFrame)
        sceneDurationFrame.pack(fill=tk.X)
        ttk.Label(sceneDurationFrame, text=_('Duration')).pack(anchor=tk.W, pady=2)

        # 'Duration days' entry.
        self._lastsDays = MyStringVar()
        LabelEntry(sceneDurationFrame,
                   text=_('Days'),
                   textvariable=self._lastsDays,
                   lblWidth=self._DATE_TIME_LBL_X).pack(anchor=tk.W, pady=2)

        # 'Duration hours' entry.
        self._lastsHours = MyStringVar()
        LabelEntry(sceneDurationFrame,
                   text=_('Hours'),
                   textvariable=self._lastsHours,
                   lblWidth=self._DATE_TIME_LBL_X).pack(anchor=tk.W, pady=2)

        # 'Duration minutes' entry.
        self._lastsMinutes = MyStringVar()
        LabelEntry(sceneDurationFrame,
                   text=_('Minutes'),
                   textvariable=self._lastsMinutes,
                   lblWidth=self._DATE_TIME_LBL_X).pack(anchor=tk.W, pady=2)

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        self._startDate.set(self._element.date)

        # Remove the seconds for the display.
        if self._element.time is not None:
            dispTime = self._element.time.rsplit(':', 1)[0]
        else:
            dispTime = None
        self._startTime.set(dispTime)

        self._startDay.set(self._element.day)
        self._lastsDays.set(self._element.lastsDays)
        self._lastsHours.set(self._element.lastsHours)
        self._lastsMinutes.set(self._element.lastsMinutes)

        #--- Frame for date/time.
        if self._ui.kwargs['show_date_time']:
            self._dateTimeFrame.show()
        else:
            self._dateTimeFrame.hide()

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """

        #--- Scene start.
        # Date and time are checked separately.
        # If an invalid date is entered, the old value is kept.
        # If an invalid time is entered, the old value is kept.
        # If a valid date is entered, the day is cleared, if any.
        # Otherwise, if a valid day is entered, the date is cleared, if any.
        switchTimeMode = False

        # 'Date' entry.
        newStartDate = self._startDate.get()
        if newStartDate or self._element.date:
            if newStartDate != self._element.date:
                try:
                    date.fromisoformat(newStartDate)
                except ValueError:
                    self._startDate.set(self._element.date)
                else:
                    self._element.date = newStartDate
                    if self._element.day and self._element.date:
                        switchTimeMode = True
                    self._ui.isModified = True

        # 'Time' entry.
        newStartTime = self._startTime.get()
        if self._element.time is not None:
            dispTime = self._element.time.rsplit(':', 1)[0]
        else:
            dispTime = None
        if newStartTime or dispTime:
            if newStartTime != dispTime:
                try:
                    time.fromisoformat(newStartTime)
                except ValueError:
                    pass
                else:
                    while newStartTime.count(':') < 2:
                        newStartTime = f'{newStartTime}:00'
                    self._element.time = newStartTime
                    self._ui.isModified = True
                finally:
                    self._startTime.set(self._element.time)

        # 'Day' entry.
        if not switchTimeMode:
            newStartDay = self._startDay.get()
            if newStartDay or self._element.day:
                if newStartDay != self._element.day:
                    self._element.day = newStartDay
                    if self._element.date:
                        self._element.date = None
                        switchTimeMode = True
                    self._ui.isModified = True
        else:
            self._element.day = None

        #--- Scene duration.
        # Scene duration changes are applied as a whole.
        # That is, days, hours and minutes entries must all be correct numbers.
        # Otherwise, the old values are kept.
        # If more than 60 minutes are entered in the "Minutes" field,
        # the hours are incremented accordingly.
        # If more than 24 hours are entered in the "Hours" field,
        # the days are incremented accordingly.
        wrongEntry = False
        newEntry = False

        # 'Duration minutes' entry.
        hoursLeft = 0
        newLastsMinutes = self._lastsMinutes.get()
        if newLastsMinutes or self._element.lastsMinutes:
            if newLastsMinutes != self._element.lastsMinutes:
                try:
                    minutes = int(newLastsMinutes)
                    hoursLeft, minutes = divmod(minutes, 60)
                    newLastsMinutes = str(minutes)
                    self._lastsMinutes.set(newLastsMinutes)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        # 'Duration hours' entry.
        daysLeft = 0
        newLastsHours = self._lastsHours.get()
        if hoursLeft or newLastsHours or self._element.lastsHours:
            if hoursLeft or newLastsHours != self._element.lastsHours:
                try:
                    hours = int(newLastsHours) + hoursLeft
                    daysLeft, hours = divmod(hours, 24)
                    newLastsHours = str(hours)
                    self._lastsHours.set(newLastsHours)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        # 'Duration days' entry.
        newLastsDays = self._lastsDays.get()
        if daysLeft or newLastsDays or self._element.lastsDays:
            if daysLeft or newLastsDays != self._element.lastsDays:
                try:
                    days = int(newLastsDays) + daysLeft
                    newLastsDays = str(days)
                    self._lastsDays.set(newLastsDays)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        if wrongEntry:
            self._lastsMinutes.set(self._element.lastsMinutes)
            self._lastsHours.set(self._element.lastsHours)
            self._lastsDays.set(self._element.lastsDays)
        elif newEntry:
            self._element.lastsMinutes = newLastsMinutes
            self._element.lastsHours = newLastsHours
            self._element.lastsDays = newLastsDays
            self._ui.isModified = True

        super().apply_changes()
        if switchTimeMode:
            self.set_data(self._element)

    def _toggle_dateTimeFrame(self, event=None):
        """Hide/show the 'Date/Time' frame."""
        if self._ui.kwargs['show_date_time']:
            self._dateTimeFrame.hide()
            self._ui.kwargs['show_date_time'] = False
        else:
            self._dateTimeFrame.show()
            self._ui.kwargs['show_date_time'] = True

