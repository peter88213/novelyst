"""Provide a converter class for yWriter export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from tkinter import messagebox
from datetime import datetime
from pywriter.pywriter_globals import ERROR
from pywriter.file.doc_open import open_document
from pywriter.converter.export_target_factory import ExportTargetFactory
from pywriter.odt.odt_proof import OdtProof
from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.odt.odt_chapterdesc import OdtChapterDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.odt.odt_brief_synopsis import OdtBriefSynopsis
from pywriter.odt.odt_export import OdtExport
from pywriter.odt.odt_characters import OdtCharacters
from pywriter.odt.odt_items import OdtItems
from pywriter.odt.odt_locations import OdtLocations
from pywriter.odt.odt_xref import OdtXref
from pywriter.odt.odt_notes import OdtNotes
from pywriter.ods.ods_charlist import OdsCharList
from pywriter.ods.ods_loclist import OdsLocList
from pywriter.ods.ods_itemlist import OdsItemList
from pywriter.ods.ods_scenelist import OdsSceneList


class NvExporter:
    """Base class for Novel file conversion."""
    EXPORT_TARGET_CLASSES = [OdtProof,
                             OdtManuscript,
                             OdtBriefSynopsis,
                             OdtSceneDesc,
                             OdtChapterDesc,
                             OdtPartDesc,
                             OdtExport,
                             OdtCharacters,
                             OdtItems,
                             OdtLocations,
                             OdtXref,
                             OdtNotes,
                             OdsCharList,
                             OdsLocList,
                             OdsItemList,
                             OdsSceneList,
                             ]

    def __init__(self, ui):
        """Create strategy class instances.
        
        Positional arguments:
            ui -- User interface reference.
        
        Extends the superclass constructor.
        """
        self.exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self.ui = ui
        self.newFile = None
        # Also indicates successful conversion.

    def run(self, source, suffix, lock=True):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- Yw7File instance.
            suffix -- str: Target file name suffix.
        """
        if lock and not self.ui.isLocked:
            self.ui.isLocked = True
        kwargs = {'suffix':suffix}
        message, __, target = self.exportTargetFactory.make_file_objects(source.filePath, **kwargs)
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        if os.path.isfile(target.filePath):
            targetFileDate = datetime.fromtimestamp(os.path.getmtime(target.filePath)).replace(microsecond=0).isoformat(sep=' ')
            options = {'default':'no'}
            doOpenExisting = messagebox.askyesnocancel(
                self.ui._title, f'File "{os.path.normpath(target.filePath)}" (last saved on {targetFileDate}) already exists.\n Open this file instead of overwriting it?', **options)
            if doOpenExisting is None:
                self.ui.set_info_how(f'{ERROR}Action canceled by user.')
                return

            elif doOpenExisting:
                open_document(target.filePath)
                self.ui.set_info_how(f'{ERROR}Opened existing {target.DESCRIPTION} (last saved on {targetFileDate}).')
                return

        message = target.merge(source)
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        message = target.write()
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
        else:
            targetFileDate = datetime.now().replace(microsecond=0).isoformat(sep=' ')
            self.ui.set_info_how(f'Created {target.DESCRIPTION} on {targetFileDate}.')
            if self.ui.ask_yes_no(f'{os.path.normpath(target.filePath)} created. Open now?'):
                open_document(target.filePath)

