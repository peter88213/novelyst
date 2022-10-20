"""Provide a converter class for novelyst export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import messagebox
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
from novelystlib.files.html_project_notes import HtmlProjectNotes


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

    def run(self, source, suffix, lock=True, show=True):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- Yw7File instance.
            suffix -- str: Target file name suffix.
            lock -- boolean: Lock the project, if True.
            show -- boolean: After document creation, ask if open it with Office.
        """
        kwargs = {'suffix':suffix}
        message, __, target = self.exportTargetFactory.make_file_objects(source.filePath, **kwargs)
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        if lock and os.path.isfile(target.filePath):
            targetFileDate = datetime.fromtimestamp(os.path.getmtime(target.filePath)).replace(microsecond=0).isoformat(sep=' ')
            options = {'default':'no'}
            doOpenExisting = messagebox.askyesnocancel(
                self.ui.title, _('Document "{0}" (last saved on {1}) already exists.\nOpen this file instead of overwriting it?').format(os.path.normpath(target.filePath), targetFileDate), **options)
            if doOpenExisting is None:
                self.ui.set_info_how(f'{ERROR}{_("Action canceled by user")}.')
                return

            elif doOpenExisting:
                open_document(target.filePath)
                self.ui.set_info_how(f'{ERROR}{_("Opened existing {0} (last saved on {1})").format(target.DESCRIPTION, targetFileDate)}.')
                return

        message = target.merge(source)
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        message = target.write()
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        # Successfully created a new document.
        if lock and not self.ui.isLocked:
            self.ui.isLocked = True
        targetFileDate = datetime.now().replace(microsecond=0).isoformat(sep=' ')
        self.ui.set_info_how(_('Created {0} on {1}.').format(target.DESCRIPTION, targetFileDate))
        if show:
            if self.ui.ask_yes_no(_('Document "{}" created. Open now?').format(os.path.normpath(target.filePath))):
                open_document(target.filePath)

