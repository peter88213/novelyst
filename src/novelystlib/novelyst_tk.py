""""Provide a tkinter GUI framework for novelyst.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from pywriter.pywriter_globals import ERROR
from pywriter.ui.main_tk import MainTk
from pywriter.file.doc_open import open_document
from novelystlib.nv_exporter import NvExporter
from novelystlib.tree_viewer import TreeViewer
from novelystlib.yw7_work_file import Yw7WorkFile
from novelystlib.element_view import ElementView
from novelystlib.project_view import ProjectView
from novelystlib.chapter_view import ChapterView
from novelystlib.scene_view import SceneView


class NovelystTk(MainTk):
    """A tkinter GUI class for yWriter tree view.

    Public methods:
        open_project -- Create a yWriter project instance and read the file.
        save_project -- Save the yWriter project to disk and set 'unchanged' status.
        on_quit(event=None) -- Save keyword arguments before exiting the program.
        on_nothing-select -- Event handler for invalid tree selection.
        on_narrative_select -- Event handler for novel tree root selection.
        on_chapter_select -- Event handler for chapter selection.
        on_scene_select -- Event handler for scene selection.
        on_character_select -- Event handler for character selection.
        on_location_select -- Event handler for location selection.
        on_item_select -- Event handler for item selection.
        show_status -- Display project statistics on the status bar.

    Public instance variables:
        isModified -- bool: ywPrj has unsaved modification (property with geter and setter).
        isLocked -- bool: ywPrj must not be modified (property with geter and setter).
        treeWindow -- tk window for the project tree.
        tv -- TreeViewer instance.
    """
    _KEY_NEW_PROJECT = ('<Control-n>', 'Ctrl-N')
    _KEY_LOCK_PROJECT = ('<Control-l>', 'Ctrl-L')
    _KEY_UNLOCK_PROJECT = ('<Control-u>', 'Ctrl-U')
    _KEY_YWRITER = ('<Control-Alt-y>', 'Ctrl-Alt-Y')
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
            color_locked_bg -- str: tk color name for Footer background when locked.
            color_locked_fg -- str: tk color name for Footer foreground when locked.
            color_modified_bg -- str: tk color name for Footer background when modified.
            color_modified_fg -- str: tk color name for Footer foreground when modified.
    
        Extends the superclass constructor.
        """
        self.kwargs = kwargs
        super().__init__(colTitle, **kwargs)
        rootWidth = int(kwargs['root_geometry'].split('x', maxsplit=1)[0])
        self._chapterMenu = None
        self._sceneMenu = None
        self._internalModificationFlag = False
        self._internalLockFlag = False
        self._exporter = NvExporter(self)

        # Create an application window with a tree frame and a data frame.
        self._appWindow = tk.PanedWindow(self._mainWindow, sashrelief=tk.RAISED)
        self._appWindow.pack(expand=True, fill='both')
        self._treeFrame = tk.Frame(self._appWindow)
        kw = {'width':kwargs['tree_frame_width']}
        self._appWindow.add(self._treeFrame, **kw)
        self._dataFrame = tk.Frame(self._appWindow)
        self._appWindow.add(self._dataFrame, minsize=350)

        # Create a novel tree window.
        self.treeWindow = tk.PanedWindow(self._treeFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.treeWindow.pack(expand=True, fill='both')
        self.tv = TreeViewer(self, self.treeWindow, **kwargs)

        #--- Create a data window.
        self._dataWindow = tk.PanedWindow(self._dataFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._dataWindow.pack(expand=True, fill='both')

        # Place a title label inside the data window.
        self.elementTitle = tk.StringVar(value='')
        self._titleLabel = tk.Entry(bd=0, textvariable=self.elementTitle, relief=tk.FLAT)
        self._dataWindow.add(self._titleLabel)

        # Place a description window inside the data window.
        self.descWindow = scrolledtext.ScrolledText(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=20, width=10, padx=5, pady=5)
        self._dataWindow.add(self.descWindow, minsize=350)

        # Place a values window inside the data window.
        self._valuesWindow = tk.Frame()
        self._dataWindow.add(self._valuesWindow, minsize=350)

        # Place a notes window inside the data window.
        self.notesWindow = scrolledtext.ScrolledText(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=4, width=10, padx=5, pady=5, bg=self._COLOR_NOTE_WINDOWS)
        self._dataWindow.add(self.notesWindow)

        self._elementView = ElementView(self, None)
        # Requires windows and frames initialized

        #--- Build the main menu

        # Files
        self._fileMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='File', underline=0, menu=self._fileMenu)
        self._fileMenu.add_command(label='New', underline=0, accelerator=self._KEY_NEW_PROJECT[1], command=self._new_project)
        self._fileMenu.add_command(label='Open...', underline=0, accelerator=self._KEY_OPEN_PROJECT[1], command=lambda: self.open_project(''))
        self._fileMenu.add_command(label='Lock', underline=0, accelerator=self._KEY_LOCK_PROJECT[1], command=self._lock)
        self._fileMenu.add_command(label='Unlock', underline=0, accelerator=self._KEY_UNLOCK_PROJECT[1], command=self._unlock)
        self._fileMenu.add_command(label='Open with yWriter', underline=10, accelerator=self._KEY_YWRITER[1], command=self._yWriter)
        self._fileMenu.add_command(label='Refresh Tree', underline=8, accelerator=self._KEY_REFRESH_TREE[1], command=self._refresh_tree)
        self._fileMenu.add_command(label='Reload', underline=0, accelerator=self._KEY_RELOAD_PROJECT[1], command=self._reload_project)
        self._fileMenu.add_command(label='Save', underline=0, accelerator=self._KEY_SAVE_PROJECT[1], command=self.save_project)
        self._fileMenu.add_command(label='Save as...', underline=5, accelerator=self._KEY_SAVE_AS[1], command=self._save_as)
        self._fileMenu.add_command(label='Close', underline=0, command=self._close_project)
        self._fileMenu.add_command(label='Exit', underline=1, accelerator=self._KEY_QUIT_PROGRAM[1], command=self.on_quit)

        # View
        self._viewMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='View', menu=self._viewMenu)
        self._viewMenu.add_command(label="Expand selected", underline=0, command=lambda: self.tv.open_children(self.tv.tree.selection()[0]))
        self._viewMenu.add_command(label="Collapse selected", underline=0, command=lambda: self.tv.close_children(self.tv.tree.selection()[0]))
        self._viewMenu.add_command(label="Expand all", underline=1, command=lambda: self.tv.open_children(''))
        self._viewMenu.add_command(label="Collapse all", underline=1, command=lambda: self.tv.close_children(''))

        # Part
        self._partMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Part', menu=self._partMenu)
        self._partMenu.add_command(label='Add', underline=0, command=self.tv.add_part)
        self._partMenu.add_separator()
        self._partMenu.add_command(label='Export part descriptions for editing', underline=12, command=lambda: self._exporter.run(self.ywPrj, '_parts'))

        # Chapter
        self._chapterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Chapter', menu=self._chapterMenu)
        self._chapterMenu.add_command(label='Add', underline=0, command=self.tv.add_chapter)
        self._chapterMenu.add_separator()
        self._chapterMenu.add_command(label='Export chapter descriptions for editing', underline=15, command=lambda: self._exporter.run(self.ywPrj, '_chapters'))

        # Scene
        self._sceneMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Scene', menu=self._sceneMenu)
        self._sceneMenu.add_command(label='Add', underline=0, command=self.tv.add_scene)
        self._sceneMenu.add_separator()
        self._sceneMenu.add_command(label='Export scene descriptions for editing', underline=13, command=lambda: self._exporter.run(self.ywPrj, '_scenes'))
        self._sceneMenu.add_command(label='Export scene list (spreadsheet)', underline=13, command=lambda: self._exporter.run(self.ywPrj, '_scenelist'))

        # Character
        self._characterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Character', menu=self._characterMenu)
        self._characterMenu.add_command(label='Add', underline=0, command=lambda: self.tv.add_world_element(self.tv.CR_ROOT))
        self._characterMenu.add_separator()
        self._characterMenu.add_command(label='Export character descriptions for editing', underline=17, command=lambda: self._exporter.run(self.ywPrj, '_characters'))
        self._characterMenu.add_command(label='Export character list (spreadsheet)', underline=17, command=lambda: self._exporter.run(self.ywPrj, '_charlist'))

        # Location
        self._locationMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Location', menu=self._locationMenu)
        self._locationMenu.add_command(label='Add', underline=0, command=lambda: self.tv.add_world_element(self.tv.LC_ROOT))
        self._locationMenu.add_separator()
        self._locationMenu.add_command(label='Export location descriptions for editing', underline=16, command=lambda: self._exporter.run(self.ywPrj, '_locations'))
        self._locationMenu.add_command(label='Export location list (spreadsheet)', underline=16, command=lambda: self._exporter.run(self.ywPrj, '_loclist'))

        # Item
        self._itemMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Item', menu=self._itemMenu)
        self._itemMenu.add_command(label='Add', underline=0, command=lambda: self.tv.add_world_element(self.tv.IT_ROOT))
        self._itemMenu.add_separator()
        self._itemMenu.add_command(label='Export item descriptions for editing', underline=12, command=lambda: self._exporter.run(self.ywPrj, '_items'))
        self._itemMenu.add_command(label='Export item list (spreadsheet)', underline=12, command=lambda: self._exporter.run(self.ywPrj, '_itemlist'))

        # Export
        self._exportMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Export', menu=self._exportMenu)
        self._exportMenu.add_command(label='Manuscript for editing', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_manuscript'))
        self._exportMenu.add_command(label='Notes chapters for editing', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_notes'))
        self._exportMenu.add_separator()
        self._exportMenu.add_command(label='Manuscript with visible structure tags for proof reading', underline=43, command=lambda: self._exporter.run(self.ywPrj, '_proof'))
        self._exportMenu.add_separator()
        self._exportMenu.add_command(label='Manuscript without tags (export only)', underline=25, command=lambda: self._exporter.run(self.ywPrj, ''))
        self._exportMenu.add_command(label='Brief synopsis (export only)', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_brf_synopsis'))
        self._exportMenu.add_command(label='Cross references (export only)', underline=0, command=lambda: self._exporter.run(self.ywPrj, '_xref'))

        self._disable_menu()

        #--- Event bindings.
        self.root.bind(self._KEY_NEW_PROJECT[0], self._new_project)
        self.root.bind(self._KEY_LOCK_PROJECT[0], self._lock)
        self.root.bind(self._KEY_UNLOCK_PROJECT[0], self._unlock)
        self.root.bind(self._KEY_RELOAD_PROJECT[0], self._reload_project)
        self.root.bind(self._KEY_YWRITER[0], self._yWriter)
        self.root.bind(self._KEY_REFRESH_TREE[0], self._refresh_tree)
        self.root.bind(self._KEY_SAVE_PROJECT[0], self.save_project)
        self.root.bind(self._KEY_SAVE_AS[0], self._save_as)

    @property
    def isModified(self):
        return self._internalModificationFlag

    @isModified.setter
    def isModified(self, setFlag):
        if setFlag:
            self._internalModificationFlag = True
            self._pathBar.config(bg=self.kwargs['color_modified_bg'])
            self._pathBar.config(fg=self.kwargs['color_modified_fg'])
        else:
            self._internalModificationFlag = False
            if not self.isLocked:
                self._pathBar.config(bg=self.root.cget('background'))
                self._pathBar.config(fg='black')

    @property
    def isLocked(self):
        return self._internalLockFlag

    @isLocked.setter
    def isLocked(self, setFlag):
        if setFlag and not self._internalLockFlag:
            if self.isModified:
                if self.ask_yes_no('Save and lock?'):
                    self.save_project()
                else:
                    return

            self._internalLockFlag = True
            self._fileMenu.entryconfig('Save', state='disabled')
            self._fileMenu.entryconfig('Lock', state='disabled')
            self._fileMenu.entryconfig('Unlock', state='normal')
            self._pathBar.config(bg=self.kwargs['color_locked_bg'])
            self._pathBar.config(fg=self.kwargs['color_locked_fg'])
        elif self._internalLockFlag:
            self._internalLockFlag = False
            self._fileMenu.entryconfig('Save', state='normal')
            self._fileMenu.entryconfig('Lock', state='normal')
            self._fileMenu.entryconfig('Unlock', state='disabled')
            self._pathBar.config(bg=self.root.cget('background'))
            self._pathBar.config(fg='black')

    def _lock(self, event=None):
        if self.ywPrj.filePath is not None:
            self.isLocked = True
            # actually, this is a setter method with conditions
            if self.isLocked:
                self.ywPrj.lock()
                # make it persistent

    def _unlock(self, event=None):
        self.isLocked = False
        self.ywPrj.unlock()
        # make it persistent
        if self.ywPrj.has_changed_on_disk():
            if self.ask_yes_no(f'File has changed on disk. Reload?'):
                self.open_project(self.ywPrj.filePath)

    def _yWriter(self, event=None):
        self.save_project()
        self._lock()
        open_document(self.ywPrj.filePath)

    def on_quit(self, event=None):
        """Save keyword arguments before exiting the program.."""
        self._close_project()
        self.kwargs['tree_frame_width'] = self._treeFrame.winfo_width()
        # save windows size and position
        self.tv.on_quit(self.kwargs)
        super().on_quit()

    def on_nothing_select(self):
        """Event handler for invalid tree selection."""
        self._elementView.close(self)
        self._elementView = ElementView(self, None)

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
        self._elementView = SceneView(self, self.ywPrj.scenes[scId])

    def on_character_select(self, crId):
        """Event handler for character selection."""
        self._elementView.close(self)
        self._elementView = ElementView(self, self.ywPrj.characters[crId])

    def on_location_select(self, lcId):
        """Event handler for location selection."""
        self._elementView.close(self)
        self._elementView = ElementView(self, self.ywPrj.locations[lcId])

    def on_item_select(self, itId):
        """Event handler for item selection."""
        self._change_selection(self.ywPrj.items[itId])
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

        self._show_path(f'{os.path.normpath(self.ywPrj.filePath)} (last saved on {self.ywPrj.fileDate})')
        self.tv.build_tree()
        self.show_status()
        self.isModified = False
        if self.ywPrj.has_lockfile():
            self.isLocked = True
        return True

    def _close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        if self.isModified:
            if self.ask_yes_no('Save changes?'):
                self.save_project()
            self.isModified = False
        self.tv.reset_tree()
        self.on_nothing_select()
        self.isLocked = False
        super()._close_project()

    def _refresh_tree(self, event=None):
        self._elementView.apply_changes(self)
        self.tv.refresh_tree()

    def _reload_project(self, event=None):
        """Reload a yWriter project."""
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
        self._show_path(f'{os.path.normpath(self.ywPrj.filePath)} (last saved on {self.ywPrj.fileDate})')
        self.isModified = False
        self._restore_status(event)
        self.kwargs['yw_last_open'] = self.ywPrj.filePath
        return True

    def _new_project(self, event=None):
        """Create a yWriter project instance."""
        if self.ywPrj is not None:
            self._close_project()
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
            self._show_path(os.path.normpath(fileName))
            self._enable_menu()
            self.build_tree()
            self.show_status()
            self.isModified = True

    def _save_as(self, event=None):
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
                    self._unlock()
                    self._show_path(f'{os.path.normpath(self.ywPrj.filePath)} (last saved on {self.ywPrj.fileDate})')
                    self.isModified = False
                    self._restore_status(event)
                    self.kwargs['yw_last_open'] = self.ywPrj.filePath
                    return True

        return False

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('View', state='disabled')
        self._mainMenu.entryconfig('Part', state='disabled')
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._mainMenu.entryconfig('Scene', state='disabled')
        self._mainMenu.entryconfig('Character', state='disabled')
        self._mainMenu.entryconfig('Location', state='disabled')
        self._mainMenu.entryconfig('Item', state='disabled')
        self._mainMenu.entryconfig('Export', state='disabled')

        self._fileMenu.entryconfig('Lock', state='disabled')
        self._fileMenu.entryconfig('Unlock', state='disabled')
        self._fileMenu.entryconfig('Open with yWriter', state='disabled')
        self._fileMenu.entryconfig('Refresh Tree', state='disabled')
        self._fileMenu.entryconfig('Reload', state='disabled')
        self._fileMenu.entryconfig('Save', state='disabled')
        self._fileMenu.entryconfig('Save as...', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('View', state='normal')
        self._mainMenu.entryconfig('Part', state='normal')
        self._mainMenu.entryconfig('Chapter', state='normal')
        self._mainMenu.entryconfig('Scene', state='normal')
        self._mainMenu.entryconfig('Character', state='normal')
        self._mainMenu.entryconfig('Location', state='normal')
        self._mainMenu.entryconfig('Item', state='normal')
        self._mainMenu.entryconfig('Export', state='normal')

        self._fileMenu.entryconfig('Lock', state='normal')
        self._fileMenu.entryconfig('Open with yWriter', state='normal')
        self._fileMenu.entryconfig('Refresh Tree', state='normal')
        self._fileMenu.entryconfig('Reload', state='normal')
        self._fileMenu.entryconfig('Save', state='normal')
        self._fileMenu.entryconfig('Save as...', state='normal')

    def _build_main_menu(self):
        """Unused; overrides the superclass template method."""
