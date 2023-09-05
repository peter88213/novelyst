"""Provide a class for csv relationship table representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv
from pywriter.pywriter_globals import *


class CsvPlotList:
    """csv relationship table representation.

    Public methods:
        write() -- Write instance variables to the file.

    Public instance variables:
        filePath: str -- path to the file (property with getter and setter). 

    Uses the conventions for Excel-generated CSV files.
    """
    DESCRIPTION = _('csv Plot list')
    EXTENSION = '.csv'
    SUFFIX = '_plotlist'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.  
            
        Extends the superclass constructor.          
        """
        self.novel = None
        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a supported type as specified by EXTENSION.

        self.filePath = filePath
        self._csvArcTrue = '▇'
        self._csvArcFalse = ''

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Setter for the filePath instance variable.
                
        - Format the path string according to Python's requirements. 
        - Accept only filenames with the right suffix and extension.
        """
        if self.SUFFIX is not None:
            suffix = self.SUFFIX
        else:
            suffix = ''
        if filePath.lower().endswith(f'{suffix}{self.EXTENSION}'.lower()):
            self._filePath = filePath

    def write(self):
        """Write the relations to the file.
        
        Raise the "Error" exception in case of error. 
        This is a stub to be overridden by subclass methods.
        """
        try:
            with open(self.filePath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, dialect='excel')

                # Get arcs.
                arcs = []
                scnArcs = {}
                for chId in self.novel.srtChapters:
                    for scId in self.novel.chapters[chId].srtScenes:
                        if self.novel.scenes[scId].scType == 0:
                            scnArcs[scId] = string_to_list(self.novel.scenes[scId].scnArcs)
                            for arc in scnArcs[scId]:
                                if not arc in arcs:
                                    arcs.append(arc)

                # Title row.
                row = []
                row.append('')
                for arc in arcs:
                    row.append(arc)
                writer.writerow(row)

                # Scene rows.
                for i, scId in enumerate(scnArcs):
                    row = []
                    row.append(self.novel.scenes[scId].title)
                    for arc in arcs:
                        if arc in scnArcs[scId]:
                            entry = self._csvArcTrue
                            # Use arc point titles instead of binary marker.
                            pointIds = string_to_list(self.novel.scenes[scId].kwVar.get('Field_SceneAssoc', None))
                            points = []
                            for ptId in pointIds:
                                if arc in self.novel.scenes[ptId].scnArcs:
                                    points.append(self.novel.scenes[ptId].title)
                            if points:
                                entry = list_to_string(points)
                            row.append(entry)
                        else:
                            row.append(self._csvArcFalse)
                    writer.writerow(row)
        except Error:
            raise Error(f'{_("Cannot write File")}: "{norm_path(self.filePath)}".')

        return (f'{_("File written")}: "{norm_path(self.filePath)}".')
