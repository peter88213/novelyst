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

    def select(self, source):
        #--- Tree for selection.
        self.treeView = ttk.Treeview(self, selectmode='browse')
        scrollY = ttk.Scrollbar(self.treeView, orient=tk.VERTICAL, command=self.treeView.yview)
        self.treeView.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeView.pack(side=tk.LEFT)
        for elemId in source:
            yield(elemId)


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
                dataPicker = DataPicker()
                newCharacters = dataPicker.select(source.novel.characters)
                for crId in newCharacters:
                    newId = create_id(self.prjFile.novel.characters)
                    self.prjFile.novel.characters[newId] = source.novel.characters[crId]
                    self.prjFile.novel.srtCharacters.append(newId)
                    print(self.prjFile.novel.characters[newId].title)

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
                dataPicker = DataPicker()
                newLocations = dataPicker.select(source.novel.locations)
                for lcId in newLocations:
                    newId = create_id(self.prjFile.novel.locations)
                    self.prjFile.novel.locations[newId] = source.novel.locations[lcId]
                    self.prjFile.novel.srtLocations.append(newId)
                    print(self.prjFile.novel.locations[newId].title)

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
                dataPicker = DataPicker()
                newItems = dataPicker.select(source.novel.items)
                for itId in newItems:
                    newId = create_id(self.prjFile.novel.items)
                    self.prjFile.novel.items[newId] = source.novel.items[itId]
                    self.prjFile.novel.srtItems.append(newId)
                    print(self.prjFile.novel.items[newId].title)

    def save_project(self):
        self.prjFile.write()


testFile = Yw7File('output.yw7')
testFile.novel = Novel()
testFile.write()
app = DevelApp('Import data', root_geometry='600x400')
app.open_project(testFile.filePath)
app.start()

