"""Provide a class for program settings.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.drag_drop_listbox import DragDropListbox


class SettingsWindow(tk.Toplevel):

    def __init__(self, tv, ui, size, **kw):
        self._tv = tv
        self._ui = ui
        super().__init__(**kw)
        self.title(_('Program settings'))
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill=tk.BOTH,
                    padx=5,
                    pady=5
                    )
        frame1 = ttk.Frame(window)
        frame1.pack(fill=tk.BOTH, side=tk.LEFT)
        ttk.Separator(window, orient=tk.VERTICAL).pack(fill=tk.Y, padx=10, side=tk.LEFT)
        frame2 = ttk.Frame(window)
        frame2.pack(fill=tk.BOTH, side=tk.LEFT)

        # Combobox for coloring mode setting.
        self._coloringModeStr = tk.StringVar(value=self._ui.COLORING_MODES[self._ui.coloringMode])
        self._coloringModeStr.trace('w', self._change_colors)
        ttk.Label(frame1,
                  text=_('Coloring mode')
                  ).pack(padx=5, pady=5, anchor=tk.W)
        ttk.Combobox(frame1,
                   textvariable=self._coloringModeStr,
                   values=self._ui.COLORING_MODES,
                   width=20
                   ).pack(padx=5, pady=5, anchor=tk.W)

        ttk.Separator(frame1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Checkbox for deleting yWriter-only data on save.
        self._cleanUpYw = tk.BooleanVar(frame1, value=self._ui.cleanUpYw)
        ttk.Checkbutton(frame1, text=_('Delete yWriter-only data on save'), variable=self._cleanUpYw).pack(anchor=tk.W)
        self._cleanUpYw.trace('w', self._update_cleanup)

        # Listbox for column reordering.
        ttk.Label(frame2,
                  text=_('Columns')
                  ).pack(padx=5, pady=5, anchor=tk.W)
        self._coIdsByTitle = {}
        for coId, title, __ in self._tv.columns:
            self._coIdsByTitle[title] = coId
        self._colEntries = tk.Variable(value=list(self._coIdsByTitle))
        DragDropListbox(frame2,
                        listvariable=self._colEntries,
                        width=20
                        ).pack(padx=5, pady=5, anchor=tk.W)
        ttk.Button(frame2,
                   text=_('Apply'),
                   command=self._change_column_order
                   ).pack(padx=5, pady=5, anchor=tk.W)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # "Exit" button.
        ttk.Button(self,
                   text=_('Exit'),
                   command=self.destroy
                   ).pack(padx=5, pady=5, anchor=tk.E)

    def _change_colors(self, *args, **kwargs):
        cmStr = self._coloringModeStr.get()
        self._ui.coloringMode = self._ui.COLORING_MODES.index(cmStr)
        self._tv.refresh_tree()

    def _change_column_order(self, *args, **kwargs):
        srtColumns = []
        titles = self._colEntries.get()
        for title in titles:
            srtColumns.append(self._coIdsByTitle[title])
        self._ui.kwargs['column_order'] = list_to_string(srtColumns)
        self._tv.configure_columns()
        self._tv.build_tree()

    def _update_cleanup(self, *args, **kwargs):
        self._ui.cleanUpYw = self._cleanUpYw.get()
