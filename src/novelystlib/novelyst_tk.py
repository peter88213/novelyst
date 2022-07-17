""""Provide a tkinter GUI framework for novelyst.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import glob
import importlib
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from pywriter.pywriter_globals import ERROR
from pywriter.ui.main_tk import MainTk
from pywriter.file.doc_open import open_document
from novelystlib.nv_exporter import NvExporter
from novelystlib.tree_viewer import TreeViewer
from novelystlib.yw7_work_file import Yw7WorkFile
from novelystlib.basic_view import BasicView
from novelystlib.element_view import ElementView
from novelystlib.project_view import ProjectView
from novelystlib.chapter_view import ChapterView
from novelystlib.scene_view import SceneView
from novelystlib.arc_view import ArcView
from novelystlib.character_view import CharacterView

# Import plugins from the "plugin" subdirectory.
plugins = []
pluginPath = f'{sys.path[0]}/plugin'
if os.path.isdir(pluginPath):
    sys.path.append(pluginPath)
    files = glob.glob(f'{pluginPath}/*.py')
    for file in files:
        moduleName = os.path.split(file)[1][:-3]
        module = importlib.import_module(moduleName)
        try:
            plugins.append(module.Plugin)
        except AttributeError:
            pass


class NovelystTk(MainTk):
    """tkinter GUI framework for novelyst."""
    _KEY_NEW_PROJECT = ('<Control-n>', 'Ctrl-N')
    _KEY_LOCK_PROJECT = ('<Control-l>', 'Ctrl-L')
    _KEY_UNLOCK_PROJECT = ('<Control-u>', 'Ctrl-U')
    _KEY_YWRITER = ('<Control-Alt-y>', 'Ctrl-Alt-Y')
    _KEY_FOLDER = ('<Control-p>', 'Ctrl-P')
    _KEY_RELOAD_PROJECT = ('<Control-r>', 'Ctrl-R')
    _KEY_REFRESH_TREE = ('<F5>', 'F5')
    _KEY_SAVE_PROJECT = ('<Control-s>', 'Ctrl-S')
    _KEY_SAVE_AS = ('<Control-S>', 'Ctrl-Shift-S')
    _COLOR_NOTE_WINDOWS = 'lemon chiffon'

    _YW_CLASS = Yw7WorkFile

    def __init__(self, colTitle, **kwargs):
        """Put a text box to the GUI main window.
        
        Required keyword arguments:
            root_geometry -- str: geometry of the root window.
            tree_frame_width -- int: width of the chapter frame.
            data_frame_width -- int: width of the data frame.
            color_locked_bg -- str: tk color name for Footer background when locked.
            color_locked_fg -- str: tk color name for Footer foreground when locked.
            color_modified_bg -- str: tk color name for Footer background when modified.
            color_modified_fg -- str: tk color name for Footer foreground when modified.
    
        Extends the superclass constructor.
        """
        self.kwargs = kwargs
        self._plugins = []
        super().__init__(colTitle, **kwargs)
        rootWidth = int(kwargs['root_geometry'].split('x', maxsplit=1)[0])
        self._internalModificationFlag = False
        self._internalLockFlag = False
        self._exporter = NvExporter(self)

        # Create an application window with a tree frame, a middle frame, and a data frame.
        self.appWindow = tk.Frame(self.mainWindow)
        self.appWindow.pack(expand=True, fill='both')
        self.treeFrame = tk.Frame(self.appWindow)
        self.treeFrame.pack(side=tk.LEFT, expand=True, fill='both')
        self.middleFrame = tk.Frame(self.appWindow)
        self.middleFrame.pack(side=tk.LEFT, expand=False, fill='both')
        self.dataFrame = tk.Frame(self.appWindow, width=kwargs['data_frame_width'])
        self.dataFrame.pack_propagate(0)
        self.dataFrame.pack(expand=True, fill='both')

        # Create a novel tree window.
        self.treeWindow = tk.PanedWindow(self.treeFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.treeWindow.pack(expand=True, fill='both')
        self.tv = TreeViewer(self, self.treeWindow, **kwargs)

        #--- Create a data window.
        self.dataWindow = tk.PanedWindow(self.dataFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.dataWindow.pack(expand=True, fill='both')

        # Place a title label inside the data window.
        self.elementTitle = tk.StringVar(value='')
        self._titleLabel = tk.Entry(bd=0, textvariable=self.elementTitle, relief=tk.FLAT)
        self.dataWindow.add(self._titleLabel)

        # Place a description window inside the data window.
        self.descWindow = scrolledtext.ScrolledText(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=15, width=10, padx=5, pady=5)
        self.dataWindow.add(self.descWindow, minsize=250)

        # Place a values window inside the data window.
        self.valuesWindow = tk.Frame()
        self.dataWindow.add(self.valuesWindow, minsize=400)

        # Place a notes window inside the data window.
        self.notesWindow = scrolledtext.ScrolledText(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=4, width=10, padx=5, pady=5, bg=self._COLOR_NOTE_WINDOWS)
        self.dataWindow.add(self.notesWindow)

        self._elementView = BasicView(self, None)
        # Requires windows and frames initialized

        #--- Build the main menu

        # Files
        self.fileMenu = tk.Menu(self.mainMenu, title='Files', tearoff=0)
        self.mainMenu.add_cascade(label='File', underline=0, menu=self.fileMenu)
        self.fileMenu.add_command(label='New', underline=0, accelerator=self._KEY_NEW_PROJECT[1], command=self.new_project)
        self.fileMenu.add_command(label='Open...', underline=0, accelerator=self._KEY_OPEN_PROJECT[1], command=lambda: self.open_project(''))
        self.fileMenu.add_command(label='Reload', underline=0, accelerator=self._KEY_RELOAD_PROJECT[1], command=self.reload_project)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Refresh Tree', underline=8, accelerator=self._KEY_REFRESH_TREE[1], command=self.refresh_tree)
        self.fileMenu.add_command(label='Lock', underline=0, accelerator=self._KEY_LOCK_PROJECT[1], command=self.lock)
        self.fileMenu.add_command(label='Unlock', underline=0, accelerator=self._KEY_UNLOCK_PROJECT[1], command=self.unlock)
        self.fileMenu.add_command(label='Open with yWriter', underline=10, accelerator=self._KEY_YWRITER[1], command=self.launch_yWriter)
        self.fileMenu.add_command(label='Open Project folder', underline=5, accelerator=self._KEY_FOLDER[1], command=self.open_folder)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Save', underline=0, accelerator=self._KEY_SAVE_PROJECT[1], command=self.save_project)
        self.fileMenu.add_command(label='Save as...', underline=5, accelerator=self._KEY_SAVE_AS[1], command=self.save_as)
        self.fileMenu.add_command(label='Remove custom fields', command=self.remove_custom_fields)
        self.fileMenu.add_command(label='Close', underline=0, command=self.close_project)
        self.fileMenu.add_command(label='Exit', underline=1, accelerator=self._KEY_QUIT_PROGRAM[1], command=self.on_quit)

        # View
        self.viewMenu = tk.Menu(self.mainMenu, title='View', tearoff=0)
        self.mainMenu.add_cascade(label='View', menu=self.viewMenu)
        self.viewMenu.add_command(label='Chapter level', underline=8, command=lambda: self.tv.show_chapters(self.tv.NV_ROOT))
        self.viewMenu.add_command(label='Expand selected', underline=0, command=lambda: self.tv.open_children(self.tv.tree.selection()[0]))
        self.viewMenu.add_command(label='Collapse selected', underline=0, command=lambda: self.tv.close_children(self.tv.tree.selection()[0]))
        self.viewMenu.add_command(label='Expand all', underline=1, command=lambda: self.tv.open_children(''))
        self.viewMenu.add_command(label='Collapse all', underline=1, command=lambda: self.tv.close_children(''))

        # Part
        self.partMenu = tk.Menu(self.mainMenu, title='Part', tearoff=0)
        self.mainMenu.add_cascade(label='Part', menu=self.partMenu)
        self.partMenu.add_command(label='Add', underline=0, command=self.tv.add_part)
        self.partMenu.add_separator()
        self.partMenu.add_command(label='Export part descriptions for editing', underline=12, command=lambda: self._exporter.run(self.ywPrj, '_parts'))

        # Chapter
        self.chapterMenu = tk.Menu(self.mainMenu, title='Chapter', tearoff=0)
        self.mainMenu.add_cascade(label='Chapter', menu=self.chapterMenu)
        self.chapterMenu.add_command(label='Add', underline=0, command=self.tv.add_chapter)
        self.chapterMenu.add_separator()
        self.chapterMenu.add_command(label='Export chapter descriptions for editing', underline=15, command=lambda: self._exporter.run(self.ywPrj, '_chapters'))

        # Scene
        self.sceneMenu = tk.Menu(self.mainMenu, title='Scene', tearoff=0)
        self.mainMenu.add_cascade(label='Scene', menu=self.sceneMenu)
        self.sceneMenu.add_command(label='Add', underline=0, command=self.tv.add_scene)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_cascade(label='Set Type', menu=self.tv._typeMenu)
        self.sceneMenu.add_cascade(label='Set Status', menu=self.tv._scStatusMenu)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_command(label='Export scene descriptions for editing', underline=13, command=lambda: self._exporter.run(self.ywPrj, '_scenes'))
        self.sceneMenu.add_command(label='Export scene list (spreadsheet)', underline=13, command=lambda: self._exporter.run(self.ywPrj, '_scenelist'))

        # Character
        self.characterMenu = tk.Menu(self.mainMenu, title='Character', tearoff=0)
        self.mainMenu.add_cascade(label='Character', menu=self.characterMenu)
        self.characterMenu.add_command(label='Add', underline=0, command=lambda: self.tv.add_world_element(self.tv.CR_ROOT))
        self.characterMenu.add_separator()
        self.characterMenu.add_cascade(label='Set Status', menu=self.tv._crStatusMenu)
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label='Export character descriptions for editing', underline=17, command=lambda: self._exporter.run(self.ywPrj, '_characters'))
        self.characterMenu.add_command(label='Export character list (spreadsheet)', underline=17, command=lambda: self._exporter.run(self.ywPrj, '_charlist'))

        # Location
        self.locationMenu = tk.Menu(self.mainMenu, title='Location', tearoff=0)
        self.mainMenu.add_cascade(label='Location', menu=self.locationMenu)
        self.locationMenu.add_command(label='Add', underline=0, command=lambda: self.tv.add_world_element(self.tv.LC_ROOT))
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label='Export location descriptions for editing', underline=16, command=lambda: self._exporter.run(self.ywPrj, '_locations'))
        self.locationMenu.add_command(label='Export location list (spreadsheet)', underline=16, command=lambda: self._exporter.run(self.ywPrj, '_loclist'))

        # Item
        self.itemMenu = tk.Menu(self.mainMenu, title='Item', tearoff=0)
        self.mainMenu.add_cascade(label='Item', menu=self.itemMenu)
        self.itemMenu.add_command(label='Add', underline=0, command=lambda: self.tv.add_world_element(self.tv.IT_ROOT))
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label='Export item descriptions for editing', underline=12, command=lambda: self._exporter.run(self.ywPrj, '_items'))
        self.itemMenu.add_command(label='Export item list (spreadsheet)', underline=12, command=lambda: self._exporter.run(self.ywPrj, '_itemlist'))

        # Export
        self.exportMenu = tk.Menu(self.mainMenu, title='Export', tearoff=0)
        self.mainMenu.add_cascade(label='Export', menu=self.exportMenu)
        self.exportMenu.add_command(label='Manuscript for editing', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_manuscript'))
        self.exportMenu.add_command(label='Notes chapters for editing', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_notes'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label='Manuscript with visible structure tags for proof reading', underline=43, command=lambda: self._exporter.run(self.ywPrj, '_proof'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label='Manuscript without tags (export only)', underline=25, command=lambda: self._exporter.run(self.ywPrj, '', False))
        self.exportMenu.add_command(label='Brief synopsis (export only)', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_brf_synopsis', False))
        self.exportMenu.add_command(label='Cross references (export only)', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_xref', False))

        self.disable_menu()

        #--- Event bindings.
        self.root.bind(self._KEY_NEW_PROJECT[0], self.new_project)
        self.root.bind(self._KEY_LOCK_PROJECT[0], self.lock)
        self.root.bind(self._KEY_UNLOCK_PROJECT[0], self.unlock)
        self.root.bind(self._KEY_RELOAD_PROJECT[0], self.reload_project)
        self.root.bind(self._KEY_YWRITER[0], self.launch_yWriter)
        self.root.bind(self._KEY_FOLDER[0], self.open_folder)
        self.root.bind(self._KEY_REFRESH_TREE[0], self.refresh_tree)
        self.root.bind(self._KEY_SAVE_PROJECT[0], self.save_project)
        self.root.bind(self._KEY_SAVE_AS[0], self.save_as)

        #--- Initialize _plugins.
        try:
            for pClass in plugins:
                pObj = pClass(self)
                self._plugins.append(pObj)
        except NameError:
            pass

    @property
    def isModified(self):
        return self._internalModificationFlag

    @isModified.setter
    def isModified(self, setFlag):
        if setFlag:
            self._internalModificationFlag = True
            self.pathBar.config(bg=self.kwargs['color_modified_bg'])
            self.pathBar.config(fg=self.kwargs['color_modified_fg'])
        else:
            self._internalModificationFlag = False
            if not self.isLocked:
                self.pathBar.config(bg=self.root.cget('background'))
                self.pathBar.config(fg='black')

    @property
    def isLocked(self):
        return self._internalLockFlag

    @isLocked.setter
    def isLocked(self, setFlag):
        if setFlag:
            if self.isModified and not self._internalLockFlag:
                if self.ask_yes_no('Save and lock?'):
                    self.save_project()
                else:
                    return

            self._internalLockFlag = True
            self.pathBar.config(bg=self.kwargs['color_locked_bg'])
            self.pathBar.config(fg=self.kwargs['color_locked_fg'])
            self.fileMenu.entryconfig('Save', state='disabled')
            self.fileMenu.entryconfig('Lock', state='disabled')
            self.fileMenu.entryconfig('Unlock', state='normal')
        else:
            self._internalLockFlag = False
            self.pathBar.config(bg=self.root.cget('background'))
            self.pathBar.config(fg='black')
            self.fileMenu.entryconfig('Save', state='normal')
            self.fileMenu.entryconfig('Lock', state='normal')
            self.fileMenu.entryconfig('Unlock', state='disabled')

    def lock(self, event=None):
        """Lock the project."""
        if self.ywPrj.filePath is not None:
            self.isLocked = True
            # actually, this is a setter method with conditions
            if self.isLocked:
                self.ywPrj.lock()
                # make it persistent
                return True

        return False

    def unlock(self, event=None):
        """Unlock the project."""
        self.isLocked = False
        self.ywPrj.unlock()
        # make it persistent
        if self.ywPrj.has_changed_on_disk():
            if self.ask_yes_no(f'File has changed on disk. Reload?'):
                self.open_project(self.ywPrj.filePath)

    def launch_yWriter(self, event=None):
        """Launch yWriter with the current project."""
        self.save_project()
        if self.lock():
            open_document(self.ywPrj.filePath)

    def open_folder(self, event=None):
        """Open the project folder."""
        projectDir, __ = os.path.split(self.ywPrj.filePath)
        try:
            os.startfile(os.path.normpath(projectDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % os.path.normpath(projectDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % os.path.normpath(projectDir))
                    # Mac
                except:
                    pass

    def on_quit(self, event=None):
        """Save keyword arguments before exiting the program.."""
        self.close_project()
        self.kwargs['tree_frame_width'] = self.treeFrame.winfo_width()
        # save windows size and position
        self.tv.on_quit(self.kwargs)
        super().on_quit()

    def on_nothing_select(self):
        """Event handler for invalid tree selection."""
        self._elementView.close(self)
        self._elementView = BasicView(self, None)

    def on_narrative_select(self):
        """Event handler for narrative tree root selection."""
        self._elementView.close(self)
        self._elementView = ProjectView(self, self.ywPrj)

    def on_chapter_select(self, chId):
        """Event handler for chapter selection."""
        self._elementView.close(self)
        self._elementView = ChapterView(self, self.ywPrj.chapters[chId])

    def on_scene_select(self, scId):
        """Event handler for scene selection."""
        self._elementView.close(self)
        if self.ywPrj.scenes[scId].isTodoScene:
            self._elementView = ArcView(self, self.ywPrj.scenes[scId])
        elif self.ywPrj.scenes[scId].isNotesScene:
            self._elementView = BasicView(self, self.ywPrj.scenes[scId])
        else:
            self._elementView = SceneView(self, self.ywPrj.scenes[scId])

    def on_character_select(self, crId):
        """Event handler for character selection."""
        self._elementView.close(self)
        self._elementView = CharacterView(self, self.ywPrj.characters[crId])

    def on_location_select(self, lcId):
        """Event handler for location selection."""
        self._elementView.close(self)
        self._elementView = ElementView(self, self.ywPrj.locations[lcId])

    def on_item_select(self, itId):
        """Event handler for item selection."""
        self._elementView.close(self)
        self._elementView = ElementView(self, self.ywPrj.items[itId])

    def open_project(self, fileName=''):
        """Create a yWriter project instance and read the file.
        
        Display project title, description and status.
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        if not super().open_project(fileName):
            return False

        self.show_path(f'{os.path.normpath(self.ywPrj.filePath)} (last saved on {self.ywPrj.fileDate})')
        self.tv.build_tree()
        self.show_status()
        self.isModified = False
        if self.ywPrj.has_lockfile():
            self.isLocked = True
        return True

    def close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        for p in self._plugins:
            try:
                p.on_quit()
            except:
                pass

        if self.isModified:
            if self.ask_yes_no('Save changes?'):
                self.save_project()
            self.isModified = False
        self.tv.reset_tree()
        self.on_nothing_select()
        self.isLocked = False
        super().close_project()

    def refresh_tree(self, event=None):
        """Apply changes and refresh the tree."""
        self._elementView.apply_changes(self)
        self.tv.refresh_tree()

    def reload_project(self, event=None):
        """Discard changes and reload the project."""
        if self.ywPrj.is_locked():
            self.set_info_how(f'{ERROR}yWriter seems to be open. Please close first.')
            return

        if self.isModified and not self.ask_yes_no('Discard changes and reload the project?'):
            return

        if self.ywPrj.has_changed_on_disk() and not self.ask_yes_no('File has changed on disk. Reload anyway?'):
            return

        self.isModified = False
        # This is to avoid another question when closing the project
        self.open_project(self.ywPrj.filePath)
        # Includes closing

    def show_status(self, message=None):
        """Display project statistics on the status bar.
        
        Extends the superclass method.
        """
        if self.ywPrj is not None and not message:
            partCount = 0
            chapterCount = 0
            sceneCount = 0
            wordCount = 0
            for chId in self.ywPrj.srtChapters:
                if self.ywPrj.chapters[chId].isUnused or self.ywPrj.chapters[chId].isTrash:
                    continue

                if self.ywPrj.chapters[chId].chType == 0 or  self.ywPrj.chapters[chId].oldType == 0:
                    for scId in self.ywPrj.chapters[chId].srtScenes:
                        if self.ywPrj.scenes[scId].isUnused:
                            continue

                        if self.ywPrj.scenes[scId].isNotesScene:
                            continue

                        if self.ywPrj.scenes[scId].isTodoScene:
                            continue

                        sceneCount += 1
                        wordCount += self.ywPrj.scenes[scId].wordCount
                if self.ywPrj.chapters[chId].chLevel == 1:
                    partCount += 1
                else:
                    chapterCount += 1
            message = f'{partCount} parts, {chapterCount} chapters, {sceneCount} scenes, {wordCount} words'
        super().show_status(message)

    #--- Methods that change the project

    def remove_custom_fields(self, event=None):
        """Remove custom fields from the yWriter file and save."""
        if self.ywPrj is not None:
            if self.ask_yes_no('Remove novelyst project settings and save?'):
                self.tv.tree.selection_set('')
                self.on_nothing_select()
                if self.ywPrj.reset_custom_variables():
                    self.set_info_how(self.ywPrj.write())

    def save_project(self, event=None):
        """Save the yWriter project to disk and set 'unchanged' status.
        
        Return True on success, otherwise return False.
        """
        if self.isLocked:
            return False

        if len(self.ywPrj.srtChapters) < 1:
            self.set_info_how(f'{ERROR}Cannot save: The project must have at least one chapter or part.')
            return False

        if self.ywPrj.is_locked():
            self.set_info_how(f'{ERROR}yWriter seems to be open. Please close first.')
            return False

        if self.ywPrj.has_changed_on_disk() and not self.ask_yes_no('File has changed on disk. Save anyway?'):
            return False

        self._elementView.apply_changes(self)
        self.ywPrj.write()
        self.show_path(f'{os.path.normpath(self.ywPrj.filePath)} (last saved on {self.ywPrj.fileDate})')
        self.isModified = False
        self.restore_status(event)
        self.kwargs['yw_last_open'] = self.ywPrj.filePath
        return True

    def new_project(self, event=None):
        """Create a yWriter project instance."""
        if self.ywPrj is not None:
            self.close_project()
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes, defaultextension='.yw7')
        if fileName:
            self.ywPrj = Yw7WorkFile(fileName)
            if self.ywPrj.title:
                titleView = self.ywPrj.title
            else:
                titleView = 'Untitled yWriter project'
            if self.ywPrj.authorName:
                authorView = self.ywPrj.authorName
            else:
                authorView = 'Unknown author'
            self.root.title(f'{titleView} by {authorView} - {self._title}')
            self.show_path(os.path.normpath(fileName))
            self.enable_menu()
            self.tv.build_tree()
            self.show_status()
            self.isModified = True

    def save_as(self, event=None):
        """Rename the yWriter file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        fileTypes = [('yWriter 7 project', '.yw7')]
        fileName = filedialog.asksaveasfilename(filetypes=fileTypes, defaultextension='.yw7')
        if fileName:
            if self.ywPrj is not None:
                self.ywPrj.filePath = fileName
                message = self.ywPrj.write()
                if message.startswith(ERROR):
                    self.set_info_how(message)
                else:
                    self.unlock()
                    self.show_path(f'{os.path.normpath(self.ywPrj.filePath)} (last saved on {self.ywPrj.fileDate})')
                    self.isModified = False
                    self.restore_status(event)
                    self.kwargs['yw_last_open'] = self.ywPrj.filePath
                    return True

        return False

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('View', state='disabled')
        self.mainMenu.entryconfig('Part', state='disabled')
        self.mainMenu.entryconfig('Chapter', state='disabled')
        self.mainMenu.entryconfig('Scene', state='disabled')
        self.mainMenu.entryconfig('Character', state='disabled')
        self.mainMenu.entryconfig('Location', state='disabled')
        self.mainMenu.entryconfig('Item', state='disabled')
        self.mainMenu.entryconfig('Export', state='disabled')

        self.fileMenu.entryconfig('Reload', state='disabled')
        self.fileMenu.entryconfig('Refresh Tree', state='disabled')
        self.fileMenu.entryconfig('Lock', state='disabled')
        self.fileMenu.entryconfig('Unlock', state='disabled')
        self.fileMenu.entryconfig('Open with yWriter', state='disabled')
        self.fileMenu.entryconfig('Open Project folder', state='disabled')
        self.fileMenu.entryconfig('Remove custom fields', state='disabled')
        self.fileMenu.entryconfig('Save', state='disabled')
        self.fileMenu.entryconfig('Save as...', state='disabled')

        for p in self._plugins:
            try:
                p.disable_menu()
            except:
                pass

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('View', state='normal')
        self.mainMenu.entryconfig('Part', state='normal')
        self.mainMenu.entryconfig('Chapter', state='normal')
        self.mainMenu.entryconfig('Scene', state='normal')
        self.mainMenu.entryconfig('Character', state='normal')
        self.mainMenu.entryconfig('Location', state='normal')
        self.mainMenu.entryconfig('Item', state='normal')
        self.mainMenu.entryconfig('Export', state='normal')

        self.fileMenu.entryconfig('Reload', state='normal')
        self.fileMenu.entryconfig('Refresh Tree', state='normal')
        self.fileMenu.entryconfig('Lock', state='normal')
        self.fileMenu.entryconfig('Open with yWriter', state='normal')
        self.fileMenu.entryconfig('Open Project folder', state='normal')
        self.fileMenu.entryconfig('Remove custom fields', state='normal')
        self.fileMenu.entryconfig('Save', state='normal')
        self.fileMenu.entryconfig('Save as...', state='normal')

        for p in self._plugins:
            try:
                p.enable_menu()
            except:
                pass

    def _build_main_menu(self):
        """Unused; overrides the superclass template method."""
