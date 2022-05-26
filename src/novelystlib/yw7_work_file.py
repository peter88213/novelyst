"""Provide a class for yWriter 7 project editing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from datetime import datetime
from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File


class Yw7WorkFile(Yw7File):
    """yWriter 7 project file representation.

    Extends the superclass with a timestamp and a locking capability.
    """
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    # Configure part/chapter numbering
    _PRJ_KWVAR = (
        'Field_RenumberChapters',
        'Field_RenumberParts',
        'Field_RenumberWithinParts',
        'Field_RomanChapterNumbers',
        'Field_RomanPartNumbers',
        'Field_ChapterHeadingPrefix',
        'Field_ChapterHeadingSuffix',
        'Field_PartHeadingPrefix',
        'Field_PartHeadingSuffix',
        )
    _CHP_KWVAR = (
        'Field_NoNumber',
        )
    _SCN_KWVAR = (
        'Field_SceneArcs',
        )

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath -- str: path to the yw7 file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.timestamp = None

    @property
    def fileDate(self):
        if self.timestamp is not None:
            return datetime.fromtimestamp(self.timestamp).replace(microsecond=0).isoformat(sep=' ')
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
            if self.timestamp != os.path.getmtime(self.filePath):
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
        #--- Fix multiple characters/locations/items.
        srtCharacters = []
        for crId in self.srtCharacters:
            if not crId in srtCharacters:
                srtCharacters.append(crId)
        self.srtCharacters = srtCharacters
        srtLocations = []
        for lcId in self.srtLocations:
            if not lcId in srtLocations:
                srtLocations.append(lcId)
        self.srtLocations = srtLocations
        srtItems = []
        for itId in self.srtItems:
            if not itId in srtItems:
                srtItems.append(itId)
        self.srtItems = srtItems

        #--- Read the file timestamp.
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None
        return message

    def write(self):
        """Extend the superclass method."""
        message = super().write()
        if not message.startswith(ERROR):
            self.timestamp = os.path.getmtime(self.filePath)
        return message

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

        isModified = False
        chapterCount = 0
        partCount = 0
        for chId in self.srtChapters:
            if 'Field_NoNumber' in self.chapters[chId].kwVar:
                if self.chapters[chId].kwVar['Field_NoNumber']:
                    continue

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].isTrash:
                continue

            if self.chapters[chId].chLevel == 0:
                # Regular chapter
                if not self.kwVar['Field_RenumberChapters']:
                    continue

            else:
                # Part (chapter "beginning a new section")
                if self.kwVar['Field_RenumberWithinParts']:
                    chapterCount = 0
                if not self.kwVar['Field_RenumberParts']:
                    continue

            if self.chapters[chId].chType == 0 or self.chapters[chId].oldType == 0:
                headingPrefix = ''
                headingSuffix = ''
                if self.chapters[chId].chLevel == 0:
                    chapterCount += 1
                    if self.kwVar['Field_RomanChapterNumbers']:
                        number = number_to_roman(chapterCount)
                    else:
                        number = str(chapterCount)
                    if self.kwVar['Field_ChapterHeadingPrefix'] is not None:
                        headingPrefix = self.kwVar['Field_ChapterHeadingPrefix']
                    if self.kwVar['Field_ChapterHeadingSuffix'] is not None:
                        headingSuffix = self.kwVar['Field_ChapterHeadingSuffix']
                else:
                    partCount += 1
                    if self.kwVar['Field_RomanPartNumbers']:
                        number = number_to_roman(partCount)
                    else:
                        number = str(partCount)
                    if self.kwVar['Field_PartHeadingPrefix'] is not None:
                        headingPrefix = self.kwVar['Field_PartHeadingPrefix']
                    if self.kwVar['Field_PartHeadingSuffix'] is not None:
                        headingSuffix = self.kwVar['Field_PartHeadingSuffix']
                newTitle = f'{headingPrefix}{number}{headingSuffix}'
                if self.chapters[chId].title != newTitle:
                    self.chapters[chId].title = newTitle
                    isModified = True

        return isModified

