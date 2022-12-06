"""Provide a class for program settings.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.label_combo import LabelCombo
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
        window.pack(fill=tk.BOTH)

        # Combobox for coloring mode setting.
        colorFrame = ttk.Frame(window)
        colorFrame.pack(fill=tk.BOTH)
        cm = self._ui.kwargs['coloring_mode']
        if not cm in self.COLORING_MODES:
            cm = self.COLORING_MODES[0]
        self._coloringMode = tk.StringVar(value=cm)
        self._coloringMode.trace('w', self._change_colors)
        LabelCombo(colorFrame,
                   text=_('Coloring mode'),
                   textvariable=self._coloringMode,
                   values=self.COLORING_MODES,
                   lblWidth=20).pack(padx=5, pady=5)

        # Listbox for column reordering.
        columnFrame = ttk.Frame(window)
        columnFrame.pack(fill=tk.BOTH)
        ttk.Label(columnFrame, text=_('Columns')).pack(padx=5, pady=5, side=tk.LEFT, anchor=tk.N)
        srtColumns = list(self._tv.columns)
        self._colEntries = tk.StringVar(value=srtColumns)
        self._colEntries.trace('w', self._change_column_order)
        DragDropListbox(columnFrame,
                        listvariable=self._colEntries,
                        width=23).pack(padx=5, pady=5, side=tk.RIGHT)

        # "Exit" button.
        ttk.Button(window, text=_('Exit'), command=self.destroy).pack(padx=5, pady=5, side=tk.RIGHT)

    def _change_colors(self, *args, **kwargs):
        self._ui.kwargs['coloring_mode'] = self._coloringMode.get()
        self._tv.refresh_tree()

    def _change_column_order(self, *args, **kwargs):
        titles = self._colEntries.get()
        # self._tv.configure_columns()
        # self._tv.build_tree()

