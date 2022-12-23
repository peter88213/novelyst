"""Provide a class for a plugin manager.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import messagebox
import webbrowser
from tkinter import ttk
from pywriter.pywriter_globals import *


class PluginManager(tk.Toplevel):

    def __init__(self, ui, size, **kw):
        self._ui = ui
        super().__init__(**kw)
        self.title(f'{_("Installed plugins")} - novelyst @release')
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill=tk.BOTH, expand=True)

        columns = 'Module', 'Version', 'novelyst API', 'Description'
        self._moduleCollection = ttk.Treeview(window, columns=columns, show='headings', selectmode='browse')
        self._moduleCollection.pack(fill=tk.BOTH, expand=True)
        self._moduleCollection.bind('<<TreeviewSelect>>', self._on_select_module)
        self._moduleCollection.tag_configure('rejected', foreground='red')
        self._moduleCollection.tag_configure('inactive', foreground='gray')

        self._moduleCollection.column('Module', width=150, minwidth=120, stretch=False)
        self._moduleCollection.heading('Module', text=_('Module'), anchor='w')
        self._moduleCollection.column('Version', width=100, minwidth=100, stretch=False)
        self._moduleCollection.heading('Version', text=_('Version'), anchor='w')
        self._moduleCollection.column('novelyst API', width=100, minwidth=100, stretch=False)
        self._moduleCollection.heading('novelyst API', text=_('novelyst API'), anchor='w')
        self._moduleCollection.column('Description', width=400, stretch=True)
        self._moduleCollection.heading('Description', text=_('Description'), anchor='w')

        for moduleName in self._ui.plugins:
            nodeTags = []
            try:
                version = self._ui.plugins[moduleName].VERSION
            except:
                version = _('unknown')
            try:
                description = self._ui.plugins[moduleName].DESCRIPTION
            except:
                description = _('No description')
            try:
                apiRequired = self._ui.plugins[moduleName].NOVELYST_API
            except:
                apiRequired = _('unknown')
            columns = [moduleName, version, apiRequired, description]
            if self._ui.plugins[moduleName].isRejected:
                nodeTags.append('rejected')
                # Mark rejected modules, represented by a dummy.
            elif not self._ui.plugins[moduleName].isActive:
                nodeTags.append('inactive')
                # Mark loaded yet incompatible modules.
            self._moduleCollection.insert('', 'end', moduleName, values=columns, tags=tuple(nodeTags))

        # "Home page" button.
        self._homeButton = ttk.Button(window, text=_('Home page'), command=self._open_home_page, state=tk.DISABLED)
        self._homeButton.pack(padx=5, pady=5, side=tk.LEFT)

        # "Delete" button.
        self._deleteButton = ttk.Button(window, text=_('Delete'), command=self._delete_module, state=tk.DISABLED)
        self._deleteButton.pack(padx=5, pady=5, side=tk.LEFT)

        # "Exit" button.
        ttk.Button(window, text=_('Exit'), command=self.destroy).pack(padx=5, pady=5, side=tk.LEFT)

    def _open_home_page(self, event=None):
        moduleName = self._moduleCollection.selection()[0]
        if moduleName:
            try:
                url = self._ui.plugins[moduleName].URL
                if url:
                    webbrowser.open(url)
            except:
                pass

    def _delete_module(self, event=None):
        moduleName = self._moduleCollection.selection()[0]
        if moduleName:
            if self._ui.plugins.delete_file(moduleName):
                self._deleteButton.configure(state=tk.DISABLED)
                if self._ui.plugins[moduleName].isActive:
                    messagebox.showinfo(f'{moduleName} {_("deleted")}', _('The plugin remains active until next start.'))
                else:
                    self._moduleCollection.delete(moduleName)

    def _on_select_module(self, event):
        moduleName = self._moduleCollection.selection()[0]
        homeButtonState = tk.DISABLED
        deleteButtonState = tk.DISABLED
        if moduleName:
            try:
                if self._ui.plugins[moduleName].URL:
                    homeButtonState = tk.NORMAL
            except:
                pass
            try:
                if self._ui.plugins[moduleName].filePath:
                    deleteButtonState = tk.NORMAL
            except:
                pass
        self._homeButton.configure(state=homeButtonState)
        self._deleteButton.configure(state=deleteButtonState)

