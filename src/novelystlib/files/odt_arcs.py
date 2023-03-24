"""Provide a class for ODT invisibly tagged arc defining chapters export, and the filter classes needed.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template
from pywriter.pywriter_globals import *
from pywriter.odt_w.odt_w_todo import OdtWTodo


class OdtArcs(OdtWTodo):
    """ODT arc defining chapters file representation.

    Export a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = _('Arcs')
    SUFFIX = '_arcs'

    _todoPartTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    _todoChapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
<text:p text:style-name="Text_20_body">$Desc</text:p>
'''
    _todoSceneTemplate = '''<text:h text:style-name="Heading_20_3" text:outline-level="3">$Title</text:h>
<text:p text:style-name="Text_20_body">$Desc</text:p>
$SceneAssoc
<text:p text:style-name="Heading_20_4">―――</text:p>\n
<text:p text:style-name="Text_20_body">$SceneContent</text:p>
'''
    _todoChapterEndTemplate = ''

    _sceneLinkTemplate = '''
<text:p text:style-name="Text_20_body">$Scene: <text:span text:style-name="Emphasis">$SceneAssocTitle</text:span></text:p>    
<text:p text:style-name="Text_20_body">→ <text:a xlink:href="../${ProjectName}_scenes.odt#ScID:$ID%7Cregion">$Description</text:a></text:p>
<text:p text:style-name="Text_20_body">→ <text:a xlink:href="../${ProjectName}_manuscript.odt#ScID:$ID%7Cregion">$Manuscript</text:a></text:p>
'''

    def __init__(self, filePath, **kwargs):
        """Initialize filter strategy class instances.
        
        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        Extends the superclass constructor.
        """
        super().__init__(filePath, **kwargs)
        self._chapterFilter = ArcFilter()
        self._sceneFilter = PointFilter()

    def _get_chapters(self):
        """Process the chapters and nested scenes.
        
        Iterate through the sorted chapter list and apply the templates, 
        substituting placeholders according to the chapter mapping dictionary.
        For each chapter call the processing of its included scenes.
        Skip chapters not accepted by the chapter filter.
        Return a list of strings.
        
        Overrides the superclass method.
        """
        lines = []
        chapterNumber = 0
        sceneNumber = 0
        wordsTotal = 0
        lettersTotal = 0
        partHeading = None
        for chId in self.novel.srtChapters:
            dispNumber = 0
            doNotExport = False
            template = None
            if self.novel.chapters[chId].chType == 2:
                # Chapter is "Todo" type.
                if self.novel.chapters[chId].chLevel == 1:
                    # Chapter is "Todo Part" type.
                    partHeading = Template(self._todoPartTemplate).safe_substitute(self._get_chapterMapping(chId, dispNumber))
                elif not self._chapterFilter.accept(self, chId):
                    partHeading = None
                    continue

                elif self._todoChapterTemplate:
                    # Chapter is "Todo Chapter" type.
                    if partHeading:
                        lines.append(partHeading)
                        partHeading = None
                    template = Template(self._todoChapterTemplate)
                    chapterNumber += 1
                    dispNumber = chapterNumber

                if template is not None:
                    lines.append(template.safe_substitute(self._get_chapterMapping(chId, dispNumber)))

                    #--- Process scenes.
                    sceneLines, sceneNumber, wordsTotal, lettersTotal = self._get_scenes(
                        chId, sceneNumber, wordsTotal, lettersTotal, doNotExport)
                    lines.extend(sceneLines)

        return lines

    def _get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section.
        
        Positional arguments:
            scId: str -- scene ID.
            sceneNumber: int -- scene number to be displayed.
            wordsTotal: int -- accumulated wordcount.
            lettersTotal: int -- accumulated lettercount.
        
        Extends the superclass method.
        """
        sceneMapping = super()._get_sceneMapping(scId, sceneNumber, wordsTotal, lettersTotal)
        sceneAssocId = self.novel.scenes[scId].kwVar.get('Field_SceneAssoc', None)
        if sceneAssocId:
            sceneAssocMapping = dict(
                SceneAssocId=sceneAssocId,
                SceneAssocTitle=self.novel.scenes[sceneAssocId].title,
                ProjectName=sceneMapping['ProjectName'],
                Scene=_('Scene'),
                Description=_('Description'),
                Manuscript=_('Manuscript'),
                )
            template = Template(self._sceneLinkTemplate)
            sceneMapping['SceneAssoc'] = template.safe_substitute(sceneAssocMapping)
        else:
            sceneMapping['SceneAssoc'] = ''
        return sceneMapping


class ArcFilter:
    """Filter a chapter representing an arc.
    
    Public methods:
        accept(source, eId) -- check whether an entity matches the filter criteria.
    
    Strategy class, implementing filtering criteria for template-based export.
    """

    def accept(self, source, eId):
        """Check whether a chapter arc-defining.
        
        Positional arguments:
            source -- Novel instance holding the entity to check.
            eId -- ID of the entity to check.       
        
        Return True if the entity is not to be filtered out.
        """
        if source.novel.chapters[eId].kwVar.get('Field_ArcDefinition', None):
            return True

        else:
            return False


class PointFilter:
    """Filter a scene representing an arc point.
    
    Public methods:
        accept(source, eId) -- check whether an entity matches the filter criteria.
    
    Strategy class, implementing filtering criteria for template-based export.
    """

    def accept(self, source, eId):
        """Check whether a scene is arc point-defining.
        
        Positional arguments:
            source -- Novel instance holding the entity to check.
            eId -- ID of the entity to check.       
        
        Return True if the entity is not to be filtered out.
        """
        if source.novel.scenes[eId].scnArcs:
            return True

        else:
            return False
