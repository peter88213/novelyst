#!/usr/bin/env python3
"""yWriter file viewer. 

Version @release

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pathlib import Path

from configparser import ConfigParser


class Configuration():
    """Read/write the program configuration.

        INI file sections:
        <self.sLabel> - Strings
        <self.oLabel> - Boolean values

    Instance variables:    
        settings - dictionary of strings
        options - dictionary of boolean values
    """

    def __init__(self, settings={}, options={}):
        """Define attribute variables.

        Arguments:
        settings - default settings (dictionary of strings)
        options - default options (dictionary of boolean values)
        """
        self.sLabel = 'SETTINGS'
        self.oLabel = 'OPTIONS'
        self.set(settings, options)

    def set(self, settings=None, options=None):
        """Set the entire configuration without writing the INI file.
        """

        if settings is not None:
            self.settings = settings.copy()

        if options is not None:
            self.options = options.copy()

    def read(self, iniFile):
        """Read a configuration file.
        Settings and options that can not be read in, remain unchanged.
        """
        config = ConfigParser()
        config.read(iniFile)

        if config.has_section(self.sLabel):

            section = config[self.sLabel]

            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)

        if config.has_section(self.oLabel):

            section = config[self.oLabel]

            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.getboolean(option, fallback)

    def write(self, iniFile):
        """Save the configuration to iniFile.
        """
        config = ConfigParser()

        if self.settings != {}:

            config.add_section(self.sLabel)

            for settingId in self.settings:
                config.set(self.sLabel, settingId, str(self.settings[settingId]))

        if self.options != {}:

            config.add_section(self.oLabel)

            for settingId in self.options:

                if self.options[settingId]:
                    config.set(self.oLabel, settingId, 'Yes')

                else:
                    config.set(self.oLabel, settingId, 'No')

        with open(iniFile, 'w') as f:
            config.write(f)
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk


ERROR = '!'
#!/usr/bin/env python3
from tkinter import filedialog
from tkinter import messagebox




class Ui():
    """Base class for UI facades, implementing a 'silent mode'.
    """

    def __init__(self, title):
        """Initialize text buffers for messaging.
        """
        self.infoWhatText = ''
        self.infoHowText = ''

    def ask_yes_no(self, text):
        """The application may use a subclass  
        for confirmation requests.    
        """
        return True

    def set_info_what(self, message):
        """What's the converter going to do?"""
        self.infoWhatText = message

    def set_info_how(self, message):
        """How's the converter doing?"""

        if message.startswith(ERROR):
            message = f'FAIL: {message.split(ERROR, maxsplit=1)[1].strip()}'
            sys.stderr.write(message)

        self.infoHowText = message

    def start(self):
        """To be overridden by subclasses requiring
        special action to launch the user interaction.
        """


