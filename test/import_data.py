"""Read characters from an XML data file.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pywriter.pywriter_globals import *
from pywriter.ui.main_tk import MainTk
from pywriter.model.novel import Novel
from pywriter.yw.yw7_file import Yw7File
from pywriter.model.id_generator import create_id
from novelystlib.data_reader.character_data_reader import CharacterDataReader
from novelystlib.data_reader.location_data_reader import LocationDataReader
from novelystlib.data_reader.item_data_reader import ItemDataReader


class DataPicker(tk.Toplevel):

    def __init__(self, sourceElements, targetElements, targetSrtElements):
        """Tree for data selection.
        
        Positional arguments:
            sourceElements: dict -- characters, locations, or items of the data file.
            targetElements: dict -- characters, locations, or items of the project file.
            targetSrtElements: list -- Sorted charcter/location/item IDs of the project file.
        
        """
        super().__init__()
        self._sourceElements = sourceElements
        self._targetElements = targetElements
        self._targetSrtElements = targetSrtElements
        self.treeView = ttk.Treeview(self, selectmode='browse')
        scrollY = ttk.Scrollbar(self.treeView, orient=tk.VERTICAL, command=self.treeView.yview)
        self.treeView.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeView.pack(side=tk.LEFT)
        ttk.Button(self, text=_('Import selected'), command=self._import).pack()

    def _import(self):
        """Import the selected elements into the project."""
        for elemId in self._sourceElements:
            newId = create_id(self._targetElements)
            self._targetElements[newId] = self._sourceElements[elemId]
            self._targetSrtElements.append(newId)
            print(self._targetElements[newId].title)
        self.destroy()


class DevelApp(MainTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.characterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Characters'), menu=self.characterMenu)
        self.characterMenu.add_command(label=_('Import'), command=self._import_characters)
        self.locationMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Locations'), menu=self.locationMenu)
        self.locationMenu.add_command(label=_('Import'), command=self._import_locations)
        self.itemMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Items'), menu=self.itemMenu)
        self.itemMenu.add_command(label=_('Import'), command=self._import_items)
        self.fileMenu.add_command(label=_('Save'), command=self.save_project)

    def _import_characters(self):
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            source = CharacterDataReader(filePath)
            source.novel = Novel()
            try:
                source.read()
            except TypeError:
                pass
            else:
                DataPicker(source.novel.characters, self.prjFile.novel.characters, self.prjFile.novel.srtCharacters)

    def _import_locations(self):
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            source = LocationDataReader(filePath)
            source.novel = Novel()
            try:
                source.read()
            except TypeError:
                pass
            else:
                DataPicker(source.novel.locations, self.prjFile.novel.locations, self.prjFile.novel.srtLocations)

    def _import_items(self):
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            source = ItemDataReader(filePath)
            source.novel = Novel()
            try:
                source.read()
            except TypeError:
                pass
            else:
                DataPicker(source.novel.items, self.prjFile.novel.items, self.prjFile.novel.srtItems)

    def save_project(self):
        self.prjFile.write()


testFile = Yw7File('output.yw7')
testFile.novel = Novel()
testFile.write()
app = DevelApp('Import data', root_geometry='600x400')
app.open_project(testFile.filePath)
app.start()

