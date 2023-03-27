"""Provide a generic class for viewing tree element properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.text_box import TextBox


class BasicView(ttk.Frame):
    """Generic class for viewing tree element properties.
    
    Public methods:
        show() -- Make the ui text boxes and the view visible.
        hide() -- Clear the ui text boxes, and hide the view.
        set_data() -- Update the view with element's data.
        apply_changes() -- Apply changes of element title, description, and notes.   
    """
    _INDEXCARD = False
    _ELEMENT_INFO = False
    _NOTES = False
    _BUTTONBAR = False

    _LBL_X = 10
    # Width of left-placed labels.

    def __init__(self, ui, parent):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.
            parent -- Parent widget to display this widget.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        """
        super().__init__(parent)

        self._ui = ui
        self._element = None
        self._tagsStr = ''
        self._parent = parent

        # Frame for element specific informations.
        self._propertiesFrame = ttk.Frame(self)
        self._propertiesFrame.pack(expand=True, fill=tk.BOTH)

        if self._INDEXCARD:
            self._create_index_card()
        if self._ELEMENT_INFO:
            self._create_element_info_window()
        if self._NOTES:
            self._create_notes_window()
        if self._BUTTONBAR:
            self._create_button_bar()

    def _create_index_card(self):
        """Create an "index card" for element title and description."""
        self._indexCard = tk.Frame(self._propertiesFrame, bd=2, relief=tk.RIDGE)
        self._indexCard.pack(expand=False, fill=tk.BOTH)

        # Title label.
        self._elementTitle = tk.StringVar(value='')
        titleEntry = tk.Entry(self._indexCard, bd=0, textvariable=self._elementTitle, relief=tk.FLAT)
        titleEntry.config({'background': self._ui.kwargs['color_text_bg'],
                           'foreground': self._ui.kwargs['color_text_fg'],
                           'insertbackground': self._ui.kwargs['color_text_fg'],
                           })
        titleEntry.pack(fill=tk.X, ipady=6)

        tk.Frame(self._indexCard, bg='red', height=1, bd=0).pack(fill=tk.X)
        tk.Frame(self._indexCard, bg='white', height=1, bd=0).pack(fill=tk.X)

        # Description window.
        self._descWindow = TextBox(self._indexCard,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=15,
                width=10,
                padx=5,
                pady=5,
                bg=self._ui.kwargs['color_text_bg'],
                fg=self._ui.kwargs['color_text_fg'],
                insertbackground=self._ui.kwargs['color_text_fg'],
                )
        self._descWindow.pack(fill=tk.X)

    def _create_element_info_window(self):
        """Create a window for element specific information."""
        self._elementInfoWindow = ttk.Frame(self._propertiesFrame)
        self._elementInfoWindow.pack(fill=tk.X)

    def _create_notes_window(self):
        """Create a text box for element notes."""
        self._notesWindow = TextBox(self._propertiesFrame,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                height=4,
                width=10,
                padx=5,
                pady=5,
                bg=self._ui.kwargs['color_notes_bg'],
                fg=self._ui.kwargs['color_notes_fg'],
                insertbackground=self._ui.kwargs['color_notes_fg'],
                )
        self._notesWindow.pack(expand=True, fill=tk.BOTH)

    def _create_button_bar(self):
        """Create a button bar at the bottom."""
        self._buttonBar = ttk.Frame(self)
        self._buttonBar.pack(fill=tk.X)

        # "Previous" button.
        ttk.Button(self._buttonBar, text=_('Previous'), command=self._load_prev).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # "Apply changes" button.
        ttk.Button(self._buttonBar, text=_('Apply changes'), command=self.apply_changes).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # "Next" button.
        ttk.Button(self._buttonBar, text=_('Next'), command=self._load_next).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def show(self):
        """Make the view visible."""
        self.pack(expand=True, fill=tk.BOTH)

    def hide(self):
        """Hide the view."""
        self.pack_forget()

    def set_data(self, element):
        """Update the view with element's data."""
        self._tagsStr = ''
        self._element = element
        if self._element is not None:

            # Title entry.
            if self._element.title is not None:
                self._elementTitle.set(self._element.title)
            else:
                self._elementTitle.set('')

            # Description entry.
            self._descWindow.clear()
            self._descWindow.set_text(self._element.desc)

            # Notes entry (if any).
            if hasattr(self._element, 'notes'):
                self._notesWindow.clear()
                self._notesWindow.set_text(self._element.notes)

    def apply_changes(self):
        """Apply changes of element title, description, and notes."""
        if self._element is not None:

            # Title entry.
            title = self._elementTitle.get()
            if title or self._element.title:
                if self._element.title != title:
                    self._element.title = title.strip()
                    self._ui.isModified = True

            # Description entry.
            if self._descWindow.hasChanged:
                desc = self._descWindow.get_text()
                if desc or self._element.desc:
                    if self._element.desc != desc:
                        self._element.desc = desc
                        self._ui.isModified = True

            # Notes entry (if any).
            if hasattr(self._element, 'notes') and self._notesWindow.hasChanged:
                notes = self._notesWindow.get_text()
                if hasattr(self._element, 'notes'):
                    if notes or self._element.notes:
                        if self._element.notes != notes:
                            self._element.notes = notes
                            self._ui.isModified = True

        if self._ui.isModified:
            self._ui.tv.update_prj_structure()

    def _update_field_str(self, tkValue, fieldname):
        """Update a custom field and return True if changed. 
               
        Positional arguments:
            tkValue -- widget variable holding a string that is not None.
            fieldname -- keyword of a custom field whose value might be None.
        """
        entry = tkValue.get()
        if self._element.kwVar.get(fieldname, None) or entry:
            if self._element.kwVar.get(fieldname, None) != entry:
                self._element.kwVar[fieldname] = entry
                return True
        return False

    def _update_field_bool(self, tkValue, fieldname):
        """Update a custom field and return True if changed.
        
        Positional arguments:
            tkValue -- widget variable holding a boolean value.
            fieldname -- keyword of a custom field.
            
        Custom field value convention:
        '1' means True
        None means False 
        """
        entry = tkValue.get()
        if entry:
            value = '1'
        else:
            value = None
        if self._element.kwVar.get(fieldname, None) or value:
            if self._element.kwVar.get(fieldname, None) != value:
                self._element.kwVar[fieldname] = value
                return True
        return False

    def _load_prev(self):
        """Load the next tree element of the same type."""
        thisNode = self._ui.tv.tree.selection()[0]
        prevNode = self._ui.tv.prev_node(thisNode, '')
        if prevNode:
            self._ui.tv.tree.see(prevNode)
            self._ui.tv.tree.selection_set(prevNode)

    def _load_next(self):
        """Load the next tree element of the same type."""
        thisNode = self._ui.tv.tree.selection()[0]
        nextNode = self._ui.tv.next_node(thisNode, '')
        if nextNode:
            self._ui.tv.tree.see(nextNode)
            self._ui.tv.tree.selection_set(nextNode)