class MainTk(Ui):
    """A tkinter GUI root class.
    Main menu, title bar, main window frame, status bar, path bar.
    """

    def __init__(self, title, **kwargs):
        """Initialize the project related instance variables
        and configure the user interface.
        - Create a main menu to be extended by subclasses.
        - Create a title bar for the project title.
        - Open a main window frame to be used by subclasses.
        - Create a status bar to be used by subclasses.
        - Create a path bar for the project file path.
        """
        super().__init__(title)
        self.statusText = ''
        self.kwargs = kwargs
        self.ywPrj = None

        self.root = tk.Tk()
        self.root.title(title)
        self.mainMenu = tk.Menu(self.root)
        self.fileMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Project...', command=lambda: self.open_project(''))
        self.fileMenu.add_command(label='Close Project', command=lambda: self.close_project())
        self.fileMenu.entryconfig('Close Project', state='disabled')
        self.fileMenu.add_command(label='Exit', command=self.root.quit)
        self.extend_menu()
        # Hook for subclasses
        self.root.config(menu=self.mainMenu)
        self.titleBar = tk.Label(self.root, text='', padx=5, pady=2)
        self.titleBar.pack(expand=False, anchor='w')
        self.mainWindow = tk.Frame()
        self.mainWindow.pack(expand=True, fill='both')
        self.statusBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=2)
        self.statusBar.pack(expand=False, fill='both')
        self.pathBar = tk.Label(self.root, text='', padx=5, pady=3)
        self.pathBar.pack(expand=False, anchor='w')

    def extend_menu(self):
        """Create an object that represents the project file.
        This is a template method that can be overridden by subclasses. 
        """

    def disable_menu(self):
        """Disable menu entries when no project is open.
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig('Close Project', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig('Close Project', state='normal')

    def start(self):
        """Start the user interface.
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def open_project(self, fileName, fileTypes=[('yWriter 7 project', '.yw7')]):
        """Select a valid project file and display the path.

        Priority:
        1. use file name argument
        2. open file select dialog

        Return the file name.
        To be extended by subclasses.
        """
        self.set_status(self.statusText)
        initDir = os.path.dirname(self.kwargs['yw_last_open'])

        if not initDir:
            initDir = './'

        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(filetypes=fileTypes, defaultextension='.yw7', initialdir=initDir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.pathBar.config(text=os.path.normpath(fileName))

        return fileName

    def close_project(self):
        """Close the yWriter project without saving.
        Reset the user interface.
        To be extended by subclasses.
        """
        self.ywPrj = None
        self.titleBar.config(text='')
        self.set_status('')
        self.pathBar.config(text='')
        self.disable_menu()

    def ask_yes_no(self, text):
        """Display a message box with "yes/no" options.
        Return True or False depending on user input.
        """
        return messagebox.askyesno('WARNING', text)

    def set_info_how(self, message):
        """How's the application doing?
        Put a message on the status bar.
        """

        if message.startswith(ERROR):
            self.statusBar.config(bg='red')
            self.statusBar.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()

        else:
            self.statusBar.config(bg='green')
            self.statusBar.config(fg='white')
            self.infoHowText = message

        self.statusBar.config(text=self.infoHowText)

    def set_status(self, message):
        """Put text on the status bar."""
        self.statusText = message
        self.statusBar.config(bg=self.root.cget('background'))
        self.statusBar.config(fg='black')
        self.statusBar.config(text=message)
import xml.etree.ElementTree as ET

from urllib.parse import quote
from shutil import copy2


class Novel():
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).

    Public methods: 
        convert_to_yw(text) -- Return text, converted from source format to yw7 markup.
        convert_from_yw(text) -- Return text, converted from yw7 markup to target format.

    Instance variables:
        title -- str; title
        desc -- str; description
        author -- str; author name
        fieldTitle1 -- str; field title 1
        fieldTitle2 -- str; field title 2
        fieldTitle3 -- str; field title 3
        fieldTitle4 -- str; field title 4
        chapters -- dict; key = chapter ID, value = Chapter instance.
        scenes -- dict; key = scene ID, value = Scene instance.
        srtChapters -- list of str; The novel's sorted chapter IDs. 
        locations -- dict; key = location ID, value = WorldElement instance.
        srtLocations -- list of str; The novel's sorted location IDs. 
        items -- dict; key = item ID, value = WorldElement instance.
        srtItems -- list of str; The novel's sorted item IDs. 
        characters -- dict; key = character ID, value = Character instance.
        srtCharacters -- list of str The novel's sorted character IDs.
        filePath -- str; path to the file represented by the class.   
    """

    DESCRIPTION = 'Novel'
    EXTENSION = None
    SUFFIX = None
    # To be extended by subclass methods.

    def __init__(self, filePath, **kwargs):
        """Define instance variables.

        Positional argument:
            filePath -- string; path to the file represented by the class.
        """
        self.title = None
        # str
        # xml: <PROJECT><Title>

        self.desc = None
        # str
        # xml: <PROJECT><Desc>

        self.author = None
        # str
        # xml: <PROJECT><AuthorName>

        self.fieldTitle1 = None
        # str
        # xml: <PROJECT><FieldTitle1>

        self.fieldTitle2 = None
        # str
        # xml: <PROJECT><FieldTitle2>

        self.fieldTitle3 = None
        # str
        # xml: <PROJECT><FieldTitle3>

        self.fieldTitle4 = None
        # str
        # xml: <PROJECT><FieldTitle4>

        self.chapters = {}
        # dict
        # xml: <CHAPTERS><CHAPTER><ID>
        # key = chapter ID, value = Chapter instance.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # dict
        # xml: <SCENES><SCENE><ID>
        # key = scene ID, value = Scene instance.
        # The order of the elements does not matter (the novel's
        # order of the scenes is defined by the order of the chapters
        # and the order of the scenes within the chapters)

        self.srtChapters = []
        # list of str
        # The novel's chapter IDs. The order of its elements
        # corresponds to the novel's order of the chapters.

        self.locations = {}
        # dict
        # xml: <LOCATIONS>
        # key = location ID, value = WorldElement instance.
        # The order of the elements does not matter.

        self.srtLocations = []
        # list of str
        # The novel's location IDs. The order of its elements
        # corresponds to the XML project file.

        self.items = {}
        # dict
        # xml: <ITEMS>
        # key = item ID, value = WorldElement instance.
        # The order of the elements does not matter.

        self.srtItems = []
        # list of str
        # The novel's item IDs. The order of its elements
        # corresponds to the XML project file.

        self.characters = {}
        # dict
        # xml: <CHARACTERS>
        # key = character ID, value = Character instance.
        # The order of the elements does not matter.

        self.srtCharacters = []
        # list of str
        # The novel's character IDs. The order of its elements
        # corresponds to the XML project file.

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a
        # supported type as specified by EXTENSION.

        self._projectName = None
        # str
        # URL-coded file name without suffix and extension.

        self._projectPath = None
        # str
        # URL-coded path to the project directory.

        self.filePath = filePath

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
            head, tail = os.path.split(os.path.realpath(filePath))
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(f'{suffix}{self.EXTENSION}', ''))

    def convert_to_yw(self, text):
        """Return text, converted from source format to yw7 markup.
        This is a stub to be overridden by subclass methods.
        """
        return text

    def convert_from_yw(self, text):
        """Return text, converted from yw7 markup to target format.
        This is a stub to be overridden by subclass methods.
        """
        return text


class Chapter():
    """yWriter chapter representation.
    # xml: <CHAPTERS><CHAPTER>
    """

    chapterTitlePrefix = "Chapter "
    # str
    # Can be changed at runtime for non-English projects.

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self.chLevel = None
        # int
        # xml: <SectionStart>
        # 0 = chapter level
        # 1 = section level ("this chapter begins a section")

        self.oldType = None
        # int
        # xml: <Type>
        # 0 = chapter type (marked "Chapter")
        # 1 = other type (marked "Other")

        self.chType = None
        # int
        # xml: <ChapterType>
        # 0 = Normal
        # 1 = Notes
        # 2 = Todo

        self.isUnused = None
        # bool
        # xml: <Unused> -1

        self.suppressChapterTitle = None
        # bool
        # xml: <Fields><Field_SuppressChapterTitle> 1
        # True: Chapter heading not to be displayed in written document.
        # False: Chapter heading to be displayed in written document.

        self.isTrash = None
        # bool
        # xml: <Fields><Field_IsTrash> 1
        # True: This chapter is the yw7 project's "trash bin".
        # False: This chapter is not a "trash bin".

        self.suppressChapterBreak = None
        # bool
        # xml: <Fields><Field_SuppressChapterBreak> 0

        self.srtScenes = []
        # list of str
        # xml: <Scenes><ScID>
        # The chapter's scene IDs. The order of its elements
        # corresponds to the chapter's order of the scenes.

    def get_title(self):
        """Fix auto-chapter titles if necessary 
        """
        text = self.title

        if text:
            text = text.replace('Chapter ', self.chapterTitlePrefix)

        return text
import re


class Scene():
    """yWriter scene representation.
    # xml: <SCENES><SCENE>
    """

    # Emulate an enumeration for the scene status
    # Since the items are used to replace text,
    # they may contain spaces. This is why Enum cannot be used here.

    STATUS = [None, 'Outline', 'Draft', '1st Edit', '2nd Edit', 'Done']
    ACTION_MARKER = 'A'
    REACTION_MARKER = 'R'

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self._sceneContent = None
        # str
        # xml: <SceneContent>
        # Scene text with yW7 raw markup.

        self.rtfFile = None
        # str
        # xml: <RTFFile>
        # Name of the file containing the scene in yWriter 5.

        self.wordCount = 0
        # int # xml: <WordCount>
        # To be updated by the sceneContent setter

        self.letterCount = 0
        # int
        # xml: <LetterCount>
        # To be updated by the sceneContent setter

        self.isUnused = None
        # bool
        # xml: <Unused> -1

        self.isNotesScene = None
        # bool
        # xml: <Fields><Field_SceneType> 1

        self.isTodoScene = None
        # bool
        # xml: <Fields><Field_SceneType> 2

        self.doNotExport = None
        # bool
        # xml: <ExportCondSpecific><ExportWhenRTF>

        self.status = None
        # int
        # xml: <Status>
        # 1 - Outline
        # 2 - Draft
        # 3 - 1st Edit
        # 4 - 2nd Edit
        # 5 - Done
        # See also the STATUS list for conversion.

        self.sceneNotes = None
        # str
        # xml: <Notes>

        self.tags = None
        # list of str
        # xml: <Tags>

        self.field1 = None
        # str
        # xml: <Field1>

        self.field2 = None
        # str
        # xml: <Field2>

        self.field3 = None
        # str
        # xml: <Field3>

        self.field4 = None
        # str
        # xml: <Field4>

        self.appendToPrev = None
        # bool
        # xml: <AppendToPrev> -1

        self.isReactionScene = None
        # bool
        # xml: <ReactionScene> -1

        self.isSubPlot = None
        # bool
        # xml: <SubPlot> -1

        self.goal = None
        # str
        # xml: <Goal>

        self.conflict = None
        # str
        # xml: <Conflict>

        self.outcome = None
        # str
        # xml: <Outcome>

        self.characters = None
        # list of str
        # xml: <Characters><CharID>

        self.locations = None
        # list of str
        # xml: <Locations><LocID>

        self.items = None
        # list of str
        # xml: <Items><ItemID>

        self.date = None
        # str
        # xml: <SpecificDateMode>-1
        # xml: <SpecificDateTime>1900-06-01 20:38:00

        self.time = None
        # str
        # xml: <SpecificDateMode>-1
        # xml: <SpecificDateTime>1900-06-01 20:38:00

        self.minute = None
        # str
        # xml: <Minute>

        self.hour = None
        # str
        # xml: <Hour>

        self.day = None
        # str
        # xml: <Day>

        self.lastsMinutes = None
        # str
        # xml: <LastsMinutes>

        self.lastsHours = None
        # str
        # xml: <LastsHours>

        self.lastsDays = None
        # str
        # xml: <LastsDays>

        self.image = None
        # str
        # xml: <ImageFile>

    @property
    def sceneContent(self):
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text):
        """Set sceneContent updating word count and letter count."""
        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yWriter raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yWriter raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)



class WorldElement():
    """Story world element representation.
    # xml: <LOCATIONS><LOCATION> or # xml: <ITEMS><ITEM>
    """

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.image = None
        # str
        # xml: <ImageFile>

        self.desc = None
        # str
        # xml: <Desc>

        self.tags = None
        # list of str
        # xml: <Tags>

        self.aka = None
        # str
        # xml: <AKA>


class Character(WorldElement):
    """yWriter character representation.
    # xml: <CHARACTERS><CHARACTER>
    """

    MAJOR_MARKER = 'Major'
    MINOR_MARKER = 'Minor'

    def __init__(self):
        super().__init__()

        self.notes = None
        # str
        # xml: <Notes>

        self.bio = None
        # str
        # xml: <Bio>

        self.goals = None
        # str
        # xml: <Goals>

        self.fullName = None
        # str
        # xml: <FullName>

        self.isMajor = None
        # bool
        # xml: <Major>


class Splitter():

    PART_SEPARATOR = '# '
    CHAPTER_SEPARATOR = '## '
    SCENE_SEPARATOR = '* * *'
    CLIP_TITLE = 20
    # This is used for splitting scenes.

    def split_scenes(self, ywPrj):
        """Generate new chapters and scenes if there are dividers within the scene content.
        """

        def create_chapter(chapterId, title, desc, level):
            """Create a new chapter and add it to the novel.
            """
            newChapter = Chapter()
            newChapter.title = title
            newChapter.desc = desc
            newChapter.chLevel = level
            newChapter.chType = 0
            ywPrj.chapters[chapterId] = newChapter

        def create_scene(sceneId, parent, splitCount):
            """Create a new scene and add it to the novel.
            """
            WARNING = ' (!) '

            newScene = Scene()

            if parent.title:

                if len(parent.title) > self.CLIP_TITLE:
                    title = f'{parent.title[:self.CLIP_TITLE]}...'

                else:
                    title = parent.title

                newScene.title = f'{title} Split: {splitCount}'

            else:
                newScene.title = f'New scene Split: {splitCount}'

            if parent.desc and not parent.desc.startswith(WARNING):
                parent.desc = f'{WARNING}{parent.desc}'

            if parent.goal and not parent.goal.startswith(WARNING):
                parent.goal = f'{WARNING}{parent.goal}'

            if parent.conflict and not parent.conflict.startswith(WARNING):
                parent.conflict = f'{WARNING}{parent.conflict}'

            if parent.outcome and not parent.outcome.startswith(WARNING):
                parent.outcome = f'{WARNING}{parent.outcome}'

            # Reset the parent's status to Draft, if not Outline.

            if parent.status > 2:
                parent.status = 2

            newScene.status = parent.status
            newScene.isNotesScene = parent.isNotesScene
            newScene.isUnused = parent.isUnused
            newScene.isTodoScene = parent.isTodoScene
            newScene.date = parent.date
            newScene.time = parent.time
            newScene.day = parent.day
            newScene.hour = parent.hour
            newScene.minute = parent.minute
            newScene.lastsDays = parent.lastsDays
            newScene.lastsHours = parent.lastsHours
            newScene.lastsMinutes = parent.lastsMinutes
            ywPrj.scenes[sceneId] = newScene

        # Get the maximum chapter ID and scene ID.

        chIdMax = 0
        scIdMax = 0

        for chId in ywPrj.srtChapters:

            if int(chId) > chIdMax:
                chIdMax = int(chId)

        for scId in ywPrj.scenes:

            if int(scId) > scIdMax:
                scIdMax = int(scId)

        srtChapters = []

        for chId in ywPrj.srtChapters:
            srtChapters.append(chId)
            chapterId = chId
            srtScenes = []

            for scId in ywPrj.chapters[chId].srtScenes:
                srtScenes.append(scId)

                if not ywPrj.scenes[scId].sceneContent:
                    continue

                sceneId = scId
                lines = ywPrj.scenes[scId].sceneContent.split('\n')
                newLines = []
                inScene = True
                sceneSplitCount = 0

                # Search scene content for dividers.

                for line in lines:

                    if line.startswith(self.PART_SEPARATOR):

                        if inScene:
                            ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)
                            newLines = []
                            sceneSplitCount = 0
                            inScene = False

                        ywPrj.chapters[chapterId].srtScenes = srtScenes
                        srtScenes = []

                        chIdMax += 1
                        chapterId = str(chIdMax)
                        create_chapter(chapterId, 'New part', line.replace(self.PART_SEPARATOR, ''), 1)
                        srtChapters.append(chapterId)

                    elif line.startswith(self.CHAPTER_SEPARATOR):

                        if inScene:
                            ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)
                            newLines = []
                            sceneSplitCount = 0
                            inScene = False

                        ywPrj.chapters[chapterId].srtScenes = srtScenes
                        srtScenes = []

                        chIdMax += 1
                        chapterId = str(chIdMax)
                        create_chapter(chapterId, 'New chapter', line.replace(self.CHAPTER_SEPARATOR, ''), 0)
                        srtChapters.append(chapterId)

                    elif line.startswith(self.SCENE_SEPARATOR):
                        ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)
                        newLines = []
                        sceneSplitCount += 1
                        scIdMax += 1
                        sceneId = str(scIdMax)
                        create_scene(sceneId, ywPrj.scenes[scId], sceneSplitCount)
                        srtScenes.append(sceneId)
                        inScene = True

                    elif not inScene:
                        newLines.append(line)
                        sceneSplitCount += 1
                        scIdMax += 1
                        sceneId = str(scIdMax)
                        create_scene(sceneId, ywPrj.scenes[scId], sceneSplitCount)
                        srtScenes.append(sceneId)
                        inScene = True

                    else:
                        newLines.append(line)

                ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)

            ywPrj.chapters[chapterId].srtScenes = srtScenes

        ywPrj.srtChapters = srtChapters


def indent(elem, level=0):
    """xml pretty printer

    Kudos to to Fredrik Lundh. 
    Source: http://effbot.org/zone/element-lib.htm#prettyprint
    """
    i = f'\n{level * "  "}'

    if len(elem):

        if not elem.text or not elem.text.strip():
            elem.text = f'{i}  '

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

        for elem in elem:
            indent(elem, level + 1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



class Yw7TreeWriter():
    """Write utf-8 encoded yWriter project file.

    Public methods: 
        write_element_tree(ywProject) -- Write back the xml element tree to a yw7 file.   
    """

    def write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with the ERROR constant in case of error.
        """

        if os.path.isfile(ywProject.filePath):
            os.replace(ywProject.filePath, f'{ywProject.filePath}.bak')
            backedUp = True

        else:
            backedUp = False

        try:
            ywProject.tree.write(ywProject.filePath, xml_declaration=False, encoding='utf-8')

        except:

            if backedUp:
                os.replace(f'{ywProject.filePath}.bak', ywProject.filePath)

            return f'{ERROR}Cannot write "{os.path.normpath(ywProject.filePath)}".'

        return 'yWriter XML tree written.'
