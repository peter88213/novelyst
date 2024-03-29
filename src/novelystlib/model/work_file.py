"""Provide a class for the novelyst model file.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from datetime import datetime
from datetime import date
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.xml_indent import indent
from pywriter.model.id_generator import create_id
from pywriter.model.chapter import Chapter


class WorkFile(Yw7File):
    """novelyst project file representation.
    
    This is to be an adapter to the .yw7 project format.
    
    Public methods:
        adust_scene_types() -- Make sure that nodes with non-"Normal" parents inherit the type.
        check_arcs() -- Check and update all relationships relevant for arcs and arc points.
        count_words() -- Return a tuple of word count totals.
        get_counts() -- Return a tuple with total numbers
        get_status_counts() -- Return a list with word count totals depending of scene status.
        has_changed_on_disk() -- Return True if the yw project file has changed since last opened.
        has_lockfile() -- Return True if a project lockfile exists.
        lock() -- Create a project lockfile.
        read() -- Read file, get custom data, word count log, and timestamp.
        renumber_chapters() -- Modify chapter headings.
        unlock() -- Delete the project lockfile, if any.
        write() -- Update the word count log, write the file, and update the timestamp.

    Public instance variables:
        timestamp: float -- Time of last file modification (number of seconds since the epoch).
        wcLog: dict[str, list[str, str]] -- Daily word count logs.
        wcLogUpdate: dict[str, list[str, str]] -- Word counts missing in the log.
    
    Public properties:
        fileDate: str -- ISO-formatted file date/time (YYYY-MM-DD hh:mm:ss).

    Public class constants:
        PRJ_KWVAR -- List of the names of the project keyword variables.
        CHP_KWVAR -- List of the names of the chapter keyword variables.
        SCN_KWVAR -- List of the names of the scene keyword variables.

    Extends the superclass.
    """
    DESCRIPTION = _('novelyst project')
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    # Configure part/chapter numbering
    PRJ_KWVAR = [
        'Field_WorkPhase',
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
        ]
    CHP_KWVAR = [
        'Field_NoNumber',
        'Field_ArcDefinition',
        ]
    SCN_KWVAR = [
        'Field_SceneArcs',
        'Field_SceneAssoc',
        'Field_CustomAR',
        'Field_SceneStyle',  # This is for updating old projects.
        'Field_SceneMode',
        ]

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the project file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.timestamp = None
        self.wcLog = {}
        self.wcLogUpdate = {}

    @property
    def fileDate(self):
        if self.timestamp is not None:
            return datetime.fromtimestamp(self.timestamp).replace(microsecond=0).isoformat(sep=' ')
        else:
            return _('Never')

    def adjust_scene_types(self):
        """Make sure that nodes with non-"Normal" parents inherit the type.
        
        Return True if a type has been changed. Otherwise return False.
        Overrides the superclass method.
        """
        isModified = False
        partType = 0
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chLevel == 1:
                partType = self.novel.chapters[chId].chType
            elif partType != 0 and not self.novel.chapters[chId].isTrash:
                if self.novel.chapters[chId].chType != partType:
                    self.novel.chapters[chId].chType = partType
                    isModified = True
            if self.novel.chapters[chId].chType != 0:
                for scId in self.novel.chapters[chId].srtScenes:
                    if self.novel.scenes[scId].scType != self.novel.chapters[chId].chType:
                        self.novel.scenes[scId].scType = self.novel.chapters[chId].chType
                        isModified = True
        return isModified

    def check_arcs(self, addChapters=False):
        """Check and update all relationships relevant for arcs and arc points.
        
        Optional arguments:
            addChapters -- If True, create arc-defining "Todo" chapters for "orphaned" arcs,
                           if False, delete scene assignments to "orphaned" arcs.  
        
        Default operation:
        - Make sure that each arc is defined by a unique chapter.       
        - Make sure all children of an arc-defining "Todo" chapter have the same arc assigned.       
        - Make sure that not more than one scene is associated with an arc point.
        - Make sure that only "Normal" type scenes are associated with arc points.
        - Make sure that points are associated only with scenes that are associated with their arc.
        - Remove arc and point related associations from non-normal scenes in non-arc defining chapters.
        - Create backward references from normal scenes to the points.
        - Make sure that all arcs assigned to scenes are defined as "Todo" chapters.
               
        Return a list with the new chapter IDs, if any.
        """
        arcs = []
        scnPoints = {}
        for scId in self.novel.scenes:
            scnPoints[scId] = []

        # Identify arc defining chapters.
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chType == 2 and self.novel.chapters[chId].chLevel == 0:

                #--- Make sure that each arc is defined by a unique chapter.
                arc = self.novel.chapters[chId].kwVar.get('Field_ArcDefinition', None)
                if arc:
                    if arc in arcs:
                        # wrong assignment: Arc is already defined by another chapter
                        self.novel.chapters[chId].kwVar['Field_ArcDefinition'] = None
                        arc = None
                    else:
                        arcs.append(arc)

                    #--- Make sure all children of an arc-defining "Todo" chapter have the same arc assigned..
                    for ptId in self.novel.chapters[chId].srtScenes:
                        self.novel.scenes[ptId].scnArcs = arc

                        # Rebuild the point's scene association, omitting invalid ones.
                        scenes = string_to_list(self.novel.scenes[ptId].kwVar.get('Field_SceneAssoc', None))
                        self.novel.scenes[ptId].kwVar['Field_SceneAssoc'] = None
                        if scenes and arc:

                            #--- Make sure that not more than one scene is associated with an arc point.
                            scId = scenes[0]

                            #--- Make sure that only "Normal" type scenes are associated with arc points.
                            if scId in self.novel.scenes:
                                if self.novel.scenes[scId].scType == 0:

                                    #--- Make sure that points are associated only with scenes that are associated with their arc.
                                    if arc in string_to_list(self.novel.scenes[scId].scnArcs):
                                        self.novel.scenes[ptId].kwVar['Field_SceneAssoc'] = scId

                                        # Prepare a backward reference from the scene to the point.
                                        scnPoints[scId].append(ptId)

                                        #--- Make sure the arc point has the same date/time as the associated scene.
                                        self.novel.scenes[ptId].date = self.novel.scenes[scId].date
                                        self.novel.scenes[ptId].time = self.novel.scenes[scId].time
                                        self.novel.scenes[ptId].day = self.novel.scenes[scId].day
            else:
                for scId in self.novel.chapters[chId].srtScenes:
                    if self.novel.scenes[scId].scType != 0:
                        #--- Remove arc and point related associations from non-normal scenes in non-arc defining chapters.
                        self.novel.scenes[scId].kwVar['Field_SceneAssoc'] = None
                        self.novel.scenes[scId].scnArcs = None

        #--- Create backward references from normal scenes to the points.
        for scId in self.novel.scenes:
            if self.novel.scenes[scId].scType == 0:
                if scnPoints[scId]:
                    self.novel.scenes[scId].kwVar['Field_SceneAssoc'] = list_to_string(scnPoints[scId])
                else:
                    self.novel.scenes[scId].kwVar['Field_SceneAssoc'] = None

        #--- Make sure that all arcs assigned to scenes are defined as "Todo" chapters.
        # If addChapters is False, delete orphaned arc assignments.
        # If addChapters is True, create "Todo" chapters for orphaned arc assignments.
        newChapters = []
        partCreated = False
        for scId in self.novel.scenes:
            scnArcs = string_to_list(self.novel.scenes[scId].scnArcs)
            for scnArc in scnArcs:
                if not scnArc in arcs:
                    if addChapters:
                        if not partCreated:
                            # Create a "To do" part for the arc definitions.
                            chId = create_id(self.novel.chapters)
                            self.novel.chapters[chId] = Chapter()
                            self.novel.chapters[chId].title = _('Arcs')
                            self.novel.chapters[chId].chLevel = 1
                            self.novel.chapters[chId].chType = 2
                            self.novel.srtChapters.append(chId)
                            partCreated = True

                        # Create a "To do" chapter with an arc definition.
                        chId = create_id(self.novel.chapters)
                        self.novel.chapters[chId] = Chapter()
                        self.novel.chapters[chId].title = f'{scnArc} - {_("Narrative arc")}'
                        self.novel.chapters[chId].chLevel = 0
                        self.novel.chapters[chId].chType = 2
                        for fieldName in self.CHP_KWVAR:
                            self.novel.chapters[chId].kwVar[fieldName] = None
                        self.novel.chapters[chId].kwVar['Field_ArcDefinition'] = scnArc
                        self.novel.srtChapters.append(chId)
                        arcs.append(scnArc)
                        newChapters.append(chId)
                    else:
                        # Delete invalid arc assignment.
                        scnArcs.remove(scnArc)
                        self.novel.scenes[scId].scnArcs = list_to_string(scnArcs)
        return newChapters

    def count_words(self):
        """Return a tuple of word count totals.
        
        count: int -- Total words of "normal" type scenes.
        totalCount: int -- Total words of "normal" and "unused" scenes.
        """
        count = 0
        totalCount = 0
        for chId in self.novel.srtChapters:
            if not self.novel.chapters[chId].isTrash:
                for scId in self.novel.chapters[chId].srtScenes:
                    if self.novel.scenes[scId].scType in (0, 3) and not self.novel.scenes[scId].doNotExport:
                        totalCount += self.novel.scenes[scId].wordCount
                        if self.novel.scenes[scId].scType == 0:
                            count += self.novel.scenes[scId].wordCount
        return count, totalCount

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
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chType == 0:
                for scId in self.novel.chapters[chId].srtScenes:
                    if self.novel.scenes[scId].scType == 0 and not self.novel.scenes[scId].doNotExport:
                        sceneCount += 1
                        wordCount += self.novel.scenes[scId].wordCount
                if self.novel.chapters[chId].chLevel == 1:
                    partCount += 1
                else:
                    chapterCount += 1
        return wordCount, sceneCount, chapterCount, partCount

    def get_status_counts(self):
        """Return a list with word count totals depending of scene status.
        
        Position 0 -- None 
        Position 1 -- Total number of words in "outline" scenes 
        Position 2 -- Total number of words in "draft" scenes
        Position 3 -- Total number of words in "1st Edit" scenes
        Position 4 -- Total number of words in "2nd Edit" scenes
        Position 5 -- Total number of words in "Done" scenes
        """
        counts = [None, 0, 0, 0, 0, 0]
        for scId in self.novel.scenes:
            if self.novel.scenes[scId].scType == 0 and not self.novel.scenes[scId].doNotExport:
                if self.novel.scenes[scId].status is not None:
                    counts[self.novel.scenes[scId].status] += self.novel.scenes[scId].wordCount
        return counts

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

    def has_lockfile(self):
        """Return True if a project lockfile exists."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        return os.path.isfile(lockfilePath)

    def lock(self):
        """Create a project lockfile."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        if not os.path.isfile(lockfilePath):
            with open(lockfilePath, 'w') as f:
                f.write('')

    def read(self):
        """Read file, get custom data, word count log, and timestamp.
        
        Extends the superclass method.
        """
        super().read()

        #--- Read the file timestamp.
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None

        #--- Read the word count log.
        root = self.tree.getroot()
        xmlWclog = root.find('WCLog')
        if xmlWclog is not None:
            for xmlWc in xmlWclog.findall('WC'):
                wcDate = xmlWc.find('Date').text
                wcCount = xmlWc.find('Count').text
                wcTotalCount = xmlWc.find('TotalCount').text
                self.wcLog[wcDate] = [wcCount, wcTotalCount]

        #--- Keep the actual wordcount, if not logged.
        # Thus the words written with another word processor can be logged on writing.
        if self.wcLog:
            actualCountInt, actualTotalCountInt = self.count_words()
            actualCount = str(actualCountInt)
            actualTotalCount = str(actualTotalCountInt)
            latestDate = list(self.wcLog)[-1]
            latestCount = self.wcLog[latestDate][0]
            latestTotalCount = self.wcLog[latestDate][1]
            if actualCount != latestCount or actualTotalCount != latestTotalCount:
                try:
                    fileDate = date.fromtimestamp(self.timestamp).isoformat()
                except:
                    fileDate = date.today().isoformat()
                self.wcLogUpdate[fileDate] = [actualCount, actualTotalCount]

        #--- Convert field created with novelyst v4.3
        for chId in self.novel.chapters:
            oldField = self.novel.chapters[chId].kwVar.get('Field_Arc_Definition', None)
            if oldField:
                self.novel.chapters[chId].kwVar['Field_ArcDefinition'] = oldField
                self.novel.chapters[chId].kwVar['Field_Arc_Definition'] = None

        #--- Check arc definitions.
        self.check_arcs(addChapters=True)

        #--- Fix multiple characters/locations/items.
        srtCharacters = []
        for crId in self.novel.srtCharacters:
            if not crId in srtCharacters:
                srtCharacters.append(crId)
        self.novel.srtCharacters = srtCharacters
        srtLocations = []
        for lcId in self.novel.srtLocations:
            if not lcId in srtLocations:
                srtLocations.append(lcId)
        self.novel.srtLocations = srtLocations
        srtItems = []
        for itId in self.novel.srtItems:
            if not itId in srtItems:
                srtItems.append(itId)
        self.novel.srtItems = srtItems

        #--- Initialize empty scene character/location/item lists.
        # This helps deleting orphaned XML list items when saving the file.
        # Also fix missing scene status as a tribute to defensive programming.
        for scId in self.novel.scenes:
            if self.novel.scenes[scId].characters is None:
                self.novel.scenes[scId].characters = []
            if self.novel.scenes[scId].locations is None:
                self.novel.scenes[scId].locations = []
            if self.novel.scenes[scId].items is None:
                self.novel.scenes[scId].items = []
            if self.novel.scenes[scId].status is None:
                self.novel.scenes[scId].status = 1

        #--- If no reasonable looking locale is set, set the system locale.
        self.novel.check_locale()

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
        for chId in self.novel.srtChapters:
            if 'Field_NoNumber' in self.novel.chapters[chId].kwVar:
                if self.novel.chapters[chId].kwVar.get('Field_NoNumber', None):
                    continue

            if self.novel.chapters[chId].chType != 0:
                continue

            if self.novel.chapters[chId].chLevel == 0:
                # Regular chapter
                if not self.novel.kwVar.get('Field_RenumberChapters', None):
                    continue

            else:
                # Part (chapter "beginning a new section")
                if self.novel.kwVar.get('Field_RenumberWithinParts', None):
                    chapterCount = 0
                if not self.novel.kwVar.get('Field_RenumberParts', None):
                    continue

            headingPrefix = ''
            headingSuffix = ''
            if self.novel.chapters[chId].chLevel == 0:
                chapterCount += 1
                if self.novel.kwVar.get('Field_RomanChapterNumbers', None):
                    number = number_to_roman(chapterCount)
                else:
                    number = str(chapterCount)
                if self.novel.kwVar.get('Field_ChapterHeadingPrefix', None) is not None:
                    headingPrefix = self.novel.kwVar['Field_ChapterHeadingPrefix']
                if self.novel.kwVar.get('Field_ChapterHeadingSuffix', None) is not None:
                    headingSuffix = self.novel.kwVar['Field_ChapterHeadingSuffix']
            else:
                partCount += 1
                if self.novel.kwVar.get('Field_RomanPartNumbers', None):
                    number = number_to_roman(partCount)
                else:
                    number = str(partCount)
                if self.novel.kwVar.get('Field_PartHeadingPrefix', None) is not None:
                    headingPrefix = self.novel.kwVar['Field_PartHeadingPrefix']
                if self.novel.kwVar.get('Field_PartHeadingSuffix', None) is not None:
                    headingSuffix = self.novel.kwVar['Field_PartHeadingSuffix']
            newTitle = f'{headingPrefix}{number}{headingSuffix}'
            if self.novel.chapters[chId].title != newTitle:
                self.novel.chapters[chId].title = newTitle
                isModified = True

        return isModified

    def unlock(self):
        """Delete the project lockfile, if any."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        try:
            os.remove(lockfilePath)
        except:
            pass

    def write(self):
        """Update the word count log, write the file, and update the timestamp.
        
        Extends the superclass method.
        """
        if self.novel.kwVar.get('Field_SaveWordCount', False):
            # Add today's word count and word count on reading, if not logged.
            newCountInt, newTotalCountInt = self.count_words()
            newCount = str(newCountInt)
            newTotalCount = str(newTotalCountInt)
            today = date.today().isoformat()
            self.wcLogUpdate[today] = [newCount, newTotalCount]
            for wcDate in self.wcLogUpdate:
                self.wcLog[wcDate] = self.wcLogUpdate[wcDate]
        self.wcLogUpdate = {}

        super().write()
        self.timestamp = os.path.getmtime(self.filePath)

    def _build_element_tree(self):
        """Extends the superclass method."""
        super()._build_element_tree()

        #--- Rebuild the word count log.
        root = self.tree.getroot()
        xmlWcLog = root.find('WCLog')
        if xmlWcLog is not None:
            root.remove(xmlWcLog)
        if self.wcLog:
            xmlWcLog = ET.SubElement(root, 'WCLog')
            wcLastCount = None
            wcLastTotalCount = None
            for wc in self.wcLog:
                if self.novel.kwVar.get('Field_SaveWordCount', False):
                    # Discard entries with unchanged word count.
                    if self.wcLog[wc][0] == wcLastCount and self.wcLog[wc][1] == wcLastTotalCount:
                        continue

                    wcLastCount = self.wcLog[wc][0]
                    wcLastTotalCount = self.wcLog[wc][1]
                xmlWc = ET.SubElement(xmlWcLog, 'WC')
                ET.SubElement(xmlWc, 'Date').text = wc
                ET.SubElement(xmlWc, 'Count').text = self.wcLog[wc][0]
                ET.SubElement(xmlWc, 'TotalCount').text = self.wcLog[wc][1]

        #--- Prepare the XML tree for saving.
        indent(root)
        self.tree = ET.ElementTree(root)

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail

