"""Provide a class for program settings.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.drag_drop_listbox import DragDropListbox


class SettingsWindow(tk.Toplevel):

    COLORING_MODES = [_('none'), _('status'), _('style')]

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

        # Combobox for coloring mode setting.
        colorFrame = ttk.Frame(window)
        colorFrame.pack(fill=tk.BOTH, side=tk.LEFT)
        cm = self._ui.kwargs['coloring_mode']
        if not cm in self.COLORING_MODES:
            cm = self.COLORING_MODES[0]
        self._coloringMode = tk.StringVar(value=cm)
        self._coloringMode.trace('w', self._change_colors)
        ttk.Label(colorFrame,
                  text=_('Coloring mode')
                  ).pack(padx=5, pady=5, anchor=tk.W)
        ttk.Combobox(colorFrame,
                   textvariable=self._coloringMode,
                   values=self.COLORING_MODES,
                   width=20
                   ).pack(padx=5, pady=5, anchor=tk.W)

        # Listbox for column reordering.
        columnFrame = ttk.Frame(window)
        columnFrame.pack(fill=tk.BOTH, side=tk.LEFT)
        ttk.Label(columnFrame,
                  text=_('Columns')
                  ).pack(padx=5, pady=5, anchor=tk.W)
        self._coIdsByTitle = {}
        for coId, title, __ in self._tv.columns:
            self._coIdsByTitle[title] = coId
        self._colEntries = tk.Variable(value=list(self._coIdsByTitle))
        DragDropListbox(columnFrame,
                        listvariable=self._colEntries,
                        width=20
                        ).pack(padx=5, pady=5, anchor=tk.W)
        ttk.Button(columnFrame,
                   text=_('Apply'),
                   command=self._change_column_order
                   ).pack(padx=5, pady=5, anchor=tk.W)
        # "Exit" button.
        ttk.Button(self,
                   text=_('Exit'),
                   command=self.destroy
                   ).pack(padx=5, pady=5, anchor=tk.E)

    def _change_colors(self, *args, **kwargs):
        self._ui.kwargs['coloring_mode'] = self._coloringMode.get()
        self._tv.refresh_tree()

    def _change_column_order(self, *args, **kwargs):
        srtColumns = []
        titles = self._colEntries.get()
        for title in titles:
            srtColumns.append(self._coIdsByTitle[title])
        self._ui.kwargs['column_order'] = list_to_string(srtColumns)
        self._tv.configure_columns()
        self._tv.build_tree()