from html import unescape



class Yw7Postprocessor():
    """Postprocess utf-8 encoded yWriter project.
    Insert the missing CDATA tags, replace xml entities by plain text.

    Public methods:
        postprocess_xml_file(filePath) -- Postprocess the xml files created by ElementTree.        
    """

    _CDATA_TAGS = ['Title', 'AuthorName', 'Bio', 'Desc',
                   'FieldTitle1', 'FieldTitle2', 'FieldTitle3',
                   'FieldTitle4', 'LaTeXHeaderFile', 'Tags',
                   'AKA', 'ImageFile', 'FullName', 'Goals',
                   'Notes', 'RTFFile', 'SceneContent',
                   'Outcome', 'Goal', 'Conflict']
    # Names of xml elements containing CDATA.
    # ElementTree.write omits CDATA tags, so they have to be inserted afterwards.

    def _format_xml(self, text):
        '''Postprocess the xml file created by ElementTree:
           Insert the missing CDATA tags, replace xml entities by plain text.
        '''
        lines = text.split('\n')
        newlines = []

        for line in lines:

            for tag in self._CDATA_TAGS:
                line = re.sub(f'\<{tag}\>', f'<{tag}><![CDATA[', line)
                line = re.sub(f'\<\/{tag}\>', f']]></{tag}>', line)

            newlines.append(line)

        text = '\n'.join(newlines)
        text = text.replace('[CDATA[ \n', '[CDATA[')
        text = text.replace('\n]]', ']]')
        text = unescape(text)

        return text

    def postprocess_xml_file(self, filePath):
        '''Postprocess the xml file created by ElementTree:
        Put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with the ERROR constant in case of error.
        '''

        with open(filePath, 'r', encoding='utf-8') as f:
            text = f.read()

        text = self._format_xml(text)
        text = f'<?xml version="1.0" encoding="utf-8"?>\n{text}'

        try:

            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return f'{ERROR}Can not write "{os.path.normpath(filePath)}".'

        return f'"{os.path.normpath(filePath)}" written.'


