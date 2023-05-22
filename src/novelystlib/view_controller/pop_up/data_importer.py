"""Provide a class for a data import pick list.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from pywriter.model.id_generator import create_id


class DataImporter(tk.Toplevel):

    def __init__(self, ui, size, sourceElements, targetElements, targetSrtElements):
        """Data import pick list.
        
        Positional arguments:
            sourceElements: dict -- characters, locations, or items of the data file.
            targetElements: dict -- characters, locations, or items of the project file.
            targetSrtElements: list -- Sorted charcter/location/item IDs of the project file.
        
        """
        super().__init__()
        self.geometry(size)
        self._ui = ui
        self._sourceElements = sourceElements
        self._targetElements = targetElements
        self._targetSrtElements = targetSrtElements
        self._pickList = ttk.Treeview(self, selectmode='extended')
        scrollY = ttk.Scrollbar(self._pickList, orient=tk.VERTICAL, command=self._pickList.yview)
        self._pickList.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self._pickList.pack(fill=tk.BOTH, expand=True)
        ttk.Button(self, text=_('Import selected elements'), command=self._import).pack()
        for elemId in self._sourceElements:
            self._pickList.insert('', 'end', elemId, text=self._sourceElements[elemId].title)

    def _import(self):
        """Import the selected elements into the project."""
        for  elemId in self._pickList.selection():
            newId = create_id(self._targetElements)
            self._targetElements[newId] = self._sourceElements[elemId]
            self._targetSrtElements.append(newId)
            self._ui.isModified = True
        self.destroy()

