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
from pywriter.yw.xml_indent import indent


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
        
    Public instance variables:
        timestamp -- file timestamp
        
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
        self.timestamp = None

        # Configure part/chapter numbering
        self._prjOptions = (
            'Field_RenumberChapters',
            'Field_RenumberParts',
            'Field_RenumberWithinParts',
            'Field_RomanChapterNumbers',
            'Field_RomanPartNumbers',
            )
        self._prjSettings = (
            'Field_ChapterHeadingPrefix',
            'Field_ChapterHeadingSuffix',
            'Field_PartHeadingPrefix',
            'Field_PartHeadingSuffix',
            )
        self._chOptions = (
            'Field_NoNumber',
            )

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
        # Fix multiple characters/locations/items.
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
        if not message.startswith(ERROR):
            # Read custom fields.
            root = self.tree.getroot()
            prj = root.find('PROJECT')
            for prjFields in prj.findall('Fields'):
                for field in self._prjOptions:
                    try:
                        if prjFields.find(field).text == '1':
                            self.kwVar[field] = True
                        else:
                            self.kwVar[field] = False
                    except:
                        self.kwVar[field] = None

                for field in self._prjSettings:
                    try:
                        self.kwVar[field] = prjFields.find(field).text
                    except:
                        self.kwVar[field] = None
            for chp in root.iter('CHAPTER'):
                chId = chp.find('ID').text
                for field in self._chOptions:
                    self.chapters[chId].kwVar[field] = None
                for chFields in chp.findall('Fields'):
                    for field in self._chOptions:
                        option = chFields.find(field)
                        try:
                            if option.text == '1':
                                self.chapters[chId].kwVar[field] = True
                            else:
                                self.chapters[chId].kwVar[field] = False
                        except:
                            pass

        # Read the file timestamp.
        try:
            self.timestamp = os.path.getmtime(self.filePath)
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
        for field in self._prjOptions:
            if self.kwVar[field]:
                try:
                    prjFields.find(field).text = '1'
                except(AttributeError):
                    ET.SubElement(prjFields, field).text = '1'
            else:
                try:
                    prjFields.remove(prjFields.find(field))
                except:
                    pass
        for field in self._prjSettings:
            setting = self.kwVar[field]
            if setting:
                try:
                    prjFields.find(field).text = setting
                except(AttributeError):
                    ET.SubElement(prjFields, field).text = setting
            else:
                try:
                    prjFields.remove(prjFields.find(field))
                except:
                    pass

        # Write chapter custom fields.
        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            chFields = chp.find('Fields')
            for field in self._chOptions:
                if field in self.chapters[chId].kwVar and self.chapters[chId].kwVar[field]:
                    if chFields is None:
                        chFields = ET.SubElement(chp, field)
                    try:
                        chFields.find(field).text = '1'
                    except(AttributeError):
                        ET.SubElement(chFields, field).text = '1'
                elif chFields is not None:
                    try:
                        chFields.remove(chFields.find(field))
                    except:
                        pass
        indent(root)
        self.tree = ET.ElementTree(root)

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
