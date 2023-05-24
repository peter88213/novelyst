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

    def __init__(self, ui, title, geometry, sourceElements, targetElements, targetSrtElements):
        """Data import pick list.
        
        Positional arguments:
            ui -- the caller.
            title: str -- Window title.
            geometry: str -- Window geometry.
            sourceElements: dict -- characters, locations, or items of the data file.
            targetElements: dict -- characters, locations, or items of the project file.
            targetSrtElements: list -- Sorted charcter/location/item IDs of the project file.
        
        """
        super().__init__()
        self._ui = ui
        self.title(title)
        self.geometry(geometry)
        self.grab_set()
        self.focus()
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
        i = 0
        for  elemId in self._pickList.selection():
            newId = create_id(self._targetElements)
            self._targetElements[newId] = self._sourceElements[elemId]
            self._targetSrtElements.append(newId)
            i += 1
        if i > 0:
            self._ui.isModified = True
            self._ui.tv.refresh_tree()
            # this seems to be necessary;
            # otherwise the sorted elements list gets cleared
            self._ui.show_info(f'{i} {_("elements imported")}', title=_('XML data import'))
        self.destroy()

