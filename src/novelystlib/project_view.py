""""Provide a class for viewing and editing project properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
from novelystlib.element_view import ElementView
from novelystlib.label_entry import LabelEntry


class ProjectView(ElementView):
    """A class for viewing and editing project properties.
    """

    def __init__(self, ui, element):
        """Show the element's properties.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, element)
        self._renChapters = tk.BooleanVar(value=element.kwVar['Field_RenumberChapters'])
        self._renChaptersCheckbox = ttk.Checkbutton(self._valuesFrame, text='Auto number chapters when refreshing the tree',
                                         variable=self._renChapters, onvalue=True, offvalue=False)
        self._renChaptersCheckbox.pack(anchor='w', pady=2)

        self._chHdPrefix = tk.StringVar(value=element.kwVar['Field_ChapterHeadingPrefix'])
        self._chHdPrefixEntry = LabelEntry(self._valuesFrame, text='Chapter heading prefix', textvariable=self._chHdPrefix)
        self._chHdPrefixEntry.pack(anchor='w', pady=2)

        self._chHdSuffix = tk.StringVar(value=element.kwVar['Field_ChapterHeadingSuffix'])
        self._chHdSuffixEntry = LabelEntry(self._valuesFrame, text='Chapter heading suffix', textvariable=self._chHdSuffix)
        self._chHdSuffixEntry.pack(anchor='w', pady=2)

        self._romanChapters = tk.BooleanVar(value=element.kwVar['Field_RomanChapterNumbers'])
        self._romanChaptersCheckbox = ttk.Checkbutton(self._valuesFrame, text='Use Roman chapter numbers',
                                        variable=self._romanChapters, onvalue=True, offvalue=False)
        self._romanChaptersCheckbox.pack(anchor='w', pady=2)

        self._renWithinParts = tk.BooleanVar(value=element.kwVar['Field_RenumberWithinParts'])
        self._renWithinPartsCheckbox = ttk.Checkbutton(self._valuesFrame, text='Reset chapter number when starting a new part',
                                        variable=self._renWithinParts, onvalue=True, offvalue=False)
        self._renWithinPartsCheckbox.pack(anchor='w', pady=2)

        self._renParts = tk.BooleanVar(value=element.kwVar['Field_RenumberParts'])
        self._renPartsCheckbox = ttk.Checkbutton(self._valuesFrame, text='Auto number parts when refreshing the tree',
                                        variable=self._renParts, onvalue=True, offvalue=False)
        self._renPartsCheckbox.pack(anchor='w', pady=2)

        self._ptHdPrefix = tk.StringVar(value=element.kwVar['Field_PartHeadingPrefix'])
        self._ptHdPrefixEntry = LabelEntry(self._valuesFrame, text='Part heading prefix', textvariable=self._ptHdPrefix)
        self._ptHdPrefixEntry.pack(anchor='w', pady=2)

        self._ptHdSuffix = tk.StringVar(value=element.kwVar['Field_PartHeadingSuffix'])
        self._ptHdSuffixEntry = LabelEntry(self._valuesFrame, text='Part heading suffix', textvariable=self._ptHdSuffix)
        self._ptHdSuffixEntry.pack(anchor='w', pady=2)

        self._romanParts = tk.BooleanVar(value=element.kwVar['Field_RomanPartNumbers'])
        self._romanPartsCheckbox = ttk.Checkbutton(self._valuesFrame, text='Use Roman part numbers',
                                        variable=self._romanParts, onvalue=True, offvalue=False)
        self._romanPartsCheckbox.pack(anchor='w', pady=2)

    def apply_changes(self, ui):
        """Apply changes.
        
        Extends the superclass method.
        """

        def update_field(tkValue, fieldname):
            """Update a custom field if changed.
            
            Positional arguments:
                tkValue -- widget variable holding a value that is not None.
                fieldname -- keyword of a custom field whose value might be None.
            """
            entry = tkValue.get()
            if self._element.kwVar[fieldname] or entry:
                if self._element.kwVar[fieldname] != entry:
                    self._element.kwVar[fieldname] = entry
                    ui.isModified = True

        update_field(self._renChapters, 'Field_RenumberChapters')
        update_field(self._chHdPrefix, 'Field_ChapterHeadingPrefix')
        update_field(self._chHdSuffix, 'Field_ChapterHeadingSuffix')
        update_field(self._romanChapters, 'Field_RomanChapterNumbers')
        update_field(self._renWithinParts, 'Field_RenumberWithinParts')
        update_field(self._renParts, 'Field_RenumberParts')
        update_field(self._ptHdPrefix, 'Field_PartHeadingPrefix')
        update_field(self._ptHdSuffix, 'Field_PartHeadingSuffix')
        update_field(self._romanParts, 'Field_RomanPartNumbers')
        super().apply_changes(ui)

