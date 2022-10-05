"""Provide a class for program settings.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.label_combo import LabelCombo


class SettingsWindow(tk.Toplevel):

    COLORING_MODES = [_('none'), _('status'), _('style')]

    def __init__(self, tv, ui, windowGeometry, **kw):
        self._tv = tv
        self._ui = ui
        super().__init__(**kw)
        self.title(_('Program settings'))
        self.geometry(windowGeometry)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill=tk.BOTH)

        # Combobox for coloring mode setting.
        cm = self._ui.kwargs['coloring_mode']
        if not cm in self.COLORING_MODES:
            cm = self.COLORING_MODES[0]
        self._coloringMode = tk.StringVar(value=cm)
        self._coloringMode.trace('w', self._change_colors)
        coloringModeCombobox = LabelCombo(window,
                              text=_('Coloring mode'),
                              textvariable=self._coloringMode,
                              values=self.COLORING_MODES,
                              lblWidth=20)
        coloringModeCombobox.pack(padx=5, pady=5)

        # "Exit" button.
        ttk.Button(window, text=_('Exit'), command=self.destroy).pack(padx=5, pady=5)

    def _change_colors(self, *args, **kwargs):
        self._ui.kwargs['coloring_mode'] = self._coloringMode.get()
        self._tv.refresh_tree()

