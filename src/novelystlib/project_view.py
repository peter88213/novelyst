""""Provide a tkinter based class for viewing and editing project properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
from novelystlib.element_view import BasicView
from novelystlib.label_entry import LabelEntry
from novelystlib.label_disp import LabelDisp


class ProjectView(BasicView):
    """Class for viewing and editing project properties."""

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)
        self._authorName = tk.StringVar(value=element.authorName)
        self._authorNameEntry = LabelEntry(self._valuesFrame, text='Author', textvariable=self._authorName, lblWidth=20)
        self._authorNameEntry.pack(anchor='w', pady=2)

        renChapters = element.kwVar['Field_RenumberChapters'] == '1'
        self._renChapters = tk.BooleanVar(value=renChapters)
        self._renChaptersCheckbox = ttk.Checkbutton(self._valuesFrame, text='Auto number chapters when refreshing the tree',
                                         variable=self._renChapters, onvalue=True, offvalue=False)
        self._renChaptersCheckbox.pack(anchor='w', pady=2)

        self._chHdPrefix = tk.StringVar(value=element.kwVar['Field_ChapterHeadingPrefix'])
        self._chHdPrefixEntry = LabelEntry(self._valuesFrame, text='Chapter heading prefix', textvariable=self._chHdPrefix, lblWidth=20)
        self._chHdPrefixEntry.pack(anchor='w', pady=2)

        self._chHdSuffix = tk.StringVar(value=element.kwVar['Field_ChapterHeadingSuffix'])
        self._chHdSuffixEntry = LabelEntry(self._valuesFrame, text='Chapter heading suffix', textvariable=self._chHdSuffix, lblWidth=20)
        self._chHdSuffixEntry.pack(anchor='w', pady=2)

        romanChapters = element.kwVar['Field_RomanChapterNumbers'] == '1'
        self._romanChapters = tk.BooleanVar(value=romanChapters)
        self._romanChaptersCheckbox = ttk.Checkbutton(self._valuesFrame, text='Use Roman chapter numbers',
                                        variable=self._romanChapters, onvalue=True, offvalue=False)
        self._romanChaptersCheckbox.pack(anchor='w', pady=2)

        renWithinParts = element.kwVar['Field_RenumberWithinParts'] == '1'
        self._renWithinParts = tk.BooleanVar(value=renWithinParts)
        self._renWithinPartsCheckbox = ttk.Checkbutton(self._valuesFrame, text='Reset chapter number when starting a new part',
                                        variable=self._renWithinParts, onvalue=True, offvalue=False)
        self._renWithinPartsCheckbox.pack(anchor='w', pady=2)

        renParts = element.kwVar['Field_RenumberParts'] == '1'
        self._renParts = tk.BooleanVar(value=renParts)
        self._renPartsCheckbox = ttk.Checkbutton(self._valuesFrame, text='Auto number parts when refreshing the tree',
                                        variable=self._renParts, onvalue=True, offvalue=False)
        self._renPartsCheckbox.pack(anchor='w', pady=2)

        self._ptHdPrefix = tk.StringVar(value=element.kwVar['Field_PartHeadingPrefix'])
        self._ptHdPrefixEntry = LabelEntry(self._valuesFrame, text='Part heading prefix', textvariable=self._ptHdPrefix, lblWidth=20)
        self._ptHdPrefixEntry.pack(anchor='w', pady=2)

        self._ptHdSuffix = tk.StringVar(value=element.kwVar['Field_PartHeadingSuffix'])
        self._ptHdSuffixEntry = LabelEntry(self._valuesFrame, text='Part heading suffix', textvariable=self._ptHdSuffix, lblWidth=20)
        self._ptHdSuffixEntry.pack(anchor='w', pady=2)

        romanParts = element.kwVar['Field_RomanPartNumbers'] == 1
        self._romanParts = tk.BooleanVar(value=romanParts)
        self._romanPartsCheckbox = ttk.Checkbutton(self._valuesFrame, text='Use Roman part numbers',
                                        variable=self._romanParts, onvalue=True, offvalue=False)
        self._romanPartsCheckbox.pack(anchor='w', pady=2)

        self._wordCountStart = tk.IntVar(value=element.wordCountStart)
        self._wordCountStartEntry = LabelEntry(self._valuesFrame, text='Starting count', textvariable=self._wordCountStart, lblWidth=20)
        self._wordCountStartEntry.pack(anchor='w', pady=2)

        self._wordTarget = tk.IntVar(value=element.wordTarget)
        self._wordTargetEntry = LabelEntry(self._valuesFrame, text='Words to write', textvariable=self._wordTarget, lblWidth=20)
        self._wordTargetEntry.pack(anchor='w', pady=2)

        wordsWritten = tk.StringVar(value=ui.wordCount - element.wordCountStart)
        wordsWrittenDisp = LabelDisp(self._valuesFrame, text='Words written', textvariable=wordsWritten, lblWidth=20)
        wordsWrittenDisp.pack(anchor='w', pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """
        authorName = self._authorName.get()
        if authorName or self._element.authorName:
            if self._element.authorName != authorName:
                self._element.authorName = authorName.strip()
                ui.isModified = True
        if self._update_field_bool(self._renChapters, 'Field_RenumberChapters'):
                ui.isModified = True
        if self._update_field_str(self._chHdPrefix, 'Field_ChapterHeadingPrefix'):
                ui.isModified = True
        if self._update_field_str(self._chHdSuffix, 'Field_ChapterHeadingSuffix'):
                ui.isModified = True
        if self._update_field_bool(self._romanChapters, 'Field_RomanChapterNumbers'):
                ui.isModified = True
        if self._update_field_bool(self._renWithinParts, 'Field_RenumberWithinParts'):
                ui.isModified = True
        if self._update_field_bool(self._renParts, 'Field_RenumberParts'):
                ui.isModified = True
        if self._update_field_str(self._ptHdPrefix, 'Field_PartHeadingPrefix'):
                ui.isModified = True
        if self._update_field_str(self._ptHdSuffix, 'Field_PartHeadingSuffix'):
                ui.isModified = True
        if self._update_field_bool(self._romanParts, 'Field_RomanPartNumbers'):
                ui.isModified = True
        try:
            entry = self._wordTarget.get()
            # entry must be an integer
            if self._element.wordTarget or entry:
                if self._element.wordTarget != entry:
                    self._element.wordTarget = entry
                    ui.isModified = True
        except:
            # entry is no integer
            pass
        try:
            entry = self._wordCountStart.get()
            # entry must be an integer
            if self._element.wordCountStart or entry:
                if self._element.wordCountStart != entry:
                    self._element.wordCountStart = entry
                    ui.isModified = True
        except:
            # entry is no integer
            pass
        super().apply_changes(ui)

