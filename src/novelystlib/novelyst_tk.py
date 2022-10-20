""""Provide a tkinter GUI framework for novelyst.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pywriter.pywriter_globals import *
from pywriter.ui.main_tk import MainTk
from pywriter.ui.set_icon_tk import *
from novelystlib.contents_viewer import ContentsViewer
from novelystlib.converter.nv_exporter import NvExporter
from novelystlib.converter.nv_reporter import NvReporter
from novelystlib.files.yw7_work_file import Yw7WorkFile
from novelystlib.plugin_collection import PluginCollection
from novelystlib.tree_viewer import TreeViewer
from novelystlib.views.no_view import NoView
from novelystlib.views.basic_view import BasicView
from novelystlib.views.world_element_view import WorldElementView
from novelystlib.views.project_view import ProjectView
from novelystlib.views.chapter_view import ChapterView
from novelystlib.views.scene_view import SceneView
from novelystlib.views.notes_scene_view import NotesSceneView
from novelystlib.views.todo_scene_view import TodoSceneView
from novelystlib.views.character_view import CharacterView
from novelystlib.widgets.text_box import TextBox
from novelystlib.widgets.settings_window import SettingsWindow
from novelystlib.widgets.plugin_manager import PluginManager

PLUGIN_PATH = f'{sys.path[0]}/plugin'


class NovelystTk(MainTk):
    """Controller of the tkinter GUI framework for novelyst."""
    _HELP_URL = 'https://peter88213.github.io/novelyst/usage'
    _KEY_NEW_PROJECT = ('<Control-n>', 'Ctrl-N')
    _KEY_LOCK_PROJECT = ('<Control-l>', 'Ctrl-L')
    _KEY_UNLOCK_PROJECT = ('<Control-u>', 'Ctrl-U')
    _KEY_FOLDER = ('<Control-p>', 'Ctrl-P')
    _KEY_RELOAD_PROJECT = ('<Control-r>', 'Ctrl-R')
    _KEY_REFRESH_TREE = ('<F5>', 'F5')
    _KEY_SAVE_PROJECT = ('<Control-s>', 'Ctrl-S')
    _KEY_SAVE_AS = ('<Control-S>', 'Ctrl-Shift-S')
    _KEY_CHAPTER_LEVEL = ('<Control-Alt-c>', 'Ctrl-Alt-C')
    _KEY_TOGGLE_VIEWER = ('<Control-t>', 'Ctrl-T')

    _YW_CLASS = Yw7WorkFile
    _COLOR_NOTE_WINDOWS = 'lemon chiffon'

    def __init__(self, colTitle, tempDir, **kwargs):
        """Put a text box to the GUI main window.
        
        Required keyword arguments:
            root_geometry -- str: geometry of the root window.
            middle_frame_width -- int: width of the chapter frame.
            right_frame_width -- int: width of the data frame.
            color_locked_bg -- str: tk color name for Footer background when locked.
            color_locked_fg -- str: tk color name for Footer foreground when locked.
            color_modified_bg -- str: tk color name for Footer background when modified.
            color_modified_fg -- str: tk color name for Footer foreground when modified.
    
        Public instance variables:
            guiStyle -- ttk.Style object.
            plugins -- PluginCollection: Dict-like Container for registered plugin objects.
            tempDir -- str: Directory path for temporary files to be deleted on exit.
            kwargs - dict: keyword arguments, used as global configuration data.
            wordCount - int: Total words of "normal" type scenes.
            reloading -- boolean: If True, suppress popup message when reopening a project that has changed on disk.
            appWindow
            leftFrame
            middleFrame
            rightFrame
            tv
            contentsViewer
            indexCard
            elementTitle
            descWindow
            infoFrame
            notesWindow
            fileMenu
            viewMenu
            partMenu
            chapterMenu
            sceneMenu
            characterMenu
            locationMenu
            itemMenu
            prjNoteMenu
            exportMenu
            toolsMenu
            helpMenu
            
    
        Extends the superclass constructor.
        """
        super().__init__(colTitle, **kwargs)
        set_icon(self.root, icon='nLogo32')

        # Initialize GUI theme.
        self.guiStyle = ttk.Style()

        self.plugins = PluginCollection(self)
        # Dict-like Container for registered plugin objects.

        self.tempDir = tempDir
        self.kwargs = kwargs
        self._internalModificationFlag = False
        self._internalLockFlag = False
        self._exporter = NvExporter(self)
        self._reporter = NvReporter(self)
        self.wordCount = 0
        self.reloading = False

        # Create an application window with three frames.
        self.appWindow = ttk.Frame(self.mainWindow)
        self.appWindow.pack(expand=True, fill=tk.BOTH)
        self.leftFrame = ttk.Frame(self.appWindow)
        self.leftFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.middleFrame = ttk.Frame(self.appWindow, width=self.kwargs['middle_frame_width'])
        self.middleFrame.pack_propagate(0)
        self.middleFrame.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        self.rightFrame = ttk.Frame(self.appWindow, width=kwargs['right_frame_width'])
        self.rightFrame.pack_propagate(0)
        self.rightFrame.pack(expand=True, fill=tk.BOTH)

        # Create a novel tree window.
        self.tv = TreeViewer(self.leftFrame, self, kwargs)
        self.tv.pack(expand=True, fill=tk.BOTH)

        # Create a text viewer in the middle frame.
        self.contentsViewer = ContentsViewer(self, self.middleFrame)

        # Create an "index card" in the right frame.
        self.indexCard = tk.Frame(self.rightFrame, bd=2, relief=tk.RIDGE)
        self.indexCard.pack(expand=False, fill=tk.BOTH)

        # Title label.
        self.elementTitle = tk.StringVar(value='')
        tk.Entry(self.indexCard, bd=0, textvariable=self.elementTitle, relief=tk.FLAT).pack(fill=tk.X, ipady=6)

        tk.Frame(self.indexCard, bg='red', height=1, bd=0).pack(fill=tk.X)
        tk.Frame(self.indexCard, bg='white', height=1, bd=0).pack(fill=tk.X)

        # Description window.
        self.descWindow = TextBox(self.indexCard, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=15, width=10, padx=5, pady=5)
        self.descWindow.pack(fill=tk.X)

        # Frame for element specific informations.
        self.infoFrame = ttk.Frame(self.rightFrame)
        self.infoFrame.pack(expand=True, fill=tk.BOTH)

        # Notes window.
        self.notesWindow = TextBox(self.rightFrame, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=4, width=10, padx=5, pady=5, bg=self._COLOR_NOTE_WINDOWS)
        self.notesWindow.pack(expand=True, fill=tk.BOTH)

        # Initialize element views.
        self._noView = NoView(self)
        self._basicView = BasicView(self)
        self._projectView = ProjectView(self)
        self._chapterView = ChapterView(self)
        self._todoSceneView = TodoSceneView(self)
        self._notesSceneView = NotesSceneView(self)
        self._sceneView = SceneView(self)
        self._characterView = CharacterView(self)
        self._worldElementView = WorldElementView(self)

        self._elementView = self._basicView
        self._elementView.set_data(None)
        # Requires windows and frames initialized

        #--- Build the main menu

        # Files
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('File'), menu=self.fileMenu)
        self.fileMenu.add_command(label=_('New'), accelerator=self._KEY_NEW_PROJECT[1], command=self.new_project)
        self.fileMenu.add_command(label=_('Open...'), accelerator=self._KEY_OPEN_PROJECT[1], command=lambda: self.open_project(''))
        self.fileMenu.add_command(label=_('Reload'), accelerator=self._KEY_RELOAD_PROJECT[1], command=self.reload_project)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Refresh Tree'), accelerator=self._KEY_REFRESH_TREE[1], command=self.refresh_tree)
        self.fileMenu.add_command(label=_('Lock'), accelerator=self._KEY_LOCK_PROJECT[1], command=self.lock)
        self.fileMenu.add_command(label=_('Unlock'), accelerator=self._KEY_UNLOCK_PROJECT[1], command=self.unlock)
        self.fileMenu.add_command(label=_('Open Project folder'), accelerator=self._KEY_FOLDER[1], command=self.open_projectFolder)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Save'), accelerator=self._KEY_SAVE_PROJECT[1], command=self.save_project)
        self.fileMenu.add_command(label=_('Save as...'), accelerator=self._KEY_SAVE_AS[1], command=self.save_as)
        self.fileMenu.add_command(label=_('Remove custom fields'), command=self.remove_custom_fields)
        self.fileMenu.add_command(label=_('Close'), command=self.close_project)
        self.fileMenu.add_command(label=_('Exit'), accelerator=self._KEY_QUIT_PROGRAM[1], command=self.on_quit)

        # View
        self.viewMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('View'), menu=self.viewMenu)
        self.viewMenu.add_command(label=_('Chapter level'), accelerator=self._KEY_CHAPTER_LEVEL[1], command=self.show_chapter_level)
        self.viewMenu.add_command(label=_('Expand selected'), command=lambda: self.tv.open_children(self.tv.tree.selection()[0]))
        self.viewMenu.add_command(label=_('Collapse selected'), command=lambda: self.tv.close_children(self.tv.tree.selection()[0]))
        self.viewMenu.add_command(label=_('Expand all'), command=lambda: self.tv.open_children(''))
        self.viewMenu.add_command(label=_('Collapse all'), command=lambda: self.tv.close_children(''))
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label=_('Toggle "Contents" window'), accelerator=self._KEY_TOGGLE_VIEWER[1], command=self.toggle_viewer)

        # Part
        self.partMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Part'), menu=self.partMenu)
        self.partMenu.add_command(label=_('Add'), command=self.tv.add_part)
        self.partMenu.add_separator()
        self.partMenu.add_command(label=_('Export part descriptions for editing'), command=lambda: self._export_document('_parts'))

        # Chapter
        self.chapterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Chapter'), menu=self.chapterMenu)
        self.chapterMenu.add_command(label=_('Add'), command=self.tv.add_chapter)
        self.chapterMenu.add_separator()
        self.chapterMenu.add_command(label=_('Export chapter descriptions for editing'), command=lambda: self._export_document('_chapters'))

        # Scene
        self.sceneMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Scene'), menu=self.sceneMenu)
        self.sceneMenu.add_command(label=_('Add'), command=self.tv.add_scene)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_cascade(label=_('Set Type'), menu=self.tv.scTypeMenu)
        self.sceneMenu.add_cascade(label=_('Set Status'), menu=self.tv.scStatusMenu)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_cascade(label=_('Set Style'), menu=self.tv.scStyleMenu)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_command(label=_('Export scene descriptions for editing'), command=lambda: self._export_document('_scenes'))
        self.sceneMenu.add_command(label=_('Export scene list (spreadsheet)'), command=lambda: self._export_document('_scenelist'))

        # Character
        self.characterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Characters'), menu=self.characterMenu)
        self.characterMenu.add_command(label=_('Add'), command=lambda: self.tv.add_other_element(self.tv.CR_ROOT))
        self.characterMenu.add_separator()
        self.characterMenu.add_cascade(label=_('Set Status'), menu=self.tv.crStatusMenu)
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label=_('Export character descriptions for editing'), command=lambda: self._export_document('_characters'))
        self.characterMenu.add_command(label=_('Export character list (spreadsheet)'), command=lambda: self._export_document('_charlist'))
        self.characterMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_character_report'))

        # Location
        self.locationMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Locations'), menu=self.locationMenu)
        self.locationMenu.add_command(label=_('Add'), command=lambda: self.tv.add_other_element(self.tv.LC_ROOT))
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Export location descriptions for editing'), command=lambda: self._export_document('_locations'))
        self.locationMenu.add_command(label=_('Export location list (spreadsheet)'), command=lambda: self._export_document('_loclist'))
        self.locationMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_location_report'))

        # Item
        self.itemMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Items'), menu=self.itemMenu)
        self.itemMenu.add_command(label=_('Add'), command=lambda: self.tv.add_other_element(self.tv.IT_ROOT))
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label=_('Export item descriptions for editing'), command=lambda: self._export_document('_items'))
        self.itemMenu.add_command(label=_('Export item list (spreadsheet)'), command=lambda: self._export_document('_itemlist'))
        self.itemMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_item_report'))

        # Project notes
        self.prjNoteMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Project notes'), menu=self.prjNoteMenu)
        self.prjNoteMenu.add_command(label=_('Add'), command=lambda: self.tv.add_other_element(self.tv.PN_ROOT))
        self.prjNoteMenu.add_separator()
        self.prjNoteMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_projectnote_report'))

        # Export
        self.exportMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Export'), menu=self.exportMenu)
        self.exportMenu.add_command(label=_('Manuscript for editing'), command=lambda: self._export_document('_manuscript'))
        self.exportMenu.add_command(label=_('Notes chapters for editing'), command=lambda: self._export_document('_notes'))
        self.exportMenu.add_command(label=_('Todo chapters for editing'), command=lambda: self._export_document('_todo'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript with visible structure tags for proof reading'), command=lambda: self._export_document('_proof'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript without tags (export only)'), command=lambda: self._export_document('', lock=False))
        self.exportMenu.add_command(label=_('Brief synopsis (export only)'), command=lambda: self._export_document('_brf_synopsis', lock=False))
        self.exportMenu.add_command(label=_('Cross references (export only)'), command=lambda: self._export_document('_xref', lock=False))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Obfuscated text for word count'), command=lambda: self._export_document('_wrimo', lock=False, show=False))
        self.exportMenu.add_command(label=_('Characters/locations/items data files'), command=lambda: self._export_document('_data', lock=False, show=False))

        # Tools
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Tools'), menu=self.toolsMenu)
        self.toolsMenu.add_command(label=_('Program settings'), command=self.edit_settings)
        self.toolsMenu.add_command(label=_('Plugin Manager'), command=self.manage_plugins)

        # Help
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        self.plugins.load_plugins(PLUGIN_PATH)
        self.disable_menu()

        #--- Event bindings.
        self.root.bind(self._KEY_NEW_PROJECT[0], self.new_project)
        self.root.bind(self._KEY_LOCK_PROJECT[0], self.lock)
        self.root.bind(self._KEY_UNLOCK_PROJECT[0], self.unlock)
        self.root.bind(self._KEY_RELOAD_PROJECT[0], self.reload_project)
        self.root.bind(self._KEY_FOLDER[0], self.open_projectFolder)
        self.root.bind(self._KEY_REFRESH_TREE[0], self.refresh_tree)
        self.root.bind(self._KEY_SAVE_PROJECT[0], self.save_project)
        self.root.bind(self._KEY_SAVE_AS[0], self.save_as)
        self.root.bind(self._KEY_CHAPTER_LEVEL[0], self.show_chapter_level)
        self.root.bind(self._KEY_TOGGLE_VIEWER[0], self.toggle_viewer)

    @property
    def isModified(self):
        return self._internalModificationFlag

    @isModified.setter
    def isModified(self, setFlag):
        if setFlag:
            self.contentsViewer.update()
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
                if self.ask_yes_no(_('Save and lock?')):
                    self.save_project()
                else:
                    return

            self._internalLockFlag = True
            self.pathBar.config(bg=self.kwargs['color_locked_bg'])
            self.pathBar.config(fg=self.kwargs['color_locked_fg'])
            self.fileMenu.entryconfig(_('Save'), state='disabled')
            self.fileMenu.entryconfig(_('Lock'), state='disabled')
            self.fileMenu.entryconfig(_('Unlock'), state='normal')
        else:
            self._internalLockFlag = False
            self.pathBar.config(bg=self.root.cget('background'))
            self.pathBar.config(fg='black')
            self.fileMenu.entryconfig(_('Save'), state='normal')
            self.fileMenu.entryconfig(_('Lock'), state='normal')
            self.fileMenu.entryconfig(_('Unlock'), state='disabled')

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
            if self.ask_yes_no(_('File has changed on disk. Reload?')):
                self.open_project(self.ywPrj.filePath)

    def toggle_viewer(self, event=None):
        if self.middleFrame.winfo_manager():
            self.middleFrame.pack_forget()
        else:
            self.middleFrame.pack(after=self.leftFrame, side=tk.LEFT, expand=False, fill=tk.BOTH)

    def open_projectFolder(self, event=None):
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
        """Save keyword arguments before exiting the program."""
        try:
            self.close_project()

            # save contents window "show markup" state.
            self.kwargs['show_markup'] = self.contentsViewer.showMarkup.get()

            # save contents window toggle state.
            if self.middleFrame.winfo_manager():
                self.kwargs['show_contents'] = True
            else:
                self.kwargs['show_contents'] = False

            # save windows size and position
            self.tv.on_quit(self.kwargs)
            super().on_quit()
        except Exception as ex:
            messagebox.showerror('ERROR: Unhandled exception on exit', str(ex))
            self.root.quit()

    def view_nothing(self):
        """Event handler for invalid tree selection."""
        if not self._elementView is self._noView:
            self._elementView.apply_changes()
            self._elementView.hide()
            self._elementView = self._noView
            self._elementView.show(None)

    def view_narrative(self):
        """Event handler for narrative tree root selection."""
        self._elementView.apply_changes()
        if not self._elementView is self._projectView:
            self._elementView.hide()
            self._elementView = self._projectView
            self._elementView.show(self.ywPrj)
        self._elementView.set_data(self.ywPrj)

    def view_chapter(self, chId):
        """Event handler for chapter selection."""
        self._elementView.apply_changes()
        if not self._elementView is self._chapterView:
            self._elementView.hide()
            self._elementView = self._chapterView
            self._elementView.show(self.ywPrj.chapters[chId])
        self._elementView.set_data(self.ywPrj.chapters[chId])
        self.contentsViewer.see(f'ch{chId}')

    def view_scene(self, scId):
        """Event handler for scene selection."""
        self._elementView.apply_changes()
        if self.ywPrj.scenes[scId].scType == 2:
            if not self._elementView is self._todoSceneView:
                self._elementView.hide()
                self._elementView = self._todoSceneView
                self._elementView.show(self.ywPrj.scenes[scId])
            self._elementView.set_data(self.ywPrj.scenes[scId])
        elif self.ywPrj.scenes[scId].scType == 1:
            if not self._elementView is self._notesSceneView:
                self._elementView.hide()
                self._elementView = self._notesSceneView
                self._elementView.show(self.ywPrj.scenes[scId])
            self._elementView.set_data(self.ywPrj.scenes[scId])
        else:
            if not self._elementView is self._sceneView:
                self._elementView.hide()
                self._elementView = self._sceneView
                self._elementView.show(self.ywPrj.scenes[scId])
            self._elementView.set_data(self.ywPrj.scenes[scId])
        self.contentsViewer.see(f'sc{scId}')

    def view_character(self, crId):
        """Event handler for character selection."""
        self._elementView.apply_changes()
        if not self._elementView is self._characterView:
            self._elementView.hide()
            self._elementView = self._characterView
            self._elementView.show(self.ywPrj.characters[crId])
        self._elementView.set_data(self.ywPrj.characters[crId])

    def view_location(self, lcId):
        """Event handler for location selection."""
        self._elementView.apply_changes()
        if not self._elementView is self._worldElementView:
            self._elementView.hide()
            self._elementView = self._worldElementView
            self._elementView.show(self.ywPrj.locations[lcId])
        self._elementView.set_data(self.ywPrj.locations[lcId])

    def view_item(self, itId):
        """Event handler for item selection."""
        self._elementView.apply_changes()
        if not self._elementView is self._worldElementView:
            self._elementView.hide()
            self._elementView = self._worldElementView
            self._elementView.show(self.ywPrj.items[itId])
        self._elementView.set_data(self.ywPrj.items[itId])

    def view_projectNote(self, pnId):
        """Event handler for project note selection."""
        self._elementView.apply_changes()
        if not self._elementView is self._basicView:
            self._elementView.hide()
            self._elementView = self._basicView
            self._elementView.show(self.ywPrj.projectNotes[pnId])
        self._elementView.set_data(self.ywPrj.projectNotes[pnId])

    def refresh_tree(self, event=None):
        """Apply changes and refresh the tree."""
        self._elementView.apply_changes()
        self.tv.refresh_tree()

    def reload_project(self, event=None):
        """Discard changes and reload the project."""
        if self.ywPrj.is_locked():
            self.set_info_how(f'{ERROR}{_("yWriter seems to be open. Please close first")}.')
            return

        if self.isModified and not self.ask_yes_no(_('Discard changes and reload the project?')):
            return

        if self.ywPrj.has_changed_on_disk() and not self.ask_yes_no(_('File has changed on disk. Reload anyway?')):
            return

        self.reloading = True
        # This is to avoid another question when closing the project
        self.open_project(self.ywPrj.filePath)
        # Includes closing

    def show_status(self, message=None):
        """Display project statistics on the status bar.
        
        Extends the superclass method.
        """
        if self.ywPrj is not None and not message:
            wordCount, sceneCount, chapterCount, partCount = self.ywPrj.get_counts()
            message = _('{0} parts, {1} chapters, {2} scenes, {3} words').format(partCount, chapterCount, sceneCount, wordCount)
            self.wordCount = wordCount
        super().show_status(message)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig(_('View'), state='disabled')
        self.mainMenu.entryconfig(_('Part'), state='disabled')
        self.mainMenu.entryconfig(_('Chapter'), state='disabled')
        self.mainMenu.entryconfig(_('Scene'), state='disabled')
        self.mainMenu.entryconfig(_('Characters'), state='disabled')
        self.mainMenu.entryconfig(_('Locations'), state='disabled')
        self.mainMenu.entryconfig(_('Items'), state='disabled')
        self.mainMenu.entryconfig(_('Export'), state='disabled')
        self.mainMenu.entryconfig(_('Project notes'), state='disabled')

        self.fileMenu.entryconfig(_('Reload'), state='disabled')
        self.fileMenu.entryconfig(_('Refresh Tree'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.fileMenu.entryconfig(_('Open Project folder'), state='disabled')
        self.fileMenu.entryconfig(_('Remove custom fields'), state='disabled')
        self.fileMenu.entryconfig(_('Save'), state='disabled')
        self.fileMenu.entryconfig(_('Save as...'), state='disabled')

        self.plugins.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig(_('View'), state='normal')
        self.mainMenu.entryconfig(_('Part'), state='normal')
        self.mainMenu.entryconfig(_('Chapter'), state='normal')
        self.mainMenu.entryconfig(_('Scene'), state='normal')
        self.mainMenu.entryconfig(_('Characters'), state='normal')
        self.mainMenu.entryconfig(_('Locations'), state='normal')
        self.mainMenu.entryconfig(_('Items'), state='normal')
        self.mainMenu.entryconfig(_('Export'), state='normal')
        self.mainMenu.entryconfig(_('Project notes'), state='normal')

        self.fileMenu.entryconfig(_('Reload'), state='normal')
        self.fileMenu.entryconfig(_('Refresh Tree'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='normal')
        self.fileMenu.entryconfig(_('Open Project folder'), state='normal')
        self.fileMenu.entryconfig(_('Remove custom fields'), state='normal')
        self.fileMenu.entryconfig(_('Save'), state='normal')
        self.fileMenu.entryconfig(_('Save as...'), state='normal')

        self.plugins.enable_menu()

    def show_chapter_level(self, event=None):
        self.tv.show_chapters(self.tv.NV_ROOT)

    def _build_main_menu(self):
        """Unused; overrides the superclass template method."""

    #--- Methods that change the project

    def remove_custom_fields(self, event=None):
        """Remove custom fields from the .yw7 file and save."""
        if self.ywPrj is not None:
            if self.ask_yes_no(_('Remove novelyst project settings and save?')):
                self.tv.tree.selection_set('')
                self.view_nothing()
                if self.ywPrj.reset_custom_variables():
                    self.set_info_how(self.ywPrj.write())

    def open_project(self, fileName=''):
        """Create a novelyst project instance and read the file.
        
        Display project title, description and status.
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        if not super().open_project(fileName):
            return False

        self.show_path(_('{0} (last saved on {1})').format(os.path.normpath(self.ywPrj.filePath), self.ywPrj.fileDate))
        self.tv.build_tree()
        self.show_status()
        self.contentsViewer.view_text()
        self.isModified = False
        if self.ywPrj.has_lockfile():
            self.isLocked = True
        return True

    def new_project(self, event=None):
        """Create a novelyst project instance."""
        if self.ywPrj is not None:
            self.close_project()
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes, defaultextension='.yw7')
        if fileName:
            self.ywPrj = Yw7WorkFile(fileName)
            self.set_title()
            self.show_path(os.path.normpath(fileName))
            self.enable_menu()
            self.tv.build_tree()
            self.show_status()
            self.isModified = True

    def close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        self.contentsViewer.reset_view()
        self.plugins.on_quit()

        self.view_nothing()
        # this closes the current element view after checking for modifications
        if self.isModified and not self.reloading:
            if self.ask_yes_no(_('Save changes?')):
                self.save_project()
        self.tv.reset_tree()
        # this removes all children from the tree
        self.isModified = False
        self.reloading = False
        self.isLocked = False
        super().close_project()

    def save_project(self, event=None):
        """Save the novelyst project to disk and set 'unchanged' status.
        
        Return True on success, otherwise return False.
        """
        if self.isLocked:
            return False

        if len(self.ywPrj.srtChapters) < 1:
            self.set_info_how(f'{ERROR}{_("Cannot save: The project must have at least one chapter or part")}.')
            return False

        if self.ywPrj.is_locked():
            self.set_info_how(f'{ERROR}{_("yWriter seems to be open. Please close first")}.')
            return False

        if self.ywPrj.has_changed_on_disk() and not self.ask_yes_no(_('File has changed on disk. Save anyway?')):
            return False

        self._elementView.apply_changes()
        self.ywPrj.write()
        self.show_path(f'{os.path.normpath(self.ywPrj.filePath)} ({_("last saved on")} {self.ywPrj.fileDate})')
        self.isModified = False
        self.restore_status(event)
        self.kwargs['yw_last_open'] = self.ywPrj.filePath
        return True

    def save_as(self, event=None):
        """Rename the .yw7 file and save it to disk.
        
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
                    self.show_path(f'{os.path.normpath(self.ywPrj.filePath)} ({_("last saved on")} {self.ywPrj.fileDate})')
                    self.isModified = False
                    self.restore_status(event)
                    self.kwargs['yw_last_open'] = self.ywPrj.filePath
                    return True

        return False

    def edit_settings(self, event=None):
        """Open a toplevel window to edit the program settings."""
        offset = 300
        __, x, y = self.root.geometry().split('+')
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        SettingsWindow(self.tv, self, windowGeometry)

    def manage_plugins(self, event=None):
        """Open a toplevel window to manage the plugins."""
        offset = 300
        __, x, y = self.root.geometry().split('+')
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        PluginManager(self, windowGeometry)

    def _export_document(self, suffix, **kwargs):
        self._elementView.apply_changes()
        self._exporter.run(self.ywPrj, suffix, **kwargs)

    def _show_report(self, suffix):
        self._elementView.apply_changes()
        self._reporter.run(self.ywPrj, suffix)

