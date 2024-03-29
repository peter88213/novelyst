"""Provide a converter class for report generation.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pywriter.pywriter_globals import *
from pywriter.file.doc_open import open_document
from pywriter.converter.export_target_factory import ExportTargetFactory
from novelystlib.export.nv_exporter import NvExporter
from novelystlib.export.html_project_notes import HtmlProjectNotes
from novelystlib.export.html_characters import HtmlCharacters
from novelystlib.export.html_locations import HtmlLocations
from novelystlib.export.html_items import HtmlItems
from novelystlib.export.html_plot_list import HtmlPlotList


class NvReporter(NvExporter):
    """Converter class for report generation.
    
    Public methods:
        run(source, suffix) -- Create a target object and run conversion.

    The HTML files are placed in a temporary directory 
    specified by the user interface's tempDir attribute, if any. 
    Otherwise, the project directory is used. 
    """
    EXPORT_TARGET_CLASSES = [HtmlProjectNotes,
                             HtmlCharacters,
                             HtmlLocations,
                             HtmlItems,
                             HtmlPlotList,
                             ]

    def __init__(self, ui):
        """Create strategy class instances.
        
        Positional arguments:
            ui: Ui -- Reference to the user interface (for messaging).
        
        Extends the superclass constructor.
        """
        self._exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self._ui = ui

    def run(self, source, suffix):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- Yw7File instance.
            suffix: str -- Target file name suffix.
        """
        kwargs = {'suffix':suffix}
        try:
            __, target = self._exportTargetFactory.make_file_objects(source.filePath, **kwargs)
        except Error as ex:
            self._ui.set_info_how(f'{str(ex)}')
        else:
            # Adjust HTML file path to the temp directory, if any
            # (the target factory sets the project directory; this is overridden here).
            dirname, filename = os.path.split(target.filePath)
            try:
                if self._ui.tempDir:
                    dirname = self._ui.tempDir
            except:
                if not dirname:
                    dirname = '.'
            target.filePath = f'{dirname}/{filename}'
            try:
                target.novel = source.novel
                target.write()
            except Error as ex:
                self._ui.set_info_how(f'!{str(ex)}')
            else:
                open_document(target.filePath)

