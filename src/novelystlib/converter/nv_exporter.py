"""Provide a converter class for novelyst export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pywriter.pywriter_globals import *
from pywriter.file.doc_open import open_document
from pywriter.converter.export_target_factory import ExportTargetFactory
from pywriter.odt_w.odt_w_proof import OdtWProof
from pywriter.odt_w.odt_w_manuscript import OdtWManuscript
from pywriter.odt_w.odt_w_scenedesc import OdtWSceneDesc
from pywriter.odt_w.odt_w_chapterdesc import OdtWChapterDesc
from pywriter.odt_w.odt_w_partdesc import OdtWPartDesc
from pywriter.odt_w.odt_w_brief_synopsis import OdtWBriefSynopsis
from pywriter.odt_w.odt_w_export import OdtWExport
from pywriter.odt_w.odt_w_items import OdtWItems
from pywriter.odt_w.odt_w_locations import OdtWLocations
from pywriter.odt_w.odt_w_xref import OdtWXref
from pywriter.odt_w.odt_w_notes import OdtWNotes
from pywriter.odt_w.odt_w_todo import OdtWTodo
from pywriter.ods_w.ods_w_charlist import OdsWCharList
from pywriter.ods_w.ods_w_loclist import OdsWLocList
from pywriter.ods_w.ods_w_itemlist import OdsWItemList
from pywriter.ods_w.ods_w_scenelist import OdsWSceneList
from pywriter.yw.data_files import DataFiles
from novelystlib.files.odt_characters_nv import OdtCharactersNv
from novelystlib.files.wrimo_file import WrimoFile
from novelystlib.files.odt_arcs import OdtArcs


class NvExporter:
    """A converter for universal export from a novelyst project.
    
    Public methods:
        run(source, suffix, lock=True, show=True) -- Create a target object and run conversion.    
    """
    EXPORT_TARGET_CLASSES = [OdtWProof,
                             OdtWManuscript,
                             OdtWBriefSynopsis,
                             OdtWSceneDesc,
                             OdtWChapterDesc,
                             OdtWPartDesc,
                             OdtWExport,
                             OdtArcs,
                             OdtCharactersNv,
                             OdtWItems,
                             OdtWLocations,
                             OdtWXref,
                             OdtWNotes,
                             OdtWTodo,
                             OdsWCharList,
                             OdsWLocList,
                             OdsWItemList,
                             OdsWSceneList,
                             DataFiles,
                             WrimoFile,
                             ]

    def __init__(self, ui):
        """Create strategy class instances.
        
        Positional arguments:
            ui -- User interface reference.
        
        Extends the superclass constructor.
        """
        DataFiles.SUFFIX = '_data'

        self.exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self.ui = ui
        self._source = None
        self._target = None
        self._lock = False
        self._show = False
        self._popup = None

    def run(self, source, suffix, lock=True, show=True):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- Yw7File instance.
            suffix -- str: Target file name suffix.
            lock -- boolean: Lock the project, if True.
            show -- boolean: After document creation, ask if open it with Office.
        """
        self._source = source
        self._lock = lock
        self._show = show
        self._popup = None
        self._isNewer = False
        kwargs = {'suffix':suffix}
        try:
            __, self._target = self.exportTargetFactory.make_file_objects(self._source.filePath, **kwargs)
        except Error as ex:
            self.ui.set_info_how(f'!{str(ex)}')
            return

        if os.path.isfile(self._target.filePath):
            self._ask()
        else:
            self._export()

    def _export(self):
        """Generate a new document. Overwrite the existing document, if any."""
        if self._popup is not None:
            self._popup.destroy()
        try:
            self._target.novel = self._source.novel
            self._target.write()
        except Error as ex:
            self.ui.set_info_how(f'!{str(ex)}')
        else:
            # Successfully created a new document.
            if self._lock and not self.ui.isLocked:
                self.ui.isLocked = True
            self._targetFileDate = datetime.now().replace(microsecond=0).isoformat(sep=' ')
            self.ui.set_info_how(_('Created {0} on {1}.').format(self._target.DESCRIPTION, self._targetFileDate))
            if self._show:
                if self.ui.ask_yes_no(_('Document "{}" created. Open now?').format(norm_path(self._target.filePath))):
                    open_document(self._target.filePath)

    def _open_existing(self):
        """Open the existing document instead of overwriting it."""
        if self._popup is not None:
            self._popup.destroy()
        open_document(self._target.filePath)
        if self._isNewer:
            prefix = ''
        else:
            prefix = '!'
            # warn the user, if a document is open that might be outdated
        self.ui.set_info_how(f'{prefix}{_("Opened existing {0} (last saved on {1})").format(self._target.DESCRIPTION, self._targetFileDate)}.')
        if self._lock and not self.ui.isLocked:
            self.ui.isLocked = True

    def _cancel(self):
        """Neither overwrite, nor open the existing document. Show a message instead."""
        if self._popup is not None:
            self._popup.destroy()
        self.ui.set_info_how(f'!{_("Action canceled by user")}.')

    def _ask(self):
        """Ask whether to overwrite or to open the existing document, and do what's necessary."""
        targetTimestamp = os.path.getmtime(self._target.filePath)
        try:
            if  targetTimestamp > self.ui.prjFile.timestamp:
                timeStatus = _('Newer than the project file')
                self._isNewer = True
            else:
                timeStatus = _('Older than the project file')
        except:
            timeStatus = ''
        self._targetFileDate = datetime.fromtimestamp(targetTimestamp).replace(microsecond=0).isoformat(sep=' ')
        message = _('{0} already exists.\n{1} (last saved on {2}).\nOpen this document instead of overwriting it?').format(
                    norm_path(self._target.DESCRIPTION), timeStatus, self._targetFileDate)
        offset = 300
        __, x, y = self.ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        self._popup = tk.Toplevel()
        self._popup.resizable(0, 0)
        self._popup.geometry(windowGeometry)
        self._popup.title(self.ui.novel.title)
        self._popup.grab_set()
        tk.Label(self._popup, text=message, bg='white').pack(ipadx=10, ipady=30)
        cancelButton = ttk.Button(self._popup, text=_('Cancel'), command=self._cancel)
        cancelButton.pack(side=tk.RIGHT, padx=5, pady=10)
        openButton = ttk.Button(self._popup, text=_('Open existing'), command=self._open_existing)
        openButton.pack(side=tk.RIGHT, padx=5, pady=10)
        overwriteButton = ttk.Button(self._popup, text=_('Overwrite'), command=self._export)
        overwriteButton.pack(side=tk.RIGHT, padx=5, pady=10)
        overwriteButton.focus_set()

