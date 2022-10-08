""""Provide a tkinter based class for viewing and editing project properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.views.basic_view import BasicView
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.widgets.label_disp import LabelDisp
from novelystlib.widgets.my_string_var import MyStringVar
from novelystlib.widgets.folding_frame import FoldingFrame


class ProjectView(BasicView):
    """Class for viewing and editing project properties."""

    def __init__(self, ui):
        """Initialize the view once before element date is available.
        
        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui)

        #--- Author entry.
        self._authorName = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Author'), textvariable=self._authorName, lblWidth=20).pack(anchor='w', pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        #--- "Project settings" frame.
        self._settingsFrame = FoldingFrame(self._elementInfoWindow, _('Project settings'), self._toggle_settingsFrame)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # Language and country code.
        self._languageCode = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Language code'),
                   textvariable=self._languageCode, lblWidth=20).pack(anchor='w', pady=2)
        self._countryCode = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Country code'),
                   textvariable=self._countryCode, lblWidth=20).pack(anchor='w', pady=2)

        # 'Auto number chapters...' checkbox.
        self._renChapters = tk.BooleanVar(value=False)
        ttk.Checkbutton(self._settingsFrame, text=_('Auto number chapters when refreshing the tree'),
                        variable=self._renChapters, onvalue=True, offvalue=False).pack(anchor='w', pady=2)

        # 'Chapter number prefix' entry.
        self._chHdPrefix = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Chapter number prefix'),
                   textvariable=self._chHdPrefix, lblWidth=20).pack(anchor='w', pady=2)

        # 'Chapter number suffix' entry.
        self._chHdSuffix = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Chapter number suffix'),
                   textvariable=self._chHdSuffix, lblWidth=20).pack(anchor='w', pady=2)

        # 'Use Roman chapter numbers' checkbox.
        self._romanChapters = tk.BooleanVar()
        ttk.Checkbutton(self._settingsFrame, text=_('Use Roman chapter numbers'),
                        variable=self._romanChapters, onvalue=True, offvalue=False).pack(anchor='w', pady=2)

        # 'Reset chapter number..." checkbox
        self._renWithinParts = tk.BooleanVar()
        ttk.Checkbutton(self._settingsFrame, text=_('Reset chapter number when starting a new part'),
                        variable=self._renWithinParts, onvalue=True, offvalue=False).pack(anchor='w', pady=2)

        # 'Auto number parts' checkbox.
        self._renParts = tk.BooleanVar()
        ttk.Checkbutton(self._settingsFrame, text=_('Auto number parts when refreshing the tree'),
                        variable=self._renParts, onvalue=True, offvalue=False).pack(anchor='w', pady=2)

        # 'Part number prefix' entry.
        self._ptHdPrefix = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Part number prefix'),
                   textvariable=self._ptHdPrefix, lblWidth=20).pack(anchor='w', pady=2)

        # 'Part number suffix' entry.
        self._ptHdSuffix = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Part number suffix'),
                   textvariable=self._ptHdSuffix, lblWidth=20).pack(anchor='w', pady=2)

        # 'Use Roman part numbers' checkbox.
        self._romanParts = tk.BooleanVar()
        ttk.Checkbutton(self._settingsFrame, text=_('Use Roman part numbers'), variable=self._romanParts, onvalue=True, offvalue=False).pack(anchor='w', pady=2)

        ttk.Separator(self._settingsFrame, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # 'Use Roman part numbers' checkbox.
        self._customGoal = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Custom Goal'),
                   textvariable=self._customGoal, lblWidth=20).pack(anchor='w', pady=2)

        # 'Custom Conflict' entry.
        self._customConflict = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Custom Conflict'),
                   textvariable=self._customConflict, lblWidth=20).pack(anchor='w', pady=2)

        # 'Custom Outcome' entry.
        self._customOutcome = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Custom Outcome'),
                   textvariable=self._customOutcome, lblWidth=20).pack(anchor='w', pady=2)

        ttk.Separator(self._settingsFrame, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # 'Custom Bio' entry.
        self._customChrBio = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Custom chara Bio'),
                   textvariable=self._customChrBio, lblWidth=20).pack(anchor='w', pady=2)

        # 'Custom chara Goals' entry.
        self._customChrGoals = MyStringVar()
        LabelEntry(self._settingsFrame, text=_('Custom chara Goals'),
                   textvariable=self._customChrGoals, lblWidth=20).pack(anchor='w', pady=2)

        ttk.Separator(self._settingsFrame, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # 'Save word count' entry.
        self._saveWordCount = tk.BooleanVar()
        ttk.Checkbutton(self._settingsFrame, text=_('Save word count'),
                        variable=self._saveWordCount, onvalue=True, offvalue=False).pack(anchor='w', pady=2)

        #--- "Writing progress" frame.
        self._progressFrame = FoldingFrame(self._elementInfoWindow, _('Writing progress'), self._toggle_progressFrame)

        # 'Words to write' entry.
        self._wordTarget = tk.IntVar()
        LabelEntry(self._progressFrame, text=_('Words to write'),
                   textvariable=self._wordTarget, lblWidth=20).pack(anchor='w', pady=2)

        # 'Starting count' entry.
        self._wordCountStart = tk.IntVar()
        LabelEntry(self._progressFrame, text=_('Starting count'),
                   textvariable=self._wordCountStart, lblWidth=20).pack(anchor='w', pady=2)

        # 'Set actual wordcount as start' button.
        ttk.Button(self._progressFrame, text=_('Set actual wordcount as start'),
                  command=self._set_initial_wc).pack(pady=2)

        # 'Words written' display.
        self._wordsWritten = MyStringVar()
        self._wordTarget.trace_add('write', self._update_wordsWritten)
        self._wordCountStart.trace_add('write', self._update_wordsWritten)
        LabelDisp(self._progressFrame, text=_('Words written'),
                  textvariable=self._wordsWritten, lblWidth=20).pack(anchor='w', pady=2)

        ttk.Separator(self._elementInfoWindow, orient=tk.HORIZONTAL).pack(fill=tk.X)

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        #--- Author entry.
        self._authorName.set(self._element.authorName)

        #--- "Project settings" frame.
        if self._ui.kwargs['show_project_settings']:
            self._settingsFrame.show()
        else:
            self._settingsFrame.hide()

        # 'Language code' entry.
        self._languageCode.set(self._element.kwVar.get('Field_LanguageCode', ''))

        # 'Country code' entry.
        self._countryCode.set(self._element.kwVar.get('Field_CountryCode', ''))

        # 'Auto number chapters' checkbox.
        renChapters = self._element.kwVar.get('Field_RenumberChapters', None) == '1'
        self._renChapters.set(renChapters)

        # 'Chapter number prefix' entry.
        self._chHdPrefix.set(self._element.kwVar.get('Field_ChapterHeadingPrefix', ''))

        # 'Chapter number suffix' entry.
        self._chHdSuffix = MyStringVar(value=self._element.kwVar.get('Field_ChapterHeadingSuffix', ''))

        # 'Use Roman chapter numbers' checkbox.
        romanChapters = self._element.kwVar.get('Field_RomanChapterNumbers', None) == '1'
        self._romanChapters.set(romanChapters)

        # 'Reset chapter number..." checkbox
        renWithinParts = self._element.kwVar.get('Field_RenumberWithinParts', None) == '1'
        self._renWithinParts.set(renWithinParts)

        # 'Auto number parts' checkbox.
        renParts = self._element.kwVar.get('Field_RenumberParts', None) == '1'
        self._renParts.set(renParts)

        # 'Part number prefix' entry.
        self._ptHdPrefix.set(self._element.kwVar.get('Field_PartHeadingPrefix', ''))

        # 'Part number suffix' entry.
        self._ptHdSuffix.set(self._element.kwVar.get('Field_PartHeadingSuffix', ''))

        # 'Use Roman part numbers' checkbox.
        romanParts = self._element.kwVar.get('Field_RomanPartNumbers', None) == 1
        self._romanParts.set(romanParts)

        # 'Use Roman part numbers' checkbox.
        self._customGoal.set(self._element.kwVar.get('Field_CustomGoal', _('Goal')))

        # 'Custom Conflict' entry.
        self._customConflict.set(self._element.kwVar.get('Field_CustomConflict', _('Conflict')))

        # 'Custom Outcome' entry.
        self._customOutcome.set(self._element.kwVar.get('Field_CustomOutcome', _('Outcome')))

        # 'Custom Bio' entry.
        self._customChrBio.set(self._element.kwVar.get('Field_CustomChrBio', _('Bio')))

        # 'Custom chara Goals' entry.
        self._customChrGoals.set(self._element.kwVar.get('Field_CustomChrGoals', _('Goals')))

        # 'Save word count' entry.
        saveWordCount = self._element.kwVar.get('Field_SaveWordCount', None) == '1'
        self._saveWordCount.set(saveWordCount)

        #--- "Writing progress" frame.
        if self._ui.kwargs['show_writing_progress']:
            self._progressFrame.show()
        else:
            self._progressFrame.hide()

        # 'Words to write' entry.
        self._wordTarget.set(self._element.wordTarget)

        # 'Starting count' entry.
        self._wordCountStart.set(self._element.wordCountStart)

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        # Title
        title = self._ui.elementTitle.get()
        if title or self._element.title:
            if self._element.title != title:
                self._element.title = title.strip()
                self._ui.isModified = True
                self._ui.set_title()

        # Author
        authorName = self._authorName.get()
        if authorName or self._element.authorName:
            if self._element.authorName != authorName:
                self._element.authorName = authorName.strip()
                self._ui.isModified = True
                self._ui.set_title()

        #--- Project settings
        if self._update_field_str(self._languageCode, 'Field_LanguageCode'):
            if self._element.check_locale():
                self._ui.isModified = True
            else:
                self._languageCode.set(self._element.kwVar['Field_LanguageCode'])

        if self._update_field_str(self._countryCode, 'Field_CountryCode'):
            if self._element.check_locale():
                self._ui.isModified = True
            else:
                self._countryCode.set(self._element.kwVar['Field_CountryCode'])

        if self._update_field_bool(self._renChapters, 'Field_RenumberChapters'):
            self._ui.isModified = True

        if self._update_field_str(self._chHdPrefix, 'Field_ChapterHeadingPrefix'):
            self._ui.isModified = True

        if self._update_field_str(self._chHdSuffix, 'Field_ChapterHeadingSuffix'):
            self._ui.isModified = True

        if self._update_field_bool(self._romanChapters, 'Field_RomanChapterNumbers'):
            self._ui.isModified = True

        if self._update_field_bool(self._renWithinParts, 'Field_RenumberWithinParts'):
            self._ui.isModified = True

        if self._update_field_bool(self._renParts, 'Field_RenumberParts'):
            self._ui.isModified = True

        if self._update_field_str(self._ptHdPrefix, 'Field_PartHeadingPrefix'):
            self._ui.isModified = True

        if self._update_field_str(self._ptHdSuffix, 'Field_PartHeadingSuffix'):
            self._ui.isModified = True

        if self._update_field_bool(self._romanParts, 'Field_RomanPartNumbers'):
            self._ui.isModified = True

        if self._update_field_str(self._customGoal, 'Field_CustomGoal'):
            self._ui.isModified = True

        if self._update_field_str(self._customConflict, 'Field_CustomConflict'):
            self._ui.isModified = True

        if self._update_field_str(self._customOutcome, 'Field_CustomOutcome'):
            self._ui.isModified = True

        if self._update_field_str(self._customChrBio, 'Field_CustomChrBio'):
            self._ui.isModified = True

        if self._update_field_str(self._customChrGoals, 'Field_CustomChrGoals'):
            self._ui.isModified = True

        if self._update_field_bool(self._saveWordCount, 'Field_SaveWordCount'):
            self._ui.isModified = True

        try:
            entry = self._wordTarget.get()
            # entry must be an integer
            if self._element.wordTarget or entry:
                if self._element.wordTarget != entry:
                    self._element.wordTarget = entry
                    self._ui.isModified = True
        except:
            # entry is no integer
            pass
        try:
            entry = self._wordCountStart.get()
            # entry must be an integer
            if self._element.wordCountStart or entry:
                if self._element.wordCountStart != entry:
                    self._element.wordCountStart = entry
                    self._ui.isModified = True
        except:
            # entry is no integer
            pass
        super().apply_changes()

    def _set_initial_wc(self):
        """Set actual wordcount as start.
        
        Callback procedure for the related button.
        """
        self._wordCountStart.set(self._ui.wordCount)

    def _toggle_settingsFrame(self, event=None):
        """Hide/show the "Project settings" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if self._ui.kwargs['show_project_settings']:
            self._settingsFrame.hide()
            self._ui.kwargs['show_project_settings'] = False
        else:
            self._settingsFrame.show()
            self._ui.kwargs['show_project_settings'] = True

    def _toggle_progressFrame(self, event=None):
        """Hide/show the "Project settings" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if self._ui.kwargs['show_writing_progress']:
            self._progressFrame.hide()
            self._ui.kwargs['show_writing_progress'] = False
        else:
            self._progressFrame.show()
            self._ui.kwargs['show_writing_progress'] = True

    def _update_wordsWritten(self, n, m, x):
        """Calculate the percentage of written words.
        
        Callback procedure for traced variables:
        - self._wordCountStart
        - self._wordTarget
        """
        try:
            ww = self._ui.wordCount - self._wordCountStart.get()
            wt = self._wordTarget.get()
            try:
                wp = f'({round(100*ww/wt)}%)'
            except ZeroDivisionError:
                wp = ''
            self._wordsWritten.set(f'{ww} {wp}')
        except:
            pass

