"""Provide a class for novelyst project editing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from datetime import datetime
from datetime import date
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.xml_indent import indent


class Yw7WorkFile(Yw7File):
    """novelyst project file representation.
    
    Public methods:
        count_words() -- return a tuple of word count totals.

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
        'Field_CustomGoal',
        'Field_CustomConflict',
        'Field_CustomOutcome',
        'Field_CustomChrBio',
        'Field_CustomChrGoals',
        'Field_SaveWordCount',
        'Field_LanguageCode',
        'Field_CountryCode',
        )
    _CHP_KWVAR = (
        'Field_NoNumber',
        )
    _SCN_KWVAR = (
        'Field_SceneArcs',
        'Field_CustomAR',
        'Field_SceneStyle',
        )
    _CRT_KWVAR = (
        'Field_BirthDate',
        'Field_DeathDate',
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
        self.wordCountStart = 0
        self.wordTarget = 0
        self.check_locale()

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

        #--- Read word target data.
        if not message.startswith(ERROR):
            root = self.tree.getroot()
            prj = root.find('PROJECT')
            if prj.find('WordCountStart') is not None:
                try:
                    self.wordCountStart = int(prj.find('WordCountStart').text)
                except:
                    self.wordCountStart = 0
            if prj.find('WordTarget') is not None:
                try:
                    self.wordTarget = int(prj.find('WordTarget').text)
                except:
                    self.wordTarget = 0

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

        #--- Initialize empty scene character/location/item lists.
        # This helps deleting orphaned XML list items when saving the file.
        for scId in self.scenes:
            if self.scenes[scId].characters is None:
                self.scenes[scId].characters = []
            if self.scenes[scId].locations is None:
                self.scenes[scId].locations = []
            if self.scenes[scId].items is None:
                self.scenes[scId].items = []

        #--- Read the file timestamp.
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None

        #--- If no reasonable looking locale is set, set the system locale.
        self.check_locale()

        return message

    def _build_element_tree(self):
        """Extends the superclass method."""
        super()._build_element_tree()

        #--- Write word target data.
        root = self.tree.getroot()
        xmlPrj = root.find('PROJECT')
        try:
            xmlPrj.find('WordCountStart').text = str(self.wordCountStart)
        except(AttributeError):
            ET.SubElement(xmlPrj, 'WordCountStart').text = str(self.wordCountStart)
        try:
            xmlPrj.find('WordTarget').text = str(self.wordTarget)
        except(AttributeError):
            ET.SubElement(xmlPrj, 'WordTarget').text = str(self.wordTarget)

        #--- Process word count log.
        if self.kwVar.get('Field_SaveWordCount', ''):
            newCountInt, newTotalCountInt = self.count_words()
            newCount = str(newCountInt)
            newTotalCount = str(newTotalCountInt)
            today = date.today().isoformat()
            wcLog = root.find('WCLog')
            if wcLog is None:
                wcLog = ET.SubElement(root, 'WCLog')
                wc = ET.SubElement(wcLog, 'WC')
                ET.SubElement(wc, 'Date').text = today
                ET.SubElement(wc, 'Count').text = newCount
                ET.SubElement(wc, 'TotalCount').text = newTotalCount
            else:
                for wc in wcLog.findall('WC'):
                    editDate = wc.find('Date')
                    count = wc.find('Count')
                    totalCount = wc.find('TotalCount')
                if wc is None:
                    wc = ET.SubElement(wcLog, 'WC')
                    ET.SubElement(wc, 'Date').text = today
                    ET.SubElement(wc, 'Count').text = newCount
                    ET.SubElement(wc, 'TotalCount').text = newTotalCount
                elif newCount != count.text or newTotalCount != totalCount.text:
                    if editDate.text != today:
                        wc = ET.SubElement(wcLog, 'WC')
                        ET.SubElement(wc, 'Date').text = today
                        ET.SubElement(wc, 'Count').text = newCount
                        ET.SubElement(wc, 'TotalCount').text = newTotalCount
                    else:
                        count.text = newCount
                        totalCount.text = newTotalCount

        indent(root)
        self.tree = ET.ElementTree(root)

    def write(self):
        """Extends the superclass method."""
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
                if self.chapters[chId].kwVar.get('Field_NoNumber', None):
                    continue

            if self.chapters[chId].chType != 0:
                continue

            if self.chapters[chId].chLevel == 0:
                # Regular chapter
                if not self.kwVar.get('Field_RenumberChapters', None):
                    continue

            else:
                # Part (chapter "beginning a new section")
                if self.kwVar.get('Field_RenumberWithinParts', None):
                    chapterCount = 0
                if not self.kwVar.get('Field_RenumberParts', None):
                    continue

            headingPrefix = ''
            headingSuffix = ''
            if self.chapters[chId].chLevel == 0:
                chapterCount += 1
                if self.kwVar.get('Field_RomanChapterNumbers', None):
                    number = number_to_roman(chapterCount)
                else:
                    number = str(chapterCount)
                if self.kwVar.get('Field_ChapterHeadingPrefix', None) is not None:
                    headingPrefix = self.kwVar['Field_ChapterHeadingPrefix']
                if self.kwVar.get('Field_ChapterHeadingSuffix', None) is not None:
                    headingSuffix = self.kwVar['Field_ChapterHeadingSuffix']
            else:
                partCount += 1
                if self.kwVar.get('Field_RomanPartNumbers', None):
                    number = number_to_roman(partCount)
                else:
                    number = str(partCount)
                if self.kwVar.get('Field_PartHeadingPrefix', None) is not None:
                    headingPrefix = self.kwVar['Field_PartHeadingPrefix']
                if self.kwVar.get('Field_PartHeadingSuffix', None) is not None:
                    headingSuffix = self.kwVar['Field_PartHeadingSuffix']
            newTitle = f'{headingPrefix}{number}{headingSuffix}'
            if self.chapters[chId].title != newTitle:
                self.chapters[chId].title = newTitle
                isModified = True

        return isModified

    def get_counts(self):
        """Return a tuple with total numbers:
        
        Total number of words in "normal" scenes, 
        Total number of used "normal" scenes,
        Total number of used "normal" chapters,
        Total number of used "normal" parts.
        """
        partCount = 0
        chapterCount = 0
        sceneCount = 0
        wordCount = 0
        for chId in self.srtChapters:
            if self.chapters[chId].chType == 0:
                for scId in self.chapters[chId].srtScenes:
                    if self.scenes[scId].scType == 0:
                        sceneCount += 1
                        wordCount += self.scenes[scId].wordCount
                if self.chapters[chId].chLevel == 1:
                    partCount += 1
                else:
                    chapterCount += 1
        return wordCount, sceneCount, chapterCount, partCount

    def count_words(self):
        """Return a tuple of word count totals.
        
        count -- int: Total words of "normal" type scenes.
        totalCount -- int: Total words of "normal" and "unused" scenes.
        """
        count = 0
        totalCount = 0
        for chId in self.srtChapters:
            if not self.chapters[chId].isTrash:
                for scId in self.chapters[chId].srtScenes:
                    if self.scenes[scId].scType in (0, 3):
                        totalCount += self.scenes[scId].wordCount
                        if self.scenes[scId].scType == 0:
                            count += self.scenes[scId].wordCount
        return count, totalCount

    def adjust_scene_types(self):
        """Make sure that nodes with non-"Normal" parents inherit the type.
        
        Overrides the superclass method.
        """
        partType = 0
        for chId in self.srtChapters:
            if self.chapters[chId].chLevel == 1:
                partType = self.chapters[chId].chType
            elif partType != 0 and not self.chapters[chId].isTrash:
                self.chapters[chId].chType = partType
            if self.chapters[chId].chType != 0:
                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].scType = self.chapters[chId].chType

