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
from pywriter.odt.odt_proof import OdtProof
from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.odt.odt_chapterdesc import OdtChapterDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.odt.odt_brief_synopsis import OdtBriefSynopsis
from pywriter.odt.odt_export import OdtExport
from pywriter.odt.odt_items import OdtItems
from pywriter.odt.odt_locations import OdtLocations
from pywriter.odt.odt_xref import OdtXref
from pywriter.odt.odt_notes import OdtNotes
from pywriter.odt.odt_todo import OdtTodo
from pywriter.ods.ods_charlist import OdsCharList
from pywriter.ods.ods_loclist import OdsLocList
from pywriter.ods.ods_itemlist import OdsItemList
from pywriter.ods.ods_scenelist import OdsSceneList
from pywriter.yw.data_files import DataFiles
from novelystlib.files.odt_characters_nv import OdtCharactersNv
from novelystlib.files.wrimo_file import WrimoFile


class NvExporter:
    """Base class for Novel file conversion."""
    EXPORT_TARGET_CLASSES = [OdtProof,
                             OdtManuscript,
                             OdtBriefSynopsis,
                             OdtSceneDesc,
                             OdtChapterDesc,
                             OdtPartDesc,
                             OdtExport,
                             OdtCharactersNv,
                             OdtItems,
                             OdtLocations,
                             OdtXref,
                             OdtNotes,
                             OdtTodo,
                             OdsCharList,
                             OdsLocList,
                             OdsItemList,
                             OdsSceneList,
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
        kwargs = {'suffix':suffix}
        message, __, self._target = self.exportTargetFactory.make_file_objects(self._source.filePath, **kwargs)
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        self._targetFileDate = datetime.now().replace(microsecond=0).isoformat(sep=' ')
        if os.path.isfile(self._target.filePath):
            self._ask()
        else:
            self._export()

    def _export(self):
        try:
            self._popup.destroy()
        except:
            pass
        message = self._target.merge(self._source)
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        message = self._target.write()
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        # Successfully created a new document.
        if self._lock and not self.ui.isLocked:
            self.ui.isLocked = True
        self.ui.set_info_how(_('Created {0} on {1}.').format(self._target.DESCRIPTION, self._targetFileDate))
        if self._show:
            if self.ui.ask_yes_no(_('Document "{}" created. Open now?').format(os.path.normpath(self._target.filePath))):
                open_document(self._target.filePath)

    def _open_existing(self):
        try:
            self._popup.destroy()
        except:
            pass
        open_document(self._target.filePath)
        self.ui.set_info_how(f'{ERROR}{_("Opened existing {0} (last saved on {1})").format(self._target.DESCRIPTION, self._targetFileDate)}.')
        if self._lock and not self.ui.isLocked:
            self.ui.isLocked = True

    def _cancel(self):
        try:
            self._popup.destroy()
        except:
            pass
        self.ui.set_info_how(f'{ERROR}{_("Action canceled by user")}.')

    def _ask(self):
        targetTimestamp = os.path.getmtime(self._target.filePath)
        try:
            if  targetTimestamp > self.ui.ywPrj.timestamp:
                timeStatus = _('Newer than the project file')
            else:
                timeStatus = _('Older than the project file')
        except:
            timeStatus = ''
        targetFileDate = datetime.fromtimestamp(targetTimestamp).replace(microsecond=0).isoformat(sep=' ')
        message = _('{0} already exists.\n{1} (last saved on {2}).\nOpen this document instead of overwriting it?').format(
                    os.path.normpath(self._target.DESCRIPTION), timeStatus, targetFileDate)
        offset = 300
        __, x, y = self.ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        self._popup = tk.Toplevel()
        self._popup.resizable(0, 0)
        self._popup.geometry(windowGeometry)
        self._popup.title(self.ui.ywPrj.title)
        self._popup.grab_set()
        tk.Label(self._popup, text=message, bg='white').pack(ipadx=10, ipady=30)
        cancelButton = ttk.Button(self._popup, text=_('Cancel'), command=self._cancel)
        cancelButton.pack(side=tk.RIGHT, padx=5, pady=10)
        openButton = ttk.Button(self._popup, text=_('Open existing'), command=self._open_existing)
        openButton.pack(side=tk.RIGHT, padx=5, pady=10)
        overwriteButton = ttk.Button(self._popup, text=_('Overwrite'), command=self._export)
        overwriteButton.pack(side=tk.RIGHT, padx=5, pady=10)
        overwriteButton.focus_set()

