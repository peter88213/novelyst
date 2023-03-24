"""Provide a tkinter based class for viewing and editing "Notes" scene properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
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
            ui: NovelystTk -- Reference to the user interface.

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

        # 'Clear date/time' button.
        ttk.Button(sceneStartFrame,
                   text=_('Clear date/time'),
                   command=self._clear_start).pack(side=tk.LEFT, padx=1, pady=2)

        # 'Generate' button.
        ttk.Button(sceneStartFrame,
                   text=_('Generate'),
                   command=self._auto_set).pack(side=tk.LEFT, padx=1, pady=2)

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

        # 'Clear duration' button.
        ttk.Button(sceneDurationFrame,
                   text=_('Clear duration'),
                   command=self._clear_duration).pack(side=tk.LEFT, padx=1, pady=2)

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
                    dispTime = self._element.time.rsplit(':', 1)[0]
                finally:
                    self._startTime.set(dispTime)

        # 'Day' entry.
        if not switchTimeMode:
            newStartDay = self._startDay.get()
            if newStartDay or self._element.day:
                if newStartDay != self._element.day:
                    try:
                        int(newStartDay)
                    except ValueError:
                        self._startDay.set(self._element.day)
                    else:
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
                if not newLastsMinutes:
                    newLastsMinutes = 0
                try:
                    minutes = int(newLastsMinutes)
                except ValueError:
                    wrongEntry = True
                else:
                    hoursLeft, minutes = divmod(minutes, 60)
                    if minutes > 0:
                        newLastsMinutes = str(minutes)
                    else:
                        newLastsMinutes = None
                    self._lastsMinutes.set(newLastsMinutes)
                    newEntry = True

        # 'Duration hours' entry.
        daysLeft = 0
        newLastsHours = self._lastsHours.get()
        if hoursLeft or newLastsHours or self._element.lastsHours:
            if hoursLeft or newLastsHours != self._element.lastsHours:
                try:
                    if newLastsHours:
                        hoursLeft += int(newLastsHours)
                    daysLeft, hoursLeft = divmod(hoursLeft, 24)
                    if hoursLeft > 0:
                        newLastsHours = str(hoursLeft)
                    else:
                        newLastsHours = None
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
                    if newLastsDays:
                        daysLeft += int(newLastsDays)
                    if daysLeft > 0:
                        newLastsDays = str(daysLeft)
                    else:
                        newLastsDays = None
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

    def _clear_start(self):
        """Remove start data from the scene.
        """
        startData = [
            self._element.date,
            self._element.time,
            self._element.day,
            ]
        hasData = False
        for dataElement in startData:
            if dataElement:
                hasData = True
        if hasData and self._ui.ask_yes_no(_('Clear date/time from this scene?')):
            self._element.date = None
            self._element.time = None
            self._element.day = None
            self.set_data(self._element)
            self._ui.isModified = True

    def _auto_set(self):
        """Set scene start to the end of the previous scene.
        """

        def get_scene_end(scene):
            """Return a scene end (date, time, day) tuple calculated from start and duration.
            
            Positional arguments:
                scene -- Scene instance
            """
            endDate = None
            endTime = None
            endDay = None
            # Calculate end date from scene scene duration.
            if scene.lastsDays:
                lastsDays = int(scene.lastsDays)
            else:
                lastsDays = 0
            if scene.lastsHours:
                lastsSeconds = int(scene.lastsHours) * 3600
            else:
                lastsSeconds = 0
            if scene.lastsMinutes:
                lastsSeconds += int(scene.lastsMinutes) * 60
            sceneDuration = timedelta(days=lastsDays, seconds=lastsSeconds)
            if scene.time:
                if scene.date:
                    try:
                        sceneStart = datetime.fromisoformat(f'{scene.date} {scene.time}')
                        sceneEnd = sceneStart + sceneDuration
                        endDate, endTime = sceneEnd.isoformat().split('T')
                    except:
                        pass
                else:
                    try:
                        if scene.day:
                            dayInt = int(scene.day)
                        else:
                            dayInt = 0
                        startDate = (date.min + timedelta(days=dayInt)).isoformat()
                        sceneStart = datetime.fromisoformat(f'{startDate} {scene.time}')
                        sceneEnd = sceneStart + sceneDuration
                        endDate, endTime = sceneEnd.isoformat().split('T')
                        endDay = str((date.fromisoformat(endDate) - date.min).days)
                        endDate = None
                    except:
                        pass
            return endDate, endTime, endDay

        thisNode = self._ui.tv.tree.selection()[0]
        prevNode = self._ui.tv.prev_node(thisNode, '')
        if prevNode:
            scId = prevNode[2:]
            newDate, newTime, newDay = get_scene_end(self._ui.novel.scenes[scId])
            if newTime is not None:
                self._startTime.set(newTime.rsplit(':', 1)[0])
                self._startDate.set(newDate)
                self._startDay.set(newDay)
                self.apply_changes()
            else:
                messagebox.showerror(_('Cannot generate date/time'), _('The previous scene has no date/time set.'))

    def _clear_duration(self):
        """Remove duration data from the scene.
        """
        durationData = [
            self._element.lastsDays,
            self._element.lastsHours,
            self._element.lastsMinutes,
            ]
        hasData = False
        for dataElement in durationData:
            if dataElement:
                hasData = True
        if hasData and self._ui.ask_yes_no(_('Clear duration from this scene?')):
            self._element.lastsDays = None
            self._element.lastsHours = None
            self._element.lastsMinutes = None
            self.set_data(self._element)
            self._ui.isModified = True