class Yw7File(Novel):
    """yWriter 7 project file representation.

    Public methods: 
        read() -- Parse the file and store selected properties.
        merge(novel) -- Copy required attributes of the novel object.
        write() -- Write selected properties to the file.
        is_locked() -- Check whether the yw7 file is locked by yWriter.

    Additional attributes:
        ywTreeWriter -- strategy class to write yWriter project files.
        ywPostprocessor -- strategy class to postprocess yWriter project files.
        tree -- xml element tree of the yWriter project
    """

    DESCRIPTION = 'yWriter 7 project'
    EXTENSION = '.yw7'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables:
        Extend the superclass constructor by adding.
        """
        super().__init__(filePath)

        self.ywTreeWriter = Yw7TreeWriter()
        self.ywPostprocessor = Yw7Postprocessor()
        self.tree = None

    def _strip_spaces(self, lines):
        """Local helper method.

        Positional argument:
            lines -- list of strings

        Return lines with leading and trailing spaces removed.
        """
        stripped = []

        for line in lines:
            stripped.append(line.strip())

        return stripped

    def read(self):
        """Parse the yWriter xml file, fetching the Novel attributes.
        Return a message beginning with the ERROR constant in case of error.
        Override the superclass method.
        """

        if self.is_locked():
            return f'{ERROR}yWriter seems to be open. Please close first.'

        try:
            self.tree = ET.parse(self.filePath)

        except:
            return f'{ERROR}Can not process "{os.path.normpath(self.filePath)}".'

        root = self.tree.getroot()

        #--- Read locations from the xml element tree.

        for loc in root.iter('LOCATION'):
            lcId = loc.find('ID').text
            self.srtLocations.append(lcId)
            self.locations[lcId] = WorldElement()

            if loc.find('Title') is not None:
                self.locations[lcId].title = loc.find('Title').text

            if loc.find('ImageFile') is not None:
                self.locations[lcId].image = loc.find('ImageFile').text

            if loc.find('Desc') is not None:
                self.locations[lcId].desc = loc.find('Desc').text

            if loc.find('AKA') is not None:
                self.locations[lcId].aka = loc.find('AKA').text

            if loc.find('Tags') is not None:

                if loc.find('Tags').text is not None:
                    tags = loc.find('Tags').text.split(';')
                    self.locations[lcId].tags = self._strip_spaces(tags)

        #--- Read items from the xml element tree.

        for itm in root.iter('ITEM'):
            itId = itm.find('ID').text
            self.srtItems.append(itId)
            self.items[itId] = WorldElement()

            if itm.find('Title') is not None:
                self.items[itId].title = itm.find('Title').text

            if itm.find('ImageFile') is not None:
                self.items[itId].image = itm.find('ImageFile').text

            if itm.find('Desc') is not None:
                self.items[itId].desc = itm.find('Desc').text

            if itm.find('AKA') is not None:
                self.items[itId].aka = itm.find('AKA').text

            if itm.find('Tags') is not None:

                if itm.find('Tags').text is not None:
                    tags = itm.find('Tags').text.split(';')
                    self.items[itId].tags = self._strip_spaces(tags)

        #--- Read characters from the xml element tree.

        for crt in root.iter('CHARACTER'):
            crId = crt.find('ID').text
            self.srtCharacters.append(crId)
            self.characters[crId] = Character()

            if crt.find('Title') is not None:
                self.characters[crId].title = crt.find('Title').text

            if crt.find('ImageFile') is not None:
                self.characters[crId].image = crt.find('ImageFile').text

            if crt.find('Desc') is not None:
                self.characters[crId].desc = crt.find('Desc').text

            if crt.find('AKA') is not None:
                self.characters[crId].aka = crt.find('AKA').text

            if crt.find('Tags') is not None:

                if crt.find('Tags').text is not None:
                    tags = crt.find('Tags').text.split(';')
                    self.characters[crId].tags = self._strip_spaces(tags)

            if crt.find('Notes') is not None:
                self.characters[crId].notes = crt.find('Notes').text

            if crt.find('Bio') is not None:
                self.characters[crId].bio = crt.find('Bio').text

            if crt.find('Goals') is not None:
                self.characters[crId].goals = crt.find('Goals').text

            if crt.find('FullName') is not None:
                self.characters[crId].fullName = crt.find('FullName').text

            if crt.find('Major') is not None:
                self.characters[crId].isMajor = True

            else:
                self.characters[crId].isMajor = False

        #--- Read attributes at novel level from the xml element tree.

        prj = root.find('PROJECT')

        if prj.find('Title') is not None:
            self.title = prj.find('Title').text

        if prj.find('AuthorName') is not None:
            self.author = prj.find('AuthorName').text

        if prj.find('Desc') is not None:
            self.desc = prj.find('Desc').text

        if prj.find('FieldTitle1') is not None:
            self.fieldTitle1 = prj.find('FieldTitle1').text

        if prj.find('FieldTitle2') is not None:
            self.fieldTitle2 = prj.find('FieldTitle2').text

        if prj.find('FieldTitle3') is not None:
            self.fieldTitle3 = prj.find('FieldTitle3').text

        if prj.find('FieldTitle4') is not None:
            self.fieldTitle4 = prj.find('FieldTitle4').text

        #--- Read attributes at chapter level from the xml element tree.

        self.srtChapters = []
        # This is necessary for re-reading.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.srtChapters.append(chId)

            if chp.find('Title') is not None:
                self.chapters[chId].title = chp.find('Title').text

            if chp.find('Desc') is not None:
                self.chapters[chId].desc = chp.find('Desc').text

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            else:
                self.chapters[chId].chLevel = 0

            if chp.find('Type') is not None:
                self.chapters[chId].oldType = int(chp.find('Type').text)

            if chp.find('ChapterType') is not None:
                self.chapters[chId].chType = int(chp.find('ChapterType').text)

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            else:
                self.chapters[chId].isUnused = False

            self.chapters[chId].suppressChapterTitle = False

            if self.chapters[chId].title is not None:

                if self.chapters[chId].title.startswith('@'):
                    self.chapters[chId].suppressChapterTitle = True

            for chFields in chp.findall('Fields'):

                if chFields.find('Field_SuppressChapterTitle') is not None:

                    if chFields.find('Field_SuppressChapterTitle').text == '1':
                        self.chapters[chId].suppressChapterTitle = True

                if chFields.find('Field_IsTrash') is not None:

                    if chFields.find('Field_IsTrash').text == '1':
                        self.chapters[chId].isTrash = True

                    else:
                        self.chapters[chId].isTrash = False

                if chFields.find('Field_SuppressChapterBreak') is not None:

                    if chFields.find('Field_SuppressChapterBreak').text == '1':
                        self.chapters[chId].suppressChapterBreak = True

                    else:
                        self.chapters[chId].suppressChapterBreak = False

                else:
                    self.chapters[chId].suppressChapterBreak = False

            self.chapters[chId].srtScenes = []

            if chp.find('Scenes') is not None:

                if not self.chapters[chId].isTrash:

                    for scn in chp.find('Scenes').findall('ScID'):
                        scId = scn.text
                        self.chapters[chId].srtScenes.append(scId)

        #--- Read attributes at scene level from the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text
            self.scenes[scId] = Scene()

            if scn.find('Title') is not None:
                self.scenes[scId].title = scn.find('Title').text

            if scn.find('Desc') is not None:
                self.scenes[scId].desc = scn.find('Desc').text

            if scn.find('RTFFile') is not None:
                self.scenes[scId].rtfFile = scn.find('RTFFile').text

            # This is relevant for yW5 files with no SceneContent:

            if scn.find('WordCount') is not None:
                self.scenes[scId].wordCount = int(
                    scn.find('WordCount').text)

            if scn.find('LetterCount') is not None:
                self.scenes[scId].letterCount = int(
                    scn.find('LetterCount').text)

            if scn.find('SceneContent') is not None:
                sceneContent = scn.find('SceneContent').text

                if sceneContent is not None:
                    self.scenes[scId].sceneContent = sceneContent

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            else:
                self.scenes[scId].isUnused = False

            self.scenes[scId].isNotesScene = False
            self.scenes[scId].isTodoScene = False

            for scFields in scn.findall('Fields'):

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '1':
                        self.scenes[scId].isNotesScene = True

                    if scFields.find('Field_SceneType').text == '2':
                        self.scenes[scId].isTodoScene = True

            if scn.find('ExportCondSpecific') is None:
                self.scenes[scId].doNotExport = False

            elif scn.find('ExportWhenRTF') is not None:
                self.scenes[scId].doNotExport = False

            else:
                self.scenes[scId].doNotExport = True

            if scn.find('Status') is not None:
                self.scenes[scId].status = int(scn.find('Status').text)

            if scn.find('Notes') is not None:
                self.scenes[scId].sceneNotes = scn.find('Notes').text

            if scn.find('Tags') is not None:

                if scn.find('Tags').text is not None:
                    tags = scn.find('Tags').text.split(';')
                    self.scenes[scId].tags = self._strip_spaces(tags)

            if scn.find('Field1') is not None:
                self.scenes[scId].field1 = scn.find('Field1').text

            if scn.find('Field2') is not None:
                self.scenes[scId].field2 = scn.find('Field2').text

            if scn.find('Field3') is not None:
                self.scenes[scId].field3 = scn.find('Field3').text

            if scn.find('Field4') is not None:
                self.scenes[scId].field4 = scn.find('Field4').text

            if scn.find('AppendToPrev') is not None:
                self.scenes[scId].appendToPrev = True

            else:
                self.scenes[scId].appendToPrev = False

            if scn.find('SpecificDateTime') is not None:
                dateTime = scn.find('SpecificDateTime').text.split(' ')

                for dt in dateTime:

                    if '-' in dt:
                        self.scenes[scId].date = dt

                    elif ':' in dt:
                        self.scenes[scId].time = dt

            else:
                if scn.find('Day') is not None:
                    self.scenes[scId].day = scn.find('Day').text

                if scn.find('Hour') is not None:
                    self.scenes[scId].hour = scn.find('Hour').text

                if scn.find('Minute') is not None:
                    self.scenes[scId].minute = scn.find('Minute').text

            if scn.find('LastsDays') is not None:
                self.scenes[scId].lastsDays = scn.find('LastsDays').text

            if scn.find('LastsHours') is not None:
                self.scenes[scId].lastsHours = scn.find('LastsHours').text

            if scn.find('LastsMinutes') is not None:
                self.scenes[scId].lastsMinutes = scn.find('LastsMinutes').text

            if scn.find('ReactionScene') is not None:
                self.scenes[scId].isReactionScene = True

            else:
                self.scenes[scId].isReactionScene = False

            if scn.find('SubPlot') is not None:
                self.scenes[scId].isSubPlot = True

            else:
                self.scenes[scId].isSubPlot = False

            if scn.find('Goal') is not None:
                self.scenes[scId].goal = scn.find('Goal').text

            if scn.find('Conflict') is not None:
                self.scenes[scId].conflict = scn.find('Conflict').text

            if scn.find('Outcome') is not None:
                self.scenes[scId].outcome = scn.find('Outcome').text

            if scn.find('ImageFile') is not None:
                self.scenes[scId].image = scn.find('ImageFile').text

            if scn.find('Characters') is not None:
                for crId in scn.find('Characters').iter('CharID'):

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    self.scenes[scId].characters.append(crId.text)

            if scn.find('Locations') is not None:
                for lcId in scn.find('Locations').iter('LocID'):

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    self.scenes[scId].locations.append(lcId.text)

            if scn.find('Items') is not None:
                for itId in scn.find('Items').iter('ItemID'):

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    self.scenes[scId].items.append(itId.text)

        # Make sure that ToDo, Notes, and Unused type is inherited from the
        # chapter.

        for chId in self.chapters:

            if self.chapters[chId].chType == 2:
                # Chapter is "ToDo" type.

                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].isTodoScene = True
                    self.scenes[scId].isUnused = True

            elif self.chapters[chId].chType == 1:
                # Chapter is "Notes" type.

                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].isNotesScene = True
                    self.scenes[scId].isUnused = True

            elif self.chapters[chId].isUnused:

                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].isUnused = True

        return 'yWriter project data read in.'

    def merge(self, source):
        """Copy required attributes of the source object.
        Return a message beginning with the ERROR constant in case of error.
        Override the superclass method.
        """

        def merge_lists(srcLst, tgtLst):
            """Insert srcLst items to tgtLst, if missing.
            """
            j = 0

            for i in range(len(srcLst)):

                if not srcLst[i] in tgtLst:
                    tgtLst.insert(j, srcLst[i])
                    j += 1

                else:
                    j = tgtLst.index(srcLst[i]) + 1

        if os.path.isfile(self.filePath):
            message = self.read()
            # initialize data

            if message.startswith(ERROR):
                return message

        #--- Merge and re-order locations.

        if source.srtLocations != []:
            self.srtLocations = source.srtLocations
            temploc = self.locations
            self.locations = {}

            for lcId in source.srtLocations:

                # Build a new self.locations dictionary sorted like the
                # source

                self.locations[lcId] = WorldElement()

                if not lcId in temploc:
                    # A new location has been added
                    temploc[lcId] = WorldElement()

                if source.locations[lcId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.locations[lcId].title = source.locations[lcId].title

                else:
                    self.locations[lcId].title = temploc[lcId].title

                if source.locations[lcId].image is not None:
                    self.locations[lcId].image = source.locations[lcId].image

                else:
                    self.locations[lcId].desc = temploc[lcId].desc

                if source.locations[lcId].desc is not None:
                    self.locations[lcId].desc = source.locations[lcId].desc

                else:
                    self.locations[lcId].desc = temploc[lcId].desc

                if source.locations[lcId].aka is not None:
                    self.locations[lcId].aka = source.locations[lcId].aka

                else:
                    self.locations[lcId].aka = temploc[lcId].aka

                if source.locations[lcId].tags is not None:
                    self.locations[lcId].tags = source.locations[lcId].tags

                else:
                    self.locations[lcId].tags = temploc[lcId].tags

        #--- Merge and re-order items.

        if source.srtItems != []:
            self.srtItems = source.srtItems
            tempitm = self.items
            self.items = {}

            for itId in source.srtItems:

                # Build a new self.items dictionary sorted like the
                # source

                self.items[itId] = WorldElement()

                if not itId in tempitm:
                    # A new item has been added
                    tempitm[itId] = WorldElement()

                if source.items[itId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.items[itId].title = source.items[itId].title

                else:
                    self.items[itId].title = tempitm[itId].title

                if source.items[itId].image is not None:
                    self.items[itId].image = source.items[itId].image

                else:
                    self.items[itId].image = tempitm[itId].image

                if source.items[itId].desc is not None:
                    self.items[itId].desc = source.items[itId].desc

                else:
                    self.items[itId].desc = tempitm[itId].desc

                if source.items[itId].aka is not None:
                    self.items[itId].aka = source.items[itId].aka

                else:
                    self.items[itId].aka = tempitm[itId].aka

                if source.items[itId].tags is not None:
                    self.items[itId].tags = source.items[itId].tags

                else:
                    self.items[itId].tags = tempitm[itId].tags

        #--- Merge and re-order characters.

        if source.srtCharacters != []:
            self.srtCharacters = source.srtCharacters
            tempchr = self.characters
            self.characters = {}

            for crId in source.srtCharacters:

                # Build a new self.characters dictionary sorted like the
                # source

                self.characters[crId] = Character()

                if not crId in tempchr:
                    # A new character has been added
                    tempchr[crId] = Character()

                if source.characters[crId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.characters[crId].title = source.characters[crId].title

                else:
                    self.characters[crId].title = tempchr[crId].title

                if source.characters[crId].image is not None:
                    self.characters[crId].image = source.characters[crId].image

                else:
                    self.characters[crId].image = tempchr[crId].image

                if source.characters[crId].desc is not None:
                    self.characters[crId].desc = source.characters[crId].desc

                else:
                    self.characters[crId].desc = tempchr[crId].desc

                if source.characters[crId].aka is not None:
                    self.characters[crId].aka = source.characters[crId].aka

                else:
                    self.characters[crId].aka = tempchr[crId].aka

                if source.characters[crId].tags is not None:
                    self.characters[crId].tags = source.characters[crId].tags

                else:
                    self.characters[crId].tags = tempchr[crId].tags

                if source.characters[crId].notes is not None:
                    self.characters[crId].notes = source.characters[crId].notes

                else:
                    self.characters[crId].notes = tempchr[crId].notes

                if source.characters[crId].bio is not None:
                    self.characters[crId].bio = source.characters[crId].bio

                else:
                    self.characters[crId].bio = tempchr[crId].bio

                if source.characters[crId].goals is not None:
                    self.characters[crId].goals = source.characters[crId].goals

                else:
                    self.characters[crId].goals = tempchr[crId].goals

                if source.characters[crId].fullName is not None:
                    self.characters[crId].fullName = source.characters[crId].fullName

                else:
                    self.characters[crId].fullName = tempchr[crId].fullName

                if source.characters[crId].isMajor is not None:
                    self.characters[crId].isMajor = source.characters[crId].isMajor

                else:
                    self.characters[crId].isMajor = tempchr[crId].isMajor

        #--- Merge scenes.

        sourceHasSceneContent = False

        for scId in source.scenes:

            if not scId in self.scenes:
                self.scenes[scId] = Scene()

            if source.scenes[scId].title:
                # avoids deleting the title, if it is empty by accident
                self.scenes[scId].title = source.scenes[scId].title

            if source.scenes[scId].desc is not None:
                self.scenes[scId].desc = source.scenes[scId].desc

            if source.scenes[scId].sceneContent is not None:
                self.scenes[scId].sceneContent = source.scenes[scId].sceneContent
                sourceHasSceneContent = True

            if source.scenes[scId].isUnused is not None:
                self.scenes[scId].isUnused = source.scenes[scId].isUnused

            if source.scenes[scId].isNotesScene is not None:
                self.scenes[scId].isNotesScene = source.scenes[scId].isNotesScene

            if source.scenes[scId].isTodoScene is not None:
                self.scenes[scId].isTodoScene = source.scenes[scId].isTodoScene

            if source.scenes[scId].status is not None:
                self.scenes[scId].status = source.scenes[scId].status

            if source.scenes[scId].sceneNotes is not None:
                self.scenes[scId].sceneNotes = source.scenes[scId].sceneNotes

            if source.scenes[scId].tags is not None:
                self.scenes[scId].tags = source.scenes[scId].tags

            if source.scenes[scId].field1 is not None:
                self.scenes[scId].field1 = source.scenes[scId].field1

            if source.scenes[scId].field2 is not None:
                self.scenes[scId].field2 = source.scenes[scId].field2

            if source.scenes[scId].field3 is not None:
                self.scenes[scId].field3 = source.scenes[scId].field3

            if source.scenes[scId].field4 is not None:
                self.scenes[scId].field4 = source.scenes[scId].field4

            if source.scenes[scId].appendToPrev is not None:
                self.scenes[scId].appendToPrev = source.scenes[scId].appendToPrev

            if source.scenes[scId].date or source.scenes[scId].time:

                if source.scenes[scId].date is not None:
                    self.scenes[scId].date = source.scenes[scId].date

                if source.scenes[scId].time is not None:
                    self.scenes[scId].time = source.scenes[scId].time

            elif source.scenes[scId].minute or source.scenes[scId].hour or source.scenes[scId].day:
                self.scenes[scId].date = None
                self.scenes[scId].time = None

            if source.scenes[scId].minute is not None:
                self.scenes[scId].minute = source.scenes[scId].minute

            if source.scenes[scId].hour is not None:
                self.scenes[scId].hour = source.scenes[scId].hour

            if source.scenes[scId].day is not None:
                self.scenes[scId].day = source.scenes[scId].day

            if source.scenes[scId].lastsMinutes is not None:
                self.scenes[scId].lastsMinutes = source.scenes[scId].lastsMinutes

            if source.scenes[scId].lastsHours is not None:
                self.scenes[scId].lastsHours = source.scenes[scId].lastsHours

            if source.scenes[scId].lastsDays is not None:
                self.scenes[scId].lastsDays = source.scenes[scId].lastsDays

            if source.scenes[scId].isReactionScene is not None:
                self.scenes[scId].isReactionScene = source.scenes[scId].isReactionScene

            if source.scenes[scId].isSubPlot is not None:
                self.scenes[scId].isSubPlot = source.scenes[scId].isSubPlot

            if source.scenes[scId].goal is not None:
                self.scenes[scId].goal = source.scenes[scId].goal

            if source.scenes[scId].conflict is not None:
                self.scenes[scId].conflict = source.scenes[scId].conflict

            if source.scenes[scId].outcome is not None:
                self.scenes[scId].outcome = source.scenes[scId].outcome

            if source.scenes[scId].characters is not None:
                self.scenes[scId].characters = []

                for crId in source.scenes[scId].characters:

                    if crId in self.characters:
                        self.scenes[scId].characters.append(crId)

            if source.scenes[scId].locations is not None:
                self.scenes[scId].locations = []

                for lcId in source.scenes[scId].locations:

                    if lcId in self.locations:
                        self.scenes[scId].locations.append(lcId)

            if source.scenes[scId].items is not None:
                self.scenes[scId].items = []

                for itId in source.scenes[scId].items:

                    if itId in self.items:
                        self.scenes[scId].items.append(itId)

        #--- Merge chapters.

        for chId in source.chapters:

            if not chId in self.chapters:
                self.chapters[chId] = Chapter()

            if source.chapters[chId].title:
                # avoids deleting the title, if it is empty by accident
                self.chapters[chId].title = source.chapters[chId].title

            if source.chapters[chId].desc is not None:
                self.chapters[chId].desc = source.chapters[chId].desc

            if source.chapters[chId].chLevel is not None:
                self.chapters[chId].chLevel = source.chapters[chId].chLevel

            if source.chapters[chId].oldType is not None:
                self.chapters[chId].oldType = source.chapters[chId].oldType

            if source.chapters[chId].chType is not None:
                self.chapters[chId].chType = source.chapters[chId].chType

            if source.chapters[chId].isUnused is not None:
                self.chapters[chId].isUnused = source.chapters[chId].isUnused

            if source.chapters[chId].suppressChapterTitle is not None:
                self.chapters[chId].suppressChapterTitle = source.chapters[chId].suppressChapterTitle

            if source.chapters[chId].suppressChapterBreak is not None:
                self.chapters[chId].suppressChapterBreak = source.chapters[chId].suppressChapterBreak

            if source.chapters[chId].isTrash is not None:
                self.chapters[chId].isTrash = source.chapters[chId].isTrash

            #--- Merge the chapter's scene list.
            # New scenes may be added.
            # Existing scenes may be moved to another chapter.
            # Deletion of scenes is not considered.
            # The scene's sort order may not change.

            if source.chapters[chId].srtScenes is not None:

                # Remove scenes that have been moved to another chapter from the scene list.

                srtScenes = []

                for scId in self.chapters[chId].srtScenes:

                    if scId in source.chapters[chId].srtScenes or not scId in source.scenes:
                        srtScenes.append(scId)
                        # The scene has not moved to another chapter or isn't imported

                    self.chapters[chId].srtScenes = srtScenes

                # Add new or moved scenes to the scene list.

                merge_lists(source.chapters[chId].srtScenes, self.chapters[chId].srtScenes)

        #--- Merge project attributes.

        if source.title:
            # avoids deleting the title, if it is empty by accident
            self.title = source.title

        if source.desc is not None:
            self.desc = source.desc

        if source.author is not None:
            self.author = source.author

        if source.fieldTitle1 is not None:
            self.fieldTitle1 = source.fieldTitle1

        if source.fieldTitle2 is not None:
            self.fieldTitle2 = source.fieldTitle2

        if source.fieldTitle3 is not None:
            self.fieldTitle3 = source.fieldTitle3

        if source.fieldTitle4 is not None:
            self.fieldTitle4 = source.fieldTitle4

        # Add new chapters to the chapter list.
        # Deletion of chapters is not considered.
        # The sort order of chapters may not change.

        merge_lists(source.srtChapters, self.srtChapters)

        # Split scenes by inserted part/chapter/scene dividers.
        # This must be done after regular merging
        # in order to avoid creating duplicate IDs.

        if sourceHasSceneContent:
            sceneSplitter = Splitter()
            sceneSplitter.split_scenes(self)

        return 'yWriter project data updated or created.'

    def write(self):
        """Open the yWriter xml file located at filePath and 
        replace a set of attributes not being None.
        Return a message beginning with the ERROR constant in case of error.
        Override the superclass method.
        """

        def build_scene_subtree(xmlScn, prjScn):

            if prjScn.title is not None:

                try:
                    xmlScn.find('Title').text = prjScn.title

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Title').text = prjScn.title

            if xmlScn.find('BelongsToChID') is None:

                for chId in self.chapters:

                    if scId in self.chapters[chId].srtScenes:
                        ET.SubElement(xmlScn, 'BelongsToChID').text = chId
                        break

            if prjScn.desc is not None:

                try:
                    xmlScn.find('Desc').text = prjScn.desc

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Desc').text = prjScn.desc

            # Scene content is overwritten in subclasses.

            if xmlScn.find('SceneContent') is None:
                ET.SubElement(xmlScn, 'SceneContent').text = prjScn.sceneContent

            if xmlScn.find('WordCount') is None:
                ET.SubElement(xmlScn, 'WordCount').text = str(prjScn.wordCount)

            if xmlScn.find('LetterCount') is None:
                ET.SubElement(xmlScn, 'LetterCount').text = str(prjScn.letterCount)

            if prjScn.isUnused:

                if xmlScn.find('Unused') is None:
                    ET.SubElement(xmlScn, 'Unused').text = '-1'

            elif xmlScn.find('Unused') is not None:
                xmlScn.remove(xmlScn.find('Unused'))

            if prjScn.isNotesScene:
                scFields = xmlScn.find('Fields')

                try:
                    scFields.find('Field_SceneType').text = '1'

                except(AttributeError):
                    scFields = ET.SubElement(xmlScn, 'Fields')
                    ET.SubElement(scFields, 'Field_SceneType').text = '1'

            elif xmlScn.find('Fields') is not None:
                scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '1':
                        scFields.remove(scFields.find('Field_SceneType'))

            if prjScn.isTodoScene:
                scFields = xmlScn.find('Fields')

                try:
                    scFields.find('Field_SceneType').text = '2'

                except(AttributeError):
                    scFields = ET.SubElement(xmlScn, 'Fields')
                    ET.SubElement(scFields, 'Field_SceneType').text = '2'

            elif xmlScn.find('Fields') is not None:
                scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '2':
                        scFields.remove(scFields.find('Field_SceneType'))

            if prjScn.status is not None:
                try:
                    xmlScn.find('Status').text = str(prjScn.status)

                except:
                    ET.SubElement(xmlScn, 'Status').text = str(prjScn.status)

            if prjScn.sceneNotes is not None:

                try:
                    xmlScn.find('Notes').text = prjScn.sceneNotes

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Notes').text = prjScn.sceneNotes

            if prjScn.tags is not None:

                try:
                    xmlScn.find('Tags').text = ';'.join(prjScn.tags)

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Tags').text = ';'.join(prjScn.tags)

            if prjScn.field1 is not None:

                try:
                    xmlScn.find('Field1').text = prjScn.field1

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field1').text = prjScn.field1

            if prjScn.field2 is not None:

                try:
                    xmlScn.find('Field2').text = prjScn.field2

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field2').text = prjScn.field2

            if prjScn.field3 is not None:

                try:
                    xmlScn.find('Field3').text = prjScn.field3

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field3').text = prjScn.field3

            if prjScn.field4 is not None:

                try:
                    xmlScn.find('Field4').text = prjScn.field4

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field4').text = prjScn.field4

            if prjScn.appendToPrev:

                if xmlScn.find('AppendToPrev') is None:
                    ET.SubElement(xmlScn, 'AppendToPrev').text = '-1'

            elif xmlScn.find('AppendToPrev') is not None:
                xmlScn.remove(xmlScn.find('AppendToPrev'))

            # Date/time information

            if (prjScn.date is not None) and (prjScn.time is not None):
                dateTime = f'{prjScn.date} {prjScn.time}'

                if xmlScn.find('SpecificDateTime') is not None:
                    xmlScn.find('SpecificDateTime').text = dateTime

                else:
                    ET.SubElement(xmlScn, 'SpecificDateTime').text = dateTime
                    ET.SubElement(xmlScn, 'SpecificDateMode').text = '-1'

                    if xmlScn.find('Day') is not None:
                        xmlScn.remove(xmlScn.find('Day'))

                    if xmlScn.find('Hour') is not None:
                        xmlScn.remove(xmlScn.find('Hour'))

                    if xmlScn.find('Minute') is not None:
                        xmlScn.remove(xmlScn.find('Minute'))

            elif (prjScn.day is not None) or (prjScn.hour is not None) or (prjScn.minute is not None):

                if xmlScn.find('SpecificDateTime') is not None:
                    xmlScn.remove(xmlScn.find('SpecificDateTime'))

                if xmlScn.find('SpecificDateMode') is not None:
                    xmlScn.remove(xmlScn.find('SpecificDateMode'))

                if prjScn.day is not None:

                    try:
                        xmlScn.find('Day').text = prjScn.day

                    except(AttributeError):
                        ET.SubElement(xmlScn, 'Day').text = prjScn.day

                if prjScn.hour is not None:

                    try:
                        xmlScn.find('Hour').text = prjScn.hour

                    except(AttributeError):
                        ET.SubElement(xmlScn, 'Hour').text = prjScn.hour

                if prjScn.minute is not None:

                    try:
                        xmlScn.find('Minute').text = prjScn.minute

                    except(AttributeError):
                        ET.SubElement(xmlScn, 'Minute').text = prjScn.minute

            if prjScn.lastsDays is not None:

                try:
                    xmlScn.find('LastsDays').text = prjScn.lastsDays

                except(AttributeError):
                    ET.SubElement(xmlScn, 'LastsDays').text = prjScn.lastsDays

            if prjScn.lastsHours is not None:

                try:
                    xmlScn.find('LastsHours').text = prjScn.lastsHours

                except(AttributeError):
                    ET.SubElement(xmlScn, 'LastsHours').text = prjScn.lastsHours

            if prjScn.lastsMinutes is not None:

                try:
                    xmlScn.find('LastsMinutes').text = prjScn.lastsMinutes

                except(AttributeError):
                    ET.SubElement(xmlScn, 'LastsMinutes').text = prjScn.lastsMinutes

            # Plot related information

            if prjScn.isReactionScene:

                if xmlScn.find('ReactionScene') is None:
                    ET.SubElement(xmlScn, 'ReactionScene').text = '-1'

            elif xmlScn.find('ReactionScene') is not None:
                xmlScn.remove(xmlScn.find('ReactionScene'))

            if prjScn.isSubPlot:

                if xmlScn.find('SubPlot') is None:
                    ET.SubElement(xmlScn, 'SubPlot').text = '-1'

            elif xmlScn.find('SubPlot') is not None:
                xmlScn.remove(xmlScn.find('SubPlot'))

            if prjScn.goal is not None:

                try:
                    xmlScn.find('Goal').text = prjScn.goal

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Goal').text = prjScn.goal

            if prjScn.conflict is not None:

                try:
                    xmlScn.find('Conflict').text = prjScn.conflict

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Conflict').text = prjScn.conflict

            if prjScn.outcome is not None:

                try:
                    xmlScn.find('Outcome').text = prjScn.outcome

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Outcome').text = prjScn.outcome

            if prjScn.image is not None:

                try:
                    xmlScn.find('ImageFile').text = prjScn.image

                except(AttributeError):
                    ET.SubElement(xmlScn, 'ImageFile').text = prjScn.image

            if prjScn.characters is not None:
                characters = xmlScn.find('Characters')

                try:
                    for oldCrId in characters.findall('CharID'):
                        characters.remove(oldCrId)

                except(AttributeError):
                    characters = ET.SubElement(xmlScn, 'Characters')

                for crId in prjScn.characters:
                    ET.SubElement(characters, 'CharID').text = crId

            if prjScn.locations is not None:
                locations = xmlScn.find('Locations')

                try:
                    for oldLcId in locations.findall('LocID'):
                        locations.remove(oldLcId)

                except(AttributeError):
                    locations = ET.SubElement(xmlScn, 'Locations')

                for lcId in prjScn.locations:
                    ET.SubElement(locations, 'LocID').text = lcId

            if prjScn.items is not None:
                items = xmlScn.find('Items')

                try:
                    for oldItId in items.findall('ItemID'):
                        items.remove(oldItId)

                except(AttributeError):
                    items = ET.SubElement(xmlScn, 'Items')

                for itId in prjScn.items:
                    ET.SubElement(items, 'ItemID').text = itId

        def build_chapter_subtree(xmlChp, prjChp, sortOrder):

            try:
                xmlChp.find('SortOrder').text = str(sortOrder)

            except(AttributeError):
                ET.SubElement(xmlChp, 'SortOrder').text = str(sortOrder)

            try:
                xmlChp.find('Title').text = prjChp.title

            except(AttributeError):
                ET.SubElement(xmlChp, 'Title').text = prjChp.title

            if prjChp.desc is not None:

                try:
                    xmlChp.find('Desc').text = prjChp.desc

                except(AttributeError):
                    ET.SubElement(xmlChp, 'Desc').text = prjChp.desc

            if xmlChp.find('SectionStart') is not None:

                if prjChp.chLevel == 0:
                    xmlChp.remove(xmlChp.find('SectionStart'))

            elif prjChp.chLevel == 1:
                ET.SubElement(xmlChp, 'SectionStart').text = '-1'

            if prjChp.oldType is not None:

                try:
                    xmlChp.find('Type').text = str(prjChp.oldType)

                except(AttributeError):
                    ET.SubElement(xmlChp, 'Type').text = str(prjChp.oldType)

            if prjChp.chType is not None:

                try:
                    xmlChp.find('ChapterType').text = str(prjChp.chType)

                except(AttributeError):
                    ET.SubElement(xmlChp, 'ChapterType').text = str(prjChp.chType)

            if prjChp.isUnused:

                if xmlChp.find('Unused') is None:
                    ET.SubElement(xmlChp, 'Unused').text = '-1'

            elif xmlChp.find('Unused') is not None:
                xmlChp.remove(xmlChp.find('Unused'))

            #--- Rebuild the chapter's scene list.

            if prjChp.srtScenes:
                xScnList = xmlChp.find('Scenes')

                if xScnList is not None:
                    xmlChp.remove(xScnList)

                sortSc = ET.SubElement(xmlChp, 'Scenes')

                for scId in prjChp.srtScenes:
                    ET.SubElement(sortSc, 'ScID').text = scId

        def build_location_subtree(xmlLoc, prjLoc, sortOrder):
            ET.SubElement(xmlLoc, 'ID').text = lcId

            if prjLoc.title is not None:
                ET.SubElement(xmlLoc, 'Title').text = prjLoc.title

            if prjLoc.image is not None:
                ET.SubElement(xmlLoc, 'ImageFile').text = prjLoc.image

            if prjLoc.desc is not None:
                ET.SubElement(xmlLoc, 'Desc').text = prjLoc.desc

            if prjLoc.aka is not None:
                ET.SubElement(xmlLoc, 'AKA').text = prjLoc.aka

            if prjLoc.tags is not None:
                ET.SubElement(xmlLoc, 'Tags').text = ';'.join(prjLoc.tags)

            ET.SubElement(xmlLoc, 'SortOrder').text = str(sortOrder)

        def build_item_subtree(xmlItm, prjItm, sortOrder):
            ET.SubElement(xmlItm, 'ID').text = itId

            if prjItm.title is not None:
                ET.SubElement(xmlItm, 'Title').text = prjItm.title

            if prjItm.image is not None:
                ET.SubElement(xmlItm, 'ImageFile').text = prjItm.image

            if prjItm.desc is not None:
                ET.SubElement(xmlItm, 'Desc').text = prjItm.desc

            if prjItm.aka is not None:
                ET.SubElement(xmlItm, 'AKA').text = prjItm.aka

            if prjItm.tags is not None:
                ET.SubElement(xmlItm, 'Tags').text = ';'.join(prjItm.tags)

            ET.SubElement(xmlItm, 'SortOrder').text = str(sortOrder)

        def build_character_subtree(xmlCrt, prjCrt, sortOrder):
            ET.SubElement(xmlCrt, 'ID').text = crId

            if prjCrt.title is not None:
                ET.SubElement(xmlCrt, 'Title').text = prjCrt.title

            if prjCrt.desc is not None:
                ET.SubElement(xmlCrt, 'Desc').text = prjCrt.desc

            if prjCrt.image is not None:
                ET.SubElement(xmlCrt, 'ImageFile').text = prjCrt.image

            ET.SubElement(xmlCrt, 'SortOrder').text = str(sortOrder)

            if prjCrt.notes is not None:
                ET.SubElement(xmlCrt, 'Notes').text = prjCrt.notes

            if prjCrt.aka is not None:
                ET.SubElement(xmlCrt, 'AKA').text = prjCrt.aka

            if prjCrt.tags is not None:
                ET.SubElement(xmlCrt, 'Tags').text = ';'.join(prjCrt.tags)

            if prjCrt.bio is not None:
                ET.SubElement(xmlCrt, 'Bio').text = prjCrt.bio

            if prjCrt.goals is not None:
                ET.SubElement(xmlCrt, 'Goals').text = prjCrt.goals

            if prjCrt.fullName is not None:
                ET.SubElement(xmlCrt, 'FullName').text = prjCrt.fullName

            if prjCrt.isMajor:
                ET.SubElement(xmlCrt, 'Major').text = '-1'

        def build_project_subtree(xmlPrj):

            VER = '7'

            try:
                xmlPrj.find('Ver').text = VER

            except(AttributeError):
                ET.SubElement(xmlPrj, 'Ver').text = VER

            if self.title is not None:

                try:
                    xmlPrj.find('Title').text = self.title

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'Title').text = self.title

            if self.desc is not None:

                try:
                    xmlPrj.find('Desc').text = self.desc

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'Desc').text = self.desc

            if self.author is not None:

                try:
                    xmlPrj.find('AuthorName').text = self.author

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'AuthorName').text = self.author

            if self.fieldTitle1 is not None:

                try:
                    xmlPrj.find('FieldTitle1').text = self.fieldTitle1

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'FieldTitle1').text = self.fieldTitle1

            if self.fieldTitle2 is not None:

                try:
                    xmlPrj.find('FieldTitle2').text = self.fieldTitle2

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'FieldTitle2').text = self.fieldTitle2

            if self.fieldTitle3 is not None:

                try:
                    xmlPrj.find('FieldTitle3').text = self.fieldTitle3

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'FieldTitle3').text = self.fieldTitle3

            if self.fieldTitle4 is not None:

                try:
                    xmlPrj.find('FieldTitle4').text = self.fieldTitle4

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'FieldTitle4').text = self.fieldTitle4

        #--- Start write method.

        if self.is_locked():
            return f'{ERROR}yWriter seems to be open. Please close first.'

        TAG = 'YWRITER7'
        xmlScenes = {}
        xmlChapters = {}

        try:
            root = self.tree.getroot()
            xmlPrj = root.find('PROJECT')
            locations = root.find('LOCATIONS')
            items = root.find('ITEMS')
            characters = root.find('CHARACTERS')
            scenes = root.find('SCENES')
            chapters = root.find('CHAPTERS')

        except(AttributeError):
            root = ET.Element(TAG)
            xmlPrj = ET.SubElement(root, 'PROJECT')
            locations = ET.SubElement(root, 'LOCATIONS')
            items = ET.SubElement(root, 'ITEMS')
            characters = ET.SubElement(root, 'CHARACTERS')
            scenes = ET.SubElement(root, 'SCENES')
            chapters = ET.SubElement(root, 'CHAPTERS')

        #--- Process project attributes.

        build_project_subtree(xmlPrj)

        #--- Process locations.
        # Remove LOCATION entries in order to rewrite
        # the LOCATIONS section in a modified sort order.

        for xmlLoc in locations.findall('LOCATION'):
            locations.remove(xmlLoc)

        # Add the new XML location subtrees to the project tree.

        sortOrder = 0

        for lcId in self.srtLocations:
            sortOrder += 1
            xmlLoc = ET.SubElement(locations, 'LOCATION')
            build_location_subtree(xmlLoc, self.locations[lcId], sortOrder)

        #--- Process items.
        # Remove ITEM entries in order to rewrite
        # the ITEMS section in a modified sort order.

        for xmlItm in items.findall('ITEM'):
            items.remove(xmlItm)

        # Add the new XML item subtrees to the project tree.

        sortOrder = 0

        for itId in self.srtItems:
            sortOrder += 1
            xmlItm = ET.SubElement(items, 'ITEM')
            build_item_subtree(xmlItm, self.items[itId], sortOrder)

        #--- Process characters.
        # Remove CHARACTER entries in order to rewrite
        # the CHARACTERS section in a modified sort order.

        for xmlCrt in characters.findall('CHARACTER'):
            characters.remove(xmlCrt)

        # Add the new XML character subtrees to the project tree.

        sortOrder = 0

        for crId in self.srtCharacters:
            sortOrder += 1
            xmlCrt = ET.SubElement(characters, 'CHARACTER')
            build_character_subtree(xmlCrt, self.characters[crId], sortOrder)

        #--- Process scenes.
        # Save the original XML scene subtrees
        # and remove them from the project tree.

        for xmlScn in scenes.findall('SCENE'):
            scId = xmlScn.find('ID').text
            xmlScenes[scId] = xmlScn
            scenes.remove(xmlScn)

        # Add the new XML scene subtrees to the project tree.

        for scId in self.scenes:

            if not scId in xmlScenes:
                xmlScenes[scId] = ET.Element('SCENE')
                ET.SubElement(xmlScenes[scId], 'ID').text = scId

            build_scene_subtree(xmlScenes[scId], self.scenes[scId])
            scenes.append(xmlScenes[scId])

        #--- Process chapters.
        # Save the original XML chapter subtree
        # and remove it from the project tree.

        for xmlChp in chapters.findall('CHAPTER'):
            chId = xmlChp.find('ID').text
            xmlChapters[chId] = xmlChp
            chapters.remove(xmlChp)

        # Add the new XML chapter subtrees to the project tree.

        sortOrder = 0

        for chId in self.srtChapters:
            sortOrder += 1

            if not chId in xmlChapters:
                xmlChapters[chId] = ET.Element('CHAPTER')
                ET.SubElement(xmlChapters[chId], 'ID').text = chId

            build_chapter_subtree(xmlChapters[chId], self.chapters[chId], sortOrder)

            chapters.append(xmlChapters[chId])

        indent(root)

        # Modify the scene contents of an existing xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if self.scenes[scId].sceneContent is not None:
                scn.find('SceneContent').text = self.scenes[scId].sceneContent
                scn.find('WordCount').text = str(self.scenes[scId].wordCount)
                scn.find('LetterCount').text = str(self.scenes[scId].letterCount)

            try:
                scn.remove(scn.find('RTFFile'))

            except:
                pass

        self.tree = ET.ElementTree(root)
        message = self.ywTreeWriter.write_element_tree(self)

        if message.startswith(ERROR):
            return message

        return self.ywPostprocessor.postprocess_xml_file(self.filePath)

    def is_locked(self):
        """Return True if a .lock file placed by yWriter exists.
        Otherwise, return False. 
        """
        return os.path.isfile(f'{self.filePath}.lock')


class NovelystTk(MainTk):
    """A tkinter GUI class for yWriter project processing.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.root.geometry("800x500")

        # Create an application window with a chapter and a scene frame.

        self.appWindow = tk.PanedWindow(self.mainWindow, sashrelief=tk.RAISED)
        self.appWindow.pack(expand=True, fill='both')
        self.chapterFrame = tk.Frame(self.appWindow)
        self.appWindow.add(self.chapterFrame)
        self.sceneFrame = tk.Frame(self.appWindow)
        self.appWindow.add(self.sceneFrame)

        # Create a chapter window with a chapter tree and an info box.

        self.chapterWindow = tk.PanedWindow(self.chapterFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.chapterWindow.pack(expand=True, fill='both')
        self.chapterTree = ttk.Treeview(self.chapterWindow)
        self.chapterWindow.add(self.chapterTree)
        self.chapterInfoWin = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1,  height=4, width=10)
        self.chapterWindow.add(self.chapterInfoWin)

        self.chapterTree.bind('<<TreeviewSelect>>', self.on_chapter_select)

        # Create a scene window with a scene tree and an info box.

        self.sceneWindow = tk.PanedWindow(self.sceneFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.sceneWindow.pack(expand=True, fill='both')
        self.sceneTree = ttk.Treeview(self.sceneWindow)
        self.sceneWindow.add(self.sceneTree)
        self.sceneInfoWin = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1,  height=4, width=10)
        self.sceneWindow.add(self.sceneInfoWin)

        self.sceneTree.bind('<<TreeviewSelect>>', self.on_scene_select)

    def on_chapter_select(self, event):
        chId = self.chapterTree.selection()[0]
        self.set_scenes(chId)
        self.set_chapter_info(chId)

    def on_scene_select(self, event):
        scId = self.sceneTree.selection()[0]
        self.set_scene_info(scId)

    def reset_chapters(self):

        for child in self.chapterTree.get_children(''):
            self.chapterTree.delete(child)

    def set_chapters(self):
        self.reset_chapters()

        for chId in self.ywPrj.srtChapters:
            self.chapterTree.insert('', 'end', chId, text=self.ywPrj.chapters[chId].title)

    def reset_scenes(self):

        for child in self.sceneTree.get_children(''):
            self.sceneTree.delete(child)

        self.sceneInfoWin.delete('1.0', tk.END)

    def set_scenes(self, chId):
        self.reset_scenes()

        for scId in self.ywPrj.chapters[chId].srtScenes:
            self.sceneTree.insert('', 'end', scId, text=self.ywPrj.scenes[scId].title)

    def set_chapter_info(self, chId):

        if self.ywPrj.chapters[chId].desc is not None:
            text = self.ywPrj.chapters[chId].desc

        else:
            text = ''

        self.chapterInfoWin.delete('1.0', tk.END)
        self.chapterInfoWin.insert(tk.END, text)

    def set_scene_info(self, scId):

        if self.ywPrj.scenes[scId].desc is not None:
            text = self.ywPrj.scenes[scId].desc

        else:
            text = ''

        self.sceneInfoWin.delete('1.0', tk.END)
        self.sceneInfoWin.insert(tk.END, text)

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.chapterMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Chapter', menu=self.chapterMenu)
        self.mainMenu.entryconfig('Chapter', state='disabled')
        self.sceneMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Scene', menu=self.sceneMenu)
        self.mainMenu.entryconfig('Scene', state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Chapter', state='disabled')
        self.mainMenu.entryconfig('Scene', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Chapter', state='normal')
        self.mainMenu.entryconfig('Scene', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self.ywPrj = Yw7File(fileName)
        message = self.ywPrj.read()

        if message.startswith(ERROR):
            self.close_project()
            self.statusBar.config(text=message)
            return ''

        if self.ywPrj.title:
            titleView = self.ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self.ywPrj.author:
            authorView = self.ywPrj.author

        else:
            authorView = 'Unknown author'

        self.titleBar.config(text=f'{titleView} by {authorView}')
        self.enable_menu()
        self.set_chapters()
        return fileName

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        self.reset_chapters()
        self.reset_scenes()
        self.chapterInfoWin.delete('1.0', tk.END)
        self.sceneInfoWin.delete('1.0', tk.END)
        super().close_project()

APPNAME = 'novelyst'

SETTINGS = dict(
    yw_last_open='',
)

OPTIONS = {}


def run(sourcePath='', installDir=''):

    #--- Load configuration.

    iniFile = f'{installDir}{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = {}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    #--- Get initial project path.

    if not sourcePath or not os.path.isfile(sourcePath):
        sourcePath = kwargs['yw_last_open']

    #--- Instantiate the app object.

    app = NovelystTk('novelyst @release', **kwargs)
    app.open_project(sourcePath)
    app.start()

    #--- Save project specific configuration

    for keyword in app.kwargs:

        if keyword in configuration.options:
            configuration.options[keyword] = app.kwargs[keyword]

        elif keyword in configuration.settings:
            configuration.settings[keyword] = app.kwargs[keyword]

        configuration.write(iniFile)


if __name__ == '__main__':

    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}/config/'

    except:
        installDir = ''

    os.makedirs(installDir, exist_ok=True)

    if len(sys.argv) == 1:
        run('', installDir)

    else:
        parser = argparse.ArgumentParser(
            description='Novel metadata organizer',
            epilog='')
        parser.add_argument('sourcePath',
                            metavar='Sourcefile',
                            help='The path of the yWriter project file.')

        args = parser.parse_args()
        run(args.sourcePath, installDir)
