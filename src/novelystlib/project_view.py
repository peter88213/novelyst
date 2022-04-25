#!/usr/bin/env python3
""""Provide a class for viewing and editing project properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
from novelystlib.element_view import ElementView


class ProjectView(ElementView):
    """A class for viewing and editing project properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)
        row1Cnt = 1
        self._renChapters = tk.BooleanVar(value=element.kwVar['Field_RenumberChapters'])
        self._renChaptersCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Auto number chapters when refreshing the tree',
                                         variable=self._renChapters, onvalue=True, offvalue=False)
        self._renChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._chHdPrefixLabel = tk.Label(ui._valuesWindow, text='Chapter heading prefix')
        self._chHdPrefixLabel.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._chHdPrefix = tk.StringVar(value=element.kwVar['Field_ChapterHeadingPrefix'])
        self._chHdPrefixEntry = tk.Entry(ui._valuesWindow, textvariable=self._chHdPrefix)
        self._chHdPrefixEntry.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._chHdSuffixLabel = tk.Label(ui._valuesWindow, text='Chapter heading suffix')
        self._chHdSuffixLabel.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._chHdSuffix = tk.StringVar(value=element.kwVar['Field_ChapterHeadingSuffix'])
        self._chHdSuffixEntry = tk.Entry(ui._valuesWindow, textvariable=self._chHdSuffix)
        self._chHdSuffixEntry.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._romanChapters = tk.BooleanVar(value=element.kwVar['Field_RomanChapterNumbers'])
        self._romanChaptersCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Use Roman chapter numbers',
                                        variable=self._romanChapters, onvalue=True, offvalue=False)
        self._romanChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._renWithinParts = tk.BooleanVar(value=element.kwVar['Field_RenumberWithinParts'])
        self._renWithinPartsCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Reset chapter number when starting a new part',
                                        variable=self._renWithinParts, onvalue=True, offvalue=False)
        self._renWithinPartsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._renParts = tk.BooleanVar(value=element.kwVar['Field_RenumberParts'])
        self._renPartsCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Auto number parts when refreshing the tree',
                                        variable=self._renParts, onvalue=True, offvalue=False)
        self._renPartsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._ptHdPrefixLabel = tk.Label(ui._valuesWindow, text='Part heading prefix')
        self._ptHdPrefixLabel.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._ptHdPrefix = tk.StringVar(value=element.kwVar['Field_PartHeadingPrefix'])
        self._ptHdPrefixEntry = tk.Entry(ui._valuesWindow, textvariable=self._ptHdPrefix)
        self._ptHdPrefixEntry.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._ptHdSuffixLabel = tk.Label(ui._valuesWindow, text='Part heading suffix')
        self._ptHdSuffixLabel.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._ptHdSuffix = tk.StringVar(value=element.kwVar['Field_PartHeadingSuffix'])
        self._ptHdSuffixEntry = tk.Entry(ui._valuesWindow, textvariable=self._ptHdSuffix)
        self._ptHdSuffixEntry.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._romanParts = tk.BooleanVar(value=element.kwVar['Field_RomanPartNumbers'])
        self._romanPartsCheckbox = ttk.Checkbutton(ui._valuesWindow, text='Use Roman part numbers',
                                        variable=self._romanParts, onvalue=True, offvalue=False)
        self._romanPartsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

    def apply_changes(self):
        """Apply changes.
        
        Extends the superclass method.
        """
        self._element.kwVar['Field_RenumberChapters'] = self._renChapters.get()
        self._renChaptersCheckbox.grid_remove()
        self._element.kwVar['Field_ChapterHeadingPrefix'] = self._chHdPrefix.get()
        self._chHdPrefixLabel.grid_remove()
        self._chHdPrefixEntry.grid_remove()
        self._element.kwVar['Field_ChapterHeadingSuffix'] = self._chHdSuffix.get()
        self._chHdSuffixLabel.grid_remove()
        self._chHdSuffixEntry.grid_remove()
        self._element.kwVar['Field_RomanChapterNumbers'] = self._romanChapters.get()
        self._romanChaptersCheckbox.grid_remove()
        self._element.kwVar['Field_RenumberWithinParts'] = self._renWithinParts.get()
        self._renWithinPartsCheckbox.grid_remove()
        self._element.kwVar['Field_RenumberParts'] = self._renParts.get()
        self._renPartsCheckbox.grid_remove()
        self._element.kwVar['Field_PartHeadingPrefix'] = self._ptHdPrefix.get()
        self._ptHdPrefixLabel.grid_remove()
        self._ptHdPrefixEntry.grid_remove()
        self._element.kwVar['Field_PartHeadingSuffix'] = self._ptHdSuffix.get()
        self._ptHdSuffixLabel.grid_remove()
        self._ptHdSuffixEntry.grid_remove()
        self._element.kwVar['Field_RomanPartNumbers'] = self._romanParts.get()
        self._romanPartsCheckbox.grid_remove()
