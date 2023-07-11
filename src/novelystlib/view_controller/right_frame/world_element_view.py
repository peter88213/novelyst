"""Provide a tkinter based class for viewing world element properties.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import ttk
from shutil import copyfile
import tkinter as tk
from tkinter import filedialog
from pywriter.pywriter_globals import *
from pywriter.file.doc_open import open_document
from novelystlib.widgets.label_entry import LabelEntry
from novelystlib.view_controller.right_frame.basic_view import BasicView
from novelystlib.widgets.my_string_var import MyStringVar


class WorldElementView(BasicView):
    """Class for viewing world element properties.
    
    Adds to the right pane:
    - An "Aka" entry.
    - A "Tags" entry.   
     
    Public methods:
        apply_changes() -- Apply changes.   
        set_data() -- Update the view with element's data.
    """

    def __init__(self, ui, parent):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            ui: NovelystTk -- Reference to the user interface.
            parent -- Parent widget to display this widget.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super(). __init__(ui, parent)

        self._fullNameFrame = ttk.Frame(self._elementInfoWindow)
        self._fullNameFrame.pack(anchor='w', fill='x')

        # 'AKA' entry.
        self._aka = MyStringVar()
        self._akaEntry = LabelEntry(self._elementInfoWindow, text=_('AKA'), textvariable=self._aka, lblWidth=self._LBL_X).pack(anchor='w', pady=2)

        # 'Tags' entry.
        self._tags = MyStringVar()
        LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X).pack(anchor='w', pady=2)

    def apply_changes(self):
        """Apply changes of element title, description and notes."""

        # 'AKA' entry.
        aka = self._aka.get()
        if aka or self._element.aka:
            if self._element.aka != aka:
                self._element.aka = aka.strip()
                self._ui.isModified = True
        if self._ui.isModified:
            self._ui.tv.update_prj_structure()

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            if newTags != self._tagsStr:
                self._element.tags = string_to_list(newTags)
                self._ui.isModified = True

        super().apply_changes()

    def set_data(self, element):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(element)

        # 'AKA' entry.
        self._aka.set(self._element.aka)

        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

        # Image buttonbar.
        if self._element.image:
            self._img_show_button.state(['!disabled'])
            self._img_clear_button.state(['!disabled'])
        else:
            self._img_show_button.state(['disabled'])
            self._img_clear_button.state(['disabled'])

    def _create_image_window(self):
        """Create a window for element specific information."""
        self._imageWindow = ttk.Frame(self._propertiesFrame)
        self._imageWindow.pack(fill='x')
        ttk.Separator(self._imageWindow, orient='horizontal').pack(fill='x')
        self._img_show_button = ttk.Button(self._imageWindow, text=_('Show image'), command=self._show_image)
        self._img_show_button.pack(side='left')
        self._img_select_button = ttk.Button(self._imageWindow, text=_('Select image'), command=self._select_image)
        self._img_select_button.pack(side='left')
        self._img_clear_button = ttk.Button(self._imageWindow, text=_('Clear image'), command=self._clear_image)
        self._img_clear_button.pack(side='left')

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_image_window()
        self._create_button_bar()

    def _clear_image(self):
        """Set the element's image to None."""
        if self._element.image is not None:
            self._element.image = None
            self._img_show_button.state(['disabled'])
            self._img_clear_button.state(['disabled'])
            self._ui.isModified = True

    def _select_image(self):
        """Select the element's image."""
        fileType = _('Image file')
        fileTypes = [(fileType, '.jpg'),
                     (fileType, '.jpeg'),
                     (fileType, '.png'),
                     (fileType, '.gif'),
                     (_('All files'), '.*')]
        selectedPath = filedialog.askopenfilename(filetypes=fileTypes)
        if selectedPath:
            __, imageFile = os.path.split(selectedPath)
            projectDir, __ = os.path.split(self._ui.prjFile.filePath)
            imagePath = f'{projectDir}/Images/{imageFile}'
            if not selectedPath == imagePath:
                try:
                    os.makedirs(f'{projectDir}/Images', exist_ok=True)
                    copyfile(selectedPath, imagePath)
                    self._ui.show_info(f"{_('Image for')} {self._element.title}: {norm_path(imagePath)}", title=_('Image copied'))
                except Exception as ex:
                    self._ui.show_error(str(ex), title=_('Cannot copy image'))
                    return
            self._element.image = imageFile
            self._img_show_button.state(['!disabled'])
            self._img_clear_button.state(['!disabled'])
            self._ui.isModified = True

    def _show_image(self):
        """Open the element#s image with the system image viewer."""
        if self._element.image:
            projectDir, __ = os.path.split(self._ui.prjFile.filePath)
            imagePath = f'{projectDir}/Images/{self._element.image}'
            if os.path.isfile(imagePath):
                open_document(imagePath)
            else:
                self._ui.show_error(f"{_('File not found')}: {norm_path(imagePath)}", title=_('Cannot show image'))
                self._clear_image()

