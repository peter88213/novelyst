"""Provide a class for yWriter 7 project editing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File


class Yw7WorkFile(Yw7File):
    """yWriter 7 project file representation.

    Public methods: 
        lock() -- create a non-yWriter lockfile.
        unlock() -- delete the non-yWriter lockfile, if any.
        has_lockfile() -- return True if a non-yWriter lockfile exists.
        has_changed_on_disk() -- return True if the yw project file has changed since last opened.
        write() -- write file if not locked, and get timestamp.
        read() -- read file and get timestamp.
        renumber_chapters() -- Modify chapter headings.
        
    Public properties:
        fileDate -- str: ISO formatted file date (read-only)
        
    This extends the superclass with a timestamp and a locking capability.
    """
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath -- str: path to the yw7 file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._timestamp = None

        # Configure part/chapter numbering
        self.renumberChapters = True
        self.renumberParts = True
        self.renumberWithinParts = False
        self.romanChapterNumbers = False
        self.romanPartNumbers = True
        self.chapterHeadingPrefix = 'Chapter '
        self.chapterHeadingSuffix = ''
        self.partHeadingPrefix = 'Part '
        self.partHeadingSuffix = ''

    @property
    def fileDate(self):
        if self._timestamp is not None:
            return datetime.fromtimestamp(self._timestamp).replace(microsecond=0).isoformat(sep=' ')
        else:
            return 'Never'

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail

    def lock(self):
        """Create a non-yWriter lockfile."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        if not os.path.isfile(lockfilePath):
            with open(lockfilePath, 'w') as f:
                f.write('')

    def unlock(self):
        """Delete the non-yWriter lockfile, if any."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        try:
            os.remove(lockfilePath)
        except:
            pass

    def has_lockfile(self):
        """Return True if a non-yWriter lockfile exists."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        return os.path.isfile(lockfilePath)

    def has_changed_on_disk(self):
        """Return True if the yw project file has changed since last opened."""
        try:
            if self._timestamp != os.path.getmtime(self.filePath):
                return True
            else:
                return False

        except:
            # this is for newly created projects
            return False

    def read(self):
        """Read file, get custom data and timestamp.
        
        Return a message beginning with the ERROR constant in case of error.
        Extends the superclass method.
        """
        message = super().read()
        if not message.startswith(ERROR):
            # Read custom fields.
            root = self.tree.getroot()
            prj = root.find('PROJECT')
            for prjFields in prj.findall('Fields'):
                something = prjFields.find('Field_SomethingCompletelyDifferent')
                if something is not None:
                    print(something.text)
            for chp in root.iter('CHAPTER'):
                chId = chp.find('ID').text
                for chFields in chp.findall('Fields'):
                    something = chFields.find('Field_SomethingCompletelyDifferent')
                    if something is not None:
                        print(something.text)
            for scn in root.iter('SCENE'):
                scId = scn.find('ID').text
                for scFields in scn.findall('Fields'):
                    something = scFields.find('Field_SomethingCompletelyDifferent')
                    if something is not None:
                        print(something.text)

        # Read the file timestamp.
        try:
            self._timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None
        return message

    def _build_element_tree(self):
        """Modify the yWriter project attributes of an existing xml element tree.

        Extends the superclass method.
        """
        super()._build_element_tree()
        root = self.tree.getroot()

        # Write project custom fields.
        xmlPrj = root.find('PROJECT')
        prjFields = xmlPrj.find('Fields')
        if prjFields is None:
            prjFields = ET.SubElement(xmlPrj, 'Fields')
        if self.firstNumberedChapter is not None:
            try:
                prjFields.find('Field_StartNovelChID').text = self.firstNumberedChapter
            except(AttributeError):
                ET.SubElement(prjFields, 'Field_StartNovelChID').text = self.firstNumberedChapter

        # Write chapter custom fields.
        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

        # Write scene custom fields.
        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

        try:
            self._timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None
        return

    def renumber_chapters(self):
        """Modify chapter headings."""
        ROMAN = [
            (1000, 'M'),
            (900, 'CM'),
            (500, 'D'),
            (400, 'CD'),
            (100, 'C'),
            (90, 'XC'),
            (50, 'L'),
            (40, 'XL'),
            (10, 'X'),
            (9, 'IX'),
            (5, 'V'),
            (4, 'IV'),
            (1, 'I'),
        ]

        def number_to_roman(n):
            """Return n as a Roman number.
            
            Credit goes to the user 'Aristide' on stack overflow.
            https://stackoverflow.com/a/47713392
            """
            result = []
            for (arabic, roman) in ROMAN:
                (factor, n) = divmod(n, arabic)
                result.append(roman * factor)
                if n == 0:
                    break

            return "".join(result)

        chapterCount = 0
        partCount = 0
        for chId in self.srtChapters:
            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].isTrash:
                continue

            if self.chapters[chId].chLevel == 0:
                # Regular chapter
                if not self.renumberChapters:
                    continue

            else:
                # Part (chapter "beginning a new section")
                if self.renumberWithinParts:
                    chapterCount = 0
                if not self.renumberParts:
                    continue

            if self.chapters[chId].chType == 0 or self.chapters[chId].oldType == 0:
                if self.chapters[chId].chLevel == 0:
                    chapterCount += 1
                    if self.romanChapterNumbers:
                        number = number_to_roman(chapterCount)
                    else:
                        number = str(chapterCount)
                    self.chapters[chId].title = f'{self.chapterHeadingPrefix}{number}{self.chapterHeadingSuffix}'
                else:
                    partCount += 1
                    if self.romanPartNumbers:
                        number = number_to_roman(partCount)
                    else:
                        number = str(partCount)
                    self.chapters[chId].title = f'{self.partHeadingPrefix}{number}{self.partHeadingSuffix}'
        return
