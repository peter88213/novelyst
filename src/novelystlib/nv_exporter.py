"""Provide a converter class for yWriter export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import webbrowser
from pywriter.pywriter_globals import ERROR
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
from pywriter.ods.ods_charlist import OdsCharList
from pywriter.ods.ods_loclist import OdsLocList
from pywriter.ods.ods_itemlist import OdsItemList
from pywriter.ods.ods_scenelist import OdsSceneList


class NvExporter:
    """Base class for Novel file conversion.

    Public methods:
        convert(sourceFile, targetFile) -- Convert sourceFile into targetFile.
        export_from_yw(sourceFile, targetFile) -- Convert from yWriter project to other file format.
        run(sourcePath, **kwargs) -- create source and target objects and run conversion.
    
    Instance variables:
        ui -- User interface reference.
        newFile -- str: path to the target file in case of success.   

    Class constants:
        EXPORT_TARGET_CLASSES -- list of FileExport subclasses to which export is possible.

    All lists are empty and meant to be overridden by subclasses.

    Instance variables:
        exportTargetFactory -- ExportTargetFactory.
    """
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

    def run(self, source, suffix, **kwargs):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- Yw7File instance.
            suffix -- str: Target file name suffix.
        
        Delete the target object after file export.
        """
        if not self.ui.save_project():
            return

        message, __, target = self.exportTargetFactory.make_file_objects(source.filePath, **{'suffix':suffix})
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        self.newFile = None
        self.export_from_yw(source, target)
        if self.newFile:
            if self.ui.ask_yes_no(f'{os.path.normpath(self.newFile)} created. Open now?'):
                self._open_newFile()
        del target

    def export_from_yw(self, source, target):
        """Convert from yWriter project to other file format.

        Positional arguments:
            source -- YwFile subclass instance.
            target -- Any Novel subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """
        self.ui.set_info_what(
            f'Input: {source.DESCRIPTION} "{os.path.normpath(source.filePath)}"\nOutput: {target.DESCRIPTION} "{os.path.normpath(target.filePath)}"')
        message = self.convert(source, target)
        self.ui.set_info_how(message)
        if message.startswith(ERROR):
            self.newFile = None
        else:
            self.newFile = target.filePath

    def convert(self, source, target):
        """Convert source into target and return a message.

        Positional arguments:
            source, target -- Novel subclass instances.

        Operation:
        2. Make the target object merge the source object's instance variables.
        3. Make the target object write the target file.
        Return a message beginning with the ERROR constant in case of error.

        Error handling:
        - Ask for permission to overwrite target.
        - Pass the error messages of the called methods of source and target.
        - The success message comes from target.write(), if called.       
        """
        if os.path.isfile(target.filePath) and not self._confirm_overwrite(target.filePath):
            return f'{ERROR}Action canceled by user.'

        message = target.merge(source)
        if message.startswith(ERROR):
            return message

        return target.write()

    def _confirm_overwrite(self, filePath):
        """Return boolean permission to overwrite the target file.
        
        Positional arguments:
            fileName -- path to the target file.
        
        Overrides the superclass method.
        """
        return self.ui.ask_yes_no(f'Overwrite existing file "{os.path.normpath(filePath)}"?')

    def _open_newFile(self):
        """Open the converted file for editing."""
        webbrowser.open(f'{self.newFile}')

