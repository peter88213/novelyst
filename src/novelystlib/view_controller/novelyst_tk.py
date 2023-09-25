"""Provide a tkinter GUI framework for novelyst.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import webbrowser
from tkinter import ttk
from tkinter import filedialog
from pywriter.pywriter_globals import *
from pywriter.model.novel import Novel
from pywriter.ui.main_tk import MainTk
from pywriter.ui.set_icon_tk import *
from novelystlib.model.work_file import WorkFile
from novelystlib.plugin.plugin_collection import PluginCollection
from novelystlib.view_controller.left_frame.tree_viewer import TreeViewer
from novelystlib.view_controller.middle_frame.contents_viewer import ContentsViewer
from novelystlib.view_controller.right_frame.basic_view import BasicView
from novelystlib.view_controller.right_frame.world_element_view import WorldElementView
from novelystlib.view_controller.right_frame.project_view import ProjectView
from novelystlib.view_controller.right_frame.chapter_view import ChapterView
from novelystlib.view_controller.right_frame.todo_chapter_view import TodoChapterView
from novelystlib.view_controller.right_frame.normal_scene_view import NormalSceneView
from novelystlib.view_controller.right_frame.notes_scene_view import NotesSceneView
from novelystlib.view_controller.right_frame.todo_scene_view import TodoSceneView
from novelystlib.view_controller.right_frame.character_view import CharacterView
from novelystlib.view_controller.right_frame.projectnote_view import ProjectnoteView
from novelystlib.view_controller.pop_up.settings_window import SettingsWindow
from novelystlib.view_controller.pop_up.plugin_manager import PluginManager
from novelystlib.export.nv_doc_exporter import NvDocExporter
from novelystlib.export.nv_reporter import NvReporter
from novelystlib.data_reader.character_data_reader import CharacterDataReader
from novelystlib.data_reader.location_data_reader import LocationDataReader
from novelystlib.data_reader.item_data_reader import ItemDataReader
from novelystlib.view_controller.pop_up.data_importer import DataImporter

PLUGIN_PATH = f'{sys.path[0]}/plugin'


class NovelystTk(MainTk):
    """Controller of the tkinter GUI framework for novelyst.
    
    Public methods:
        check_lock() -- Show a message and return True, if the project is locked.
        close_project(event) -- Close the current project.
        detach_properties_frame(event) -- View the properties in its own window.
        disable_menu() -- Disable menu entries when no project is open.
        discard_manuscript() -- Rename the current editable manuscript. 
        dock_properties_frame(event) -- Dock the properties window at the right pane, if detached.
        edit_settings(event) -- Open a toplevel window to edit the program settings.
        enable_menu() -- Enable menu entries when a project is open.
        export_document(suffix) -- Export a document.
        import_characters() -- Import characters from an XML data file.
        import_locations() -- Import locations from an XML data file.
        import_items() -- Import items from an XML data file.
        lock(event) -- Lock the project.
        manage_plugins(event) -- Open a toplevel window to manage the plugins.
        new_project(event) -- Create a novelyst project instance.
        on_quit(event) -- Save keyword arguments before exiting the program.
        open_installation_folder(event) -- Open the installation folder with the OS file manager.
        open_project(fileName='') -- Create a novelyst project instance and read the file.
        open_project_folder(event) -- Open the project folder with the OS file manager.
        refresh_tree(event) -- Apply changes and refresh the tree.
        reload_project(event) -- Discard changes and reload the project.
        restore_backup(event) -- Discard changes and restore the latest backup file.
        save_as(event) -- Rename the project file and save it to disk.
        save_project(event) -- Save the novelyst project to disk and set "unchanged" status.
        show_chapter_level(event) -- Open all Book/Part nodes and close all chapter nodes in the tree viewer.
        show_properties() -- Show the properties of the selected element.
        show_status(message=None) -- Display project statistics at the status bar.
        toggle_lock(event) -- Toggle the 'locked' status.
        toggle_viewer(event) -- Show/hide the contents viewer text box.
        toggle_properties(event) -- Show/hide the element properties frame.
        toggle_properties_window(event) -- Detach/dock the element properties frame.
        unlock(event) -- Unlock the project.
        view_chapter(chId) -- Show the selected chapter's properties; move to it in the content viewer.
        view_character(crId) -- Show the selected character's properties.
        view_item(itId) -- Show the selected item's properties.
        view_location(lcId) -- Show the selected location's properties.
        view_narrative() -- Show the project's properties.
        view_nothing() -- Reset properties if nothing valid is selected.
        view_projectNote(pnId) -- Show the selected project note.
        view_scene(scId) -- Show the selected scene's properties; move to it in the content viewer.
        
    Public instance variables:
        guiStyle -- ttk.Style object.
        plugins: PluginCollection -- Dict-like Container for registered plugin objects.
        tempDir: str -- Directory path for temporary files to be deleted on exit.
        kwargs: dict -- keyword arguments, used as global configuration data.
        exporter: NvExporter -- Converter strategy for document export. 
        reporter: NvExporter -- Converter strategy for report generation. 
        wordCount: int -- Total words of "normal" type scenes.
        reloading: bool -- If True, suppress popup message when reopening a project that has changed on disk.
        prjFile: WorkFile
        novel: Novel
        coloringMode: int -- Scene row coloring mode indicating a COLORING_MODES item.
        cleanUpYw: bool -- If True, delete yWriter-only data on saving the project.
        appWindow: ttk.frame -- Application window with three frames.
        leftFrame: ttk.frame -- Frame for the project tree.
        tv: TreeViewer -- Project tree view instance.
        middleFrame: ttk.frame -- Frame for the contents viewer.
        contentsViewer: ContentsViewer -- Text box for the novel contents.
        fileMenu: tk.Menu -- "File" menu.
        viewMenu: tk.Menu -- "View" menu.
        partMenu: tk.Menu -- "Part" menu.
        chapterMenu: tk.Menu -- "Chapter" menu.
        sceneMenu: tk.Menu -- "Scene" menu.
        characterMenu: tk.Menu -- "Character" menu.
        locationMenu: tk.Menu -- "Location" menu.
        itemMenu: tk.Menu -- "Item" menu.
        prjNoteMenu: tk.Menu -- "Project notes" menu.
        exportMenu: tk.Menu -- "Export" menu.
        toolsMenu: tk.Menu -- "Tools" menu.
        helpMenu: tk.Menu -- "Help" menu.   
        rightFrame: ttk.frame -- Frame for the metadata views.
        
    Public properties:
        isModified: Boolean -- True if there are unsaved changes.
        isLocked: Boolean -- True if a lock file exists for the current project.  
        
    Public class constants:
        COLORING_MODES: List[str] -- Scene row coloring modes.
    """
    COLORING_MODES = [_('None'), _('Status'), _('Work phase'), _('Mode')]
    _HELP_URL = 'https://peter88213.github.io/novelyst/help/help'
    _KEY_NEW_PROJECT = ('<Control-n>', 'Ctrl-N')
    _KEY_LOCK_PROJECT = ('<Control-l>', 'Ctrl-L')
    _KEY_UNLOCK_PROJECT = ('<Control-u>', 'Ctrl-U')
    _KEY_FOLDER = ('<Control-p>', 'Ctrl-P')
    _KEY_RELOAD_PROJECT = ('<Control-r>', 'Ctrl-R')
    _KEY_RESTORE_BACKUP = ('<Control-b>', 'Ctrl-B')
    _KEY_REFRESH_TREE = ('<F5>', 'F5')
    _KEY_SAVE_PROJECT = ('<Control-s>', 'Ctrl-S')
    _KEY_SAVE_AS = ('<Control-S>', 'Ctrl-Shift-S')
    _KEY_CHAPTER_LEVEL = ('<Control-Alt-c>', 'Ctrl-Alt-C')
    _KEY_TOGGLE_VIEWER = ('<Control-t>', 'Ctrl-T')
    _KEY_TOGGLE_PROPERTIES = ('<Control-Alt-t>', 'Ctrl-Alt-T')
    _KEY_DETACH_PROPERTIES = ('<Control-Alt-d>', 'Ctrl-Alt-D')
    _KEY_GO_BACK = ('<F2>', 'F2')
    _KEY_GO_FORWARD = ('<F3>', 'F3')
    _KEY_SHOW_BOOK = ('<F6>', 'F6')
    _KEY_SHOW_CHARACTERS = ('<F7>', 'F7')
    _KEY_SHOW_LOCATIONS = ('<F8>', 'F8')
    _KEY_SHOW_ITEMS = ('<F9>', 'F9')
    _KEY_SHOW_RESEARCH = ('<F10>', 'F10')
    _KEY_SHOW_PLANNING = ('<F11>', 'F11')
    _KEY_SHOW_PROJECTNOTES = ('<F12>', 'F12')
    _KEY_SHOW_HELP = ('<F1>', 'F1')

    _YW_CLASS = WorkFile

    def __init__(self, colTitle, tempDir, **kwargs):
        """Load plugins and set up the application's user interface.
        
        Required keyword arguments:
            root_geometry: str -- geometry of the root window.
            middle_frame_width: int -- width of the chapter frame.
            right_frame_width: int -- width of the data frame.
            color_locked_bg: str -- tk color name for Footer background when locked.
            color_locked_fg: str -- tk color name for Footer foreground when locked.
            color_modified_bg: str -- tk color name for Footer background when modified.
            color_modified_fg: str -- tk color name for Footer foreground when modified.
            color_text_bg: str -- tk color name for text box background.
            color_text_fg: str -- tk color name for text box foreground.
            coloring_mode: int -- Scene row coloring mode.
    
        Extends the superclass constructor.
        """
        super().__init__(colTitle, **kwargs)

        set_icon(self.root, icon='nLogo32')
        self._fileTypes = [(WorkFile.DESCRIPTION, WorkFile.EXTENSION)]

        # Initialize GUI theme.
        self.guiStyle = ttk.Style()

        self.plugins = PluginCollection(self)
        # Dict-like Container for registered plugin objects.

        self.tempDir = tempDir
        self.kwargs = kwargs
        self._internalModificationFlag = False
        self._internalLockFlag = False
        self.exporter = NvDocExporter(self)
        self.reporter = NvReporter(self)
        self.wordCount = 0
        self.reloading = False
        self.prjFile = None
        self.novel = None

        # Scene coloring mode.
        try:
            self.coloringMode = int(self.kwargs['coloring_mode'])
        except:
            self.coloringMode = 0
        if self.coloringMode > len(self.COLORING_MODES):
            self.coloringMode = 0

        # "Delete yWriter-only data on save" state.
        self.cleanUpYw = self.kwargs['clean_up_yw']

        #--- Build the GUI frames.

        # Create an application window with three frames.
        self.appWindow = ttk.Frame(self.mainWindow)
        self.appWindow.pack(expand=True, fill='both')

        #--- left frame (intended for the tree).
        self.leftFrame = ttk.Frame(self.appWindow)
        self.leftFrame.pack(side='left', expand=True, fill='both')

        # Create a novel tree window.
        self.tv = TreeViewer(self.leftFrame, self, self.kwargs)
        self.tv.pack(expand=True, fill='both')

        #--- Middle frame (intended for the content viewer).
        self.middleFrame = ttk.Frame(self.appWindow, width=self.kwargs['middle_frame_width'])
        self.middleFrame.pack_propagate(0)

        # Create a text viewer in the middle frame.
        self.contentsViewer = ContentsViewer(self, self.middleFrame, **self.kwargs)
        if self.kwargs['show_contents']:
            self.middleFrame.pack(side='left', expand=False, fill='both')

        #--- Build the main menu
        # Requires windows and frames initialized

        # Files
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('File'), menu=self.fileMenu)
        self.fileMenu.add_command(label=_('New'), accelerator=self._KEY_NEW_PROJECT[1], command=self.new_project)
        self.fileMenu.add_command(label=_('Open...'), accelerator=self._KEY_OPEN_PROJECT[1], command=self.open_project)
        self.fileMenu.add_command(label=_('Reload'), accelerator=self._KEY_RELOAD_PROJECT[1], command=self.reload_project)
        self.fileMenu.add_command(label=_('Restore backup'), accelerator=self._KEY_RESTORE_BACKUP[1], command=self.restore_backup)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Refresh Tree'), accelerator=self._KEY_REFRESH_TREE[1], command=self.refresh_tree)
        self.fileMenu.add_command(label=_('Lock'), accelerator=self._KEY_LOCK_PROJECT[1], command=self.lock)
        self.fileMenu.add_command(label=_('Unlock'), accelerator=self._KEY_UNLOCK_PROJECT[1], command=self.unlock)
        self.fileMenu.add_command(label=_('Open Project folder'), accelerator=self._KEY_FOLDER[1], command=self.open_projectFolder)
        self.fileMenu.add_command(label=_('Discard manuscript'), command=self.discard_manuscript)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Save'), accelerator=self._KEY_SAVE_PROJECT[1], command=self.save_project)
        self.fileMenu.add_command(label=_('Save as...'), accelerator=self._KEY_SAVE_AS[1], command=self.save_as)
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
        self.viewMenu.add_command(label=_('Show Book'), accelerator=self._KEY_SHOW_BOOK[1], command=lambda: self.tv.show_branch(self.tv.NV_ROOT))
        self.viewMenu.add_command(label=_('Show Characters'), accelerator=self._KEY_SHOW_CHARACTERS[1], command=lambda: self.tv.show_branch(self.tv.CR_ROOT))
        self.viewMenu.add_command(label=_('Show Locations'), accelerator=self._KEY_SHOW_LOCATIONS[1], command=lambda: self.tv.show_branch(self.tv.LC_ROOT))
        self.viewMenu.add_command(label=_('Show Items'), accelerator=self._KEY_SHOW_ITEMS[1], command=lambda: self.tv.show_branch(self.tv.IT_ROOT))
        self.viewMenu.add_command(label=_('Show Research'), accelerator=self._KEY_SHOW_RESEARCH[1], command=lambda: self.tv.show_branch(self.tv.RS_ROOT))
        self.viewMenu.add_command(label=_('Show Planning'), accelerator=self._KEY_SHOW_PLANNING[1], command=lambda: self.tv.show_branch(self.tv.PL_ROOT))
        self.viewMenu.add_command(label=_('Show Project notes'), accelerator=self._KEY_SHOW_PROJECTNOTES[1], command=lambda: self.tv.show_branch(self.tv.PN_ROOT))
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label=_('Toggle Text viewer'), accelerator=self._KEY_TOGGLE_VIEWER[1], command=self.toggle_viewer)
        self.viewMenu.add_command(label=_('Toggle Properties'), accelerator=self._KEY_TOGGLE_PROPERTIES[1], command=self.toggle_properties)
        self.viewMenu.add_command(label=_('Detach/Dock Properties'), accelerator=self._KEY_DETACH_PROPERTIES[1], command=self.toggle_properties_window)

        # Part
        self.partMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Part'), menu=self.partMenu)
        self.partMenu.add_command(label=_('Add'), command=self.tv.add_part)
        self.partMenu.add_separator()
        self.partMenu.add_command(label=_('Export part descriptions for editing'), command=lambda: self.export_document('_parts'))

        # Chapter
        self.chapterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Chapter'), menu=self.chapterMenu)
        self.chapterMenu.add_command(label=_('Add'), command=self.tv.add_chapter)
        self.chapterMenu.add_separator()
        self.chapterMenu.add_command(label=_('Export chapter descriptions for editing'), command=lambda: self.export_document('_chapters'))

        # Scene
        self.sceneMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Scene'), menu=self.sceneMenu)
        self.sceneMenu.add_command(label=_('Add'), command=self.tv.add_scene)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_cascade(label=_('Set Type'), menu=self.tv.scTypeMenu)
        self.sceneMenu.add_cascade(label=_('Set Status'), menu=self.tv.scStatusMenu)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_cascade(label=_('Set Mode'), menu=self.tv.scStyleMenu)
        self.sceneMenu.add_separator()
        self.sceneMenu.add_command(label=_('Export scene descriptions for editing'), command=lambda: self.export_document('_scenes'))
        self.sceneMenu.add_command(label=_('Export scene list (spreadsheet)'), command=lambda: self.export_document('_scenelist'))

        # Character
        self.characterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Characters'), menu=self.characterMenu)
        self.characterMenu.add_command(label=_('Add'), command=self.tv.add_character)
        self.characterMenu.add_separator()
        self.characterMenu.add_cascade(label=_('Set Status'), menu=self.tv.crStatusMenu)
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label=_('Import'), command=self.import_characters)
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label=_('Export character descriptions for editing'), command=lambda: self.export_document('_characters'))
        self.characterMenu.add_command(label=_('Export character list (spreadsheet)'), command=lambda: self.export_document('_charlist'))
        self.characterMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_character_report'))

        # Location
        self.locationMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Locations'), menu=self.locationMenu)
        self.locationMenu.add_command(label=_('Add'), command=self.tv.add_location)
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Import'), command=self.import_locations)
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Export location descriptions for editing'), command=lambda: self.export_document('_locations'))
        self.locationMenu.add_command(label=_('Export location list (spreadsheet)'), command=lambda: self.export_document('_loclist'))
        self.locationMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_location_report'))

        # Item
        self.itemMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Items'), menu=self.itemMenu)
        self.itemMenu.add_command(label=_('Add'), command=self.tv.add_item)
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label=_('Import'), command=self.import_items)
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label=_('Export item descriptions for editing'), command=lambda: self.export_document('_items'))
        self.itemMenu.add_command(label=_('Export item list (spreadsheet)'), command=lambda: self.export_document('_itemlist'))
        self.itemMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_item_report'))

        # Project notes
        self.prjNoteMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Project notes'), menu=self.prjNoteMenu)
        self.prjNoteMenu.add_command(label=_('Add'), command=self.tv.add_project_note)
        self.prjNoteMenu.add_separator()
        self.prjNoteMenu.add_command(label=_('Show list'), command=lambda: self._show_report('_projectnote_report'))

        # Export
        self.exportMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Export'), menu=self.exportMenu)
        self.exportMenu.add_command(label=_('Manuscript for editing'), command=lambda:self.export_document('_manuscript'))
        self.exportMenu.add_command(label=_('Notes chapters for editing'), command=lambda: self.export_document('_notes'))
        self.exportMenu.add_command(label=_('Todo chapters for editing'), command=lambda: self.export_document('_todo'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript with visible structure tags for proof reading'), command=lambda: self.export_document('_proof'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript without tags (export only)'), command=lambda: self.export_document('', lock=False))
        self.exportMenu.add_command(label=_('Brief synopsis (export only)'), command=lambda: self.export_document('_brf_synopsis', lock=False))
        self.exportMenu.add_command(label=_('Cross references (export only)'), command=lambda: self.export_document('_xref', lock=False))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Obfuscated text for word count'), command=lambda: self.export_document('_wrimo', lock=False, show=False))
        self.exportMenu.add_command(label=_('Characters/locations/items data files'), command=lambda: self.export_document('_data', lock=False, show=False))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Plot description (export only)'), command=lambda: self.export_document('_plot', lock=False))
        self.exportMenu.add_command(label=_('Plot spreadsheet (export only)'), command=lambda: self.export_document('_plotlist', lock=False))
        self.exportMenu.add_command(label=_('Show Plot list'), command=lambda: self._show_report('_plotlist'))

        # Tools
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Tools'), menu=self.toolsMenu)
        self.toolsMenu.add_command(label=_('Program settings'), command=self.edit_settings)
        self.toolsMenu.add_command(label=_('Plugin Manager'), command=self.manage_plugins)
        self.toolsMenu.add_command(label=_('Open installation folder'), command=self.open_installationFolder)
        self.toolsMenu.add_separator()

        # Help
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), accelerator=self._KEY_SHOW_HELP[1], command=lambda: webbrowser.open(self._HELP_URL))

        self.plugins.load_plugins(PLUGIN_PATH)
        self.disable_menu()

        #--- Right frame (intended for the element properties pane).
        self.rightFrame = ttk.Frame(self.appWindow, width=self.kwargs['right_frame_width'])
        self.rightFrame.pack_propagate(0)
        if self.kwargs['show_properties']:
            self.rightFrame.pack(expand=True, fill='both')
        self._initialize_properties_frame(self.rightFrame)
        self._propWinDetached = False
        if self.kwargs['detach_prop_win']:
            self.detach_properties_frame()

        #--- Event bindings.
        self.root.bind(self._KEY_NEW_PROJECT[0], self.new_project)
        self.root.bind(self._KEY_LOCK_PROJECT[0], self.lock)
        self.root.bind(self._KEY_UNLOCK_PROJECT[0], self.unlock)
        self.root.bind(self._KEY_RELOAD_PROJECT[0], self.reload_project)
        self.root.bind(self._KEY_RESTORE_BACKUP[0], self.restore_backup)
        self.root.bind(self._KEY_FOLDER[0], self.open_projectFolder)
        self.root.bind(self._KEY_REFRESH_TREE[0], self.refresh_tree)
        self.root.bind(self._KEY_SAVE_PROJECT[0], self.save_project)
        self.root.bind(self._KEY_SAVE_AS[0], self.save_as)
        self.root.bind(self._KEY_CHAPTER_LEVEL[0], self.show_chapter_level)
        self.root.bind(self._KEY_TOGGLE_VIEWER[0], self.toggle_viewer)
        self.root.bind(self._KEY_TOGGLE_PROPERTIES[0], self.toggle_properties)
        self.root.bind(self._KEY_DETACH_PROPERTIES[0], self.toggle_properties_window)
        self.root.bind(self._KEY_GO_BACK[0], self.tv.go_back)
        self.root.bind(self._KEY_GO_FORWARD[0], self.tv.go_forward)
        if sys.platform == 'win32':
            self.root.bind('<4>', self.tv.go_back)
            self.root.bind('<5>', self.tv.go_forward)
        self.root.bind(self._KEY_SHOW_BOOK[0], lambda event: self.tv.show_branch(self.tv.NV_ROOT))
        self.root.bind(self._KEY_SHOW_CHARACTERS[0], lambda event: self.tv.show_branch(self.tv.CR_ROOT))
        self.root.bind(self._KEY_SHOW_LOCATIONS[0], lambda event: self.tv.show_branch(self.tv.LC_ROOT))
        self.root.bind(self._KEY_SHOW_ITEMS[0], lambda event: self.tv.show_branch(self.tv.IT_ROOT))
        self.root.bind(self._KEY_SHOW_RESEARCH[0], lambda event: self.tv.show_branch(self.tv.RS_ROOT))
        self.root.bind(self._KEY_SHOW_PLANNING[0], lambda event: self.tv.show_branch(self.tv.PL_ROOT))
        self.root.bind(self._KEY_SHOW_PROJECTNOTES[0], lambda event: self.tv.show_branch(self.tv.PN_ROOT))
        self.root.bind(self._KEY_SHOW_HELP[0], lambda event: webbrowser.open(self._HELP_URL))

        #--- Get applications for opening linked non-standard filetypes.
        self.applications = {}
        for k in kwargs:
            if k.startswith('launch'):
                try:
                    __, ext = k.split('_')
                except:
                    pass
                else:
                    self.applications[f'.{ext}'] = kwargs[k]

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

    def check_lock(self):
        """Show a message and return True, if the project is locked."""
        if self.isLocked:
            if self.ask_yes_no(_('The project is locked.\nUnlock?'), title=_('Can not do')):
                self.unlock()
                return False

            else:
                return True
        else:
            return False

    def close_project(self, event=None):
        """Close the current project.
        
        - Save changes
        - clear all views
        - reset flags
        - trigger plugins.
        
        Extends the superclass method.
        """
        self._elementView.apply_changes()
        self.contentsViewer.reset_view()
        self.plugins.on_close()

        # this closes the current element view after checking for modifications
        if self.isModified and not self.reloading:
            if self.ask_yes_no(_('Save changes?')):
                self.save_project()
        self.isModified = False
        self.view_nothing()
        self.tv.reset_tree()
        # this removes all children from the tree
        self.reloading = False
        self.isLocked = False
        self.novel = None
        super().close_project()

    def detach_properties_frame(self, event=None):
        """View the properties in its own window."""
        self._elementView.apply_changes()
        if self._propWinDetached:
            return

        if self.rightFrame.winfo_manager():
            self.rightFrame.pack_forget()
        self._propertiesWindow = tk.Toplevel()
        self._propertiesWindow.geometry(self.kwargs['prop_win_geometry'])
        set_icon(self._propertiesWindow, icon='pLogo32', default=False)
        self._elementView.pack_forget()
        self._initialize_properties_frame(self._propertiesWindow)
        self._elementView.pack()
        self.show_properties()
        self._propertiesWindow.protocol("WM_DELETE_WINDOW", self.dock_properties_frame)
        self.kwargs['detach_prop_win'] = True
        self._propWinDetached = True

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
        self.fileMenu.entryconfig(_('Restore backup'), state='disabled')
        self.fileMenu.entryconfig(_('Refresh Tree'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.fileMenu.entryconfig(_('Open Project folder'), state='disabled')
        self.fileMenu.entryconfig(_('Save'), state='disabled')
        self.fileMenu.entryconfig(_('Save as...'), state='disabled')
        self.fileMenu.entryconfig(_('Discard manuscript'), state='disabled')

        self.plugins.disable_menu()

    def discard_manuscript(self):
        """Rename the current editable manuscript. 
        
        This might be useful to avoid confusion in certain cases.
        """
        fileName, __ = os.path.splitext(self.prjFile.filePath)
        manuscriptPath = f'{fileName}_manuscript.odt'
        if os.path.isfile(manuscriptPath):
            prjPath, manuscriptName = os.path.split(manuscriptPath)
            if os.path.isfile(f'{prjPath}/.~lock.{manuscriptName}#'):
                self.set_info_how(f"!{_('Please close the manuscript first')}.")
            elif self.ask_yes_no(f"{_('Discard manuscript')}?", self.novel.title):
                os.replace(manuscriptPath, f'{fileName}_manuscript.odt.bak')
                self.set_info_how(f"{_('Manuscript discarded')}.")

    def dock_properties_frame(self, event=None):
        """Dock the properties window at the right pane, if detached."""
        self._elementView.apply_changes()
        if not self._propWinDetached:
            return

        self._initialize_properties_frame(self.rightFrame)
        if not self.rightFrame.winfo_manager():
            self.rightFrame.pack(side='left', expand=False, fill='both')
        self._elementView.pack()
        self.show_properties()
        self.kwargs['prop_win_geometry'] = self._propertiesWindow.winfo_geometry()
        self._propertiesWindow.destroy()
        self.kwargs['show_properties'] = True
        self.kwargs['detach_prop_win'] = False
        self._propWinDetached = False
        self.root.lift()

    def edit_settings(self, event=None):
        """Open a toplevel window to edit the program settings."""
        offset = 300
        __, x, y = self.root.geometry().split('+')
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        SettingsWindow(self.tv, self, windowGeometry)

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
        self.fileMenu.entryconfig(_('Restore backup'), state='normal')
        self.fileMenu.entryconfig(_('Refresh Tree'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='normal')
        self.fileMenu.entryconfig(_('Open Project folder'), state='normal')
        self.fileMenu.entryconfig(_('Save'), state='normal')
        self.fileMenu.entryconfig(_('Save as...'), state='normal')
        self.fileMenu.entryconfig(_('Discard manuscript'), state='normal')

        self.plugins.enable_menu()

    def export_document(self, suffix, **kwargs):
        """Export a document.
        
        Required arguments:
            suffix -- str: Document type suffix (https://peter88213.github.io/novelyst/help/export_menu).
        """
        self.restore_status()
        self._elementView.apply_changes()
        self.exporter.run(self.prjFile, suffix, **kwargs)

    def import_characters(self):
        """Import characters from an XML data file."""
        self.restore_status()
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            source = CharacterDataReader(filePath)
            source.novel = Novel()
            try:
                source.read()
            except:
                self.set_info_how(f"!{_('No character data found')}: {norm_path(filePath)}")
            else:
                offset = 50
                size = '300x400'
                __, x, y = self.root.geometry().split('+')
                windowGeometry = f'{size}+{int(x)+offset}+{int(y)+offset}'
                DataImporter(self, _('Select characters'),
                             windowGeometry,
                             source.novel.characters,
                             self.prjFile.novel.characters,
                             self.prjFile.novel.srtCharacters)

    def import_locations(self):
        """Import locations from an XML data file."""
        self.restore_status()
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            source = LocationDataReader(filePath)
            source.novel = Novel()
            try:
                source.read()
            except:
                self.set_info_how(f"!{_('No location data found')}: {norm_path(filePath)}")
            else:
                offset = 50
                size = '300x400'
                __, x, y = self.root.geometry().split('+')
                windowGeometry = f'{size}+{int(x)+offset}+{int(y)+offset}'
                DataImporter(self, _('Select locations'),
                             windowGeometry,
                             source.novel.locations,
                             self.prjFile.novel.locations,
                             self.prjFile.novel.srtLocations)

    def import_items(self):
        """Import items from an XML data file."""
        self.restore_status()
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            source = ItemDataReader(filePath)
            source.novel = Novel()
            try:
                source.read()
            except:
                self.set_info_how(f"!{_('No item data found')}: {norm_path(filePath)}")
            else:
                offset = 50
                size = '300x400'
                __, x, y = self.root.geometry().split('+')
                windowGeometry = f'{size}+{int(x)+offset}+{int(y)+offset}'
                DataImporter(self, _('Select items'),
                             windowGeometry,
                             source.novel.items,
                             self.prjFile.novel.items,
                             self.prjFile.novel.srtItems)

    def lock(self, event=None):
        """Lock the project."""
        if self.prjFile.filePath is not None:
            self.isLocked = True
            # actually, this is a setter method with conditions
            if self.isLocked:
                self.prjFile.lock()
                # make it persistent
                return True

        return False

    def manage_plugins(self, event=None):
        """Open a toplevel window to manage the plugins."""
        offset = 300
        __, x, y = self.root.geometry().split('+')
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        PluginManager(self, windowGeometry)

    def new_project(self, event=None):
        """Create a novelyst project instance."""
        if self.prjFile is not None:
            self.close_project()
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes, defaultextension=self._fileTypes[0][1])
        if fileName:
            self.prjFile = WorkFile(fileName)
            self.novel = Novel()
            self.novel.title = ''
            self.novel.authorName = ''
            self.novel.authorBio = ''
            self.novel.desc = ''
            self.novel.wordCountStart = 0
            self.novel.wordTarget = 0
            self.prjFile.novel = self.novel
            self.set_title()
            self.show_path(norm_path(fileName))
            self.enable_menu()
            self.tv.build_tree()
            self.show_status()
            self.isModified = True

            #--- Initialize custom keyword variables.
            for fieldName in self.prjFile.PRJ_KWVAR:
                self.novel.kwVar[fieldName] = None
            self.novel.kwVar['Field_WorkPhase'] = 1

    def on_quit(self, event=None):
        """Save changes and keyword arguments before exiting the program."""
        try:
            # Save properties.
            self._elementView.apply_changes()

            # Save changes.
            self.close_project()
            self.plugins.on_quit()

            # Save contents window "show markup" state.
            self.kwargs['show_markup'] = self.contentsViewer.showMarkup.get()

            # Save "Delete yWriter-only data on save" state.
            self.kwargs['clean_up_yw'] = self.cleanUpYw

            # Save scene coloring mode.
            self.kwargs['coloring_mode'] = self.coloringMode

            # Save windows size and position.
            if self._propWinDetached:
                self.kwargs['prop_win_geometry'] = self._propertiesWindow.winfo_geometry()
            self.tv.on_quit()
            super().on_quit()
        except Exception as ex:
            self.show_error(str(ex), title='ERROR: Unhandled exception on exit')
            self.root.quit()

    def open_installationFolder(self, event=None):
        """Open the installation folder with the OS file manager."""
        installDir = os.path.dirname(sys.argv[0])
        try:
            os.startfile(norm_path(installDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(installDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(installDir))
                    # Mac
                except:
                    pass

    def open_project(self, fileName=''):
        """Create a novelyst project instance and read the file.
        
        Display project title, description and status.
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        if not super().open_project(fileName):
            return False

        self.show_path(_('{0} (last saved on {1})').format(norm_path(self.prjFile.filePath), self.prjFile.fileDate))
        self.tv.build_tree()
        self.show_status()
        self.contentsViewer.view_text()
        if self.prjFile.wcLogUpdate and self.novel.kwVar.get('Field_SaveWordCount', False):
            self.isModified = True
        else:
            self.isModified = False
        if self.prjFile.has_lockfile():
            self.isLocked = True
        return True

    def open_projectFolder(self, event=None):
        """Open the project folder with the OS file manager."""
        projectDir, __ = os.path.split(self.prjFile.filePath)
        try:
            os.startfile(norm_path(projectDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(projectDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(projectDir))
                    # Mac
                except:
                    pass

    def refresh_tree(self, event=None):
        """Apply changes and refresh the tree."""
        self._elementView.apply_changes()
        self.tv.refresh_tree()

    def reload_project(self, event=None):
        """Discard changes and reload the project."""
        if self.prjFile.is_locked():
            self.set_info_how(f'!{_("yWriter seems to be open. Please close first")}.')
            return

        if self.isModified and not self.ask_yes_no(_('Discard changes and reload the project?')):
            return

        if self.prjFile.has_changed_on_disk() and not self.ask_yes_no(_('File has changed on disk. Reload anyway?')):
            return

        self.reloading = True
        # This is to avoid another question when closing the project
        self.open_project(self.prjFile.filePath)
        # Includes closing

    def restore_backup(self, event=None):
        """Discard changes and restore the latest backup file."""
        latestBackup = f'{self.prjFile.filePath}.bak'
        if not os.path.isfile(latestBackup):
            self.set_info_how(f'!{_("No backup available")}')
            return

        if self.isModified:
            if not self.ask_yes_no(_('Discard changes and restore the latest backup?')):
                return

        elif not self.ask_yes_no(_('Restore the latest backup?')):
            return

        try:
            os.replace(latestBackup, self.prjFile.filePath)
        except Exception as ex:
            self.set_info_how(str(ex))
            return

        self.reloading = True
        # This is to avoid another question when closing the project
        self.open_project(self.prjFile.filePath)
        # Includes closing

    def save_as(self, event=None):
        """Rename the project file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes, defaultextension=self._fileTypes[0][1])
        if fileName:
            if self.prjFile is not None:
                self.prjFile.filePath = fileName
                try:
                    self.prjFile.write()
                except Error as ex:
                    self.set_info_how(f'!{str(ex)}')
                else:
                    self.unlock()
                    self.show_path(f'{norm_path(self.prjFile.filePath)} ({_("last saved on")} {self.prjFile.fileDate})')
                    self.isModified = False
                    self.restore_status()
                    self.kwargs['yw_last_open'] = self.prjFile.filePath
                    return True

        return False

    def save_project(self, event=None):
        """Save the novelyst project to disk and set "unchanged" status.
        
        Return True on success, otherwise return False.
        """
        if self.check_lock():
            self.set_info_how(f'!{_("Cannot save: The project is locked")}.')
            return False

        if self.prjFile.is_locked():
            self.set_info_how(f'!{_("yWriter seems to be open. Please close first")}.')
            return False

        if self.prjFile.has_changed_on_disk() and not self.ask_yes_no(_('File has changed on disk. Save anyway?')):
            return False

        self._elementView.apply_changes()
        try:
            if self.cleanUpYw:
                self.prjFile.tree = None
            self.prjFile.write()
        except Error as ex:
            self.set_info_how(f'!{str(ex)}')
            return False

        self.show_path(f'{norm_path(self.prjFile.filePath)} ({_("last saved on")} {self.prjFile.fileDate})')
        self.isModified = False
        self.restore_status()
        self.kwargs['yw_last_open'] = self.prjFile.filePath
        return True

    def show_chapter_level(self, event=None):
        """Open all Book/part nodes and close all chapter nodes in the tree viewer."""
        self.tv.show_chapters(self.tv.NV_ROOT)

    def show_properties(self):
        """Show the properties of the selected element."""
        try:
            nodeId = self.tv.tree.selection()[0]
            if nodeId.startswith(self.tv.SCENE_PREFIX):
                self.view_scene(nodeId[2:])
            elif nodeId.startswith(self.tv.CHAPTER_PREFIX):
                self.view_chapter(nodeId[2:])
            elif nodeId.startswith(self.tv.PART_PREFIX):
                self.view_chapter(nodeId[2:])
            elif nodeId.startswith(self.tv.NV_ROOT):
                self.view_narrative()
            elif nodeId.startswith(self.tv.CHARACTER_PREFIX):
                self.view_character(nodeId[2:])
            elif nodeId.startswith(self.tv.LOCATION_PREFIX):
                self.view_location(nodeId[2:])
            elif nodeId.startswith(self.tv.ITEM_PREFIX):
                self.view_item(nodeId[2:])
            elif nodeId.startswith(self.tv.PRJ_NOTE_PREFIX):
                self.view_projectNote(nodeId[2:])
            else:
                self.view_nothing()
        except IndexError:
            pass

    def show_status(self, message=None):
        """Display project statistics at the status bar.
        
        Extends the superclass method.
        """
        if self.prjFile is not None and not message:
            wordCount, sceneCount, chapterCount, partCount = self.prjFile.get_counts()
            message = _('{0} parts, {1} chapters, {2} scenes, {3} words').format(partCount, chapterCount, sceneCount, wordCount)
            self.wordCount = wordCount
        super().show_status(message)

    def toggle_lock(self, event=None):
        """Toggle the 'locked' status."""
        if self.isLocked:
            self.unlock()
        else:
            self.lock()

    def toggle_viewer(self, event=None):
        """Show/hide the contents viewer text box."""
        if self.middleFrame.winfo_manager():
            self.middleFrame.pack_forget()
            self.kwargs['show_contents'] = False
        else:
            self.middleFrame.pack(after=self.leftFrame, side='left', expand=False, fill='both')
            self.kwargs['show_contents'] = True

    def toggle_properties(self, event=None):
        """Show/hide the element properties frame."""
        if self.rightFrame.winfo_manager():
            self._elementView.apply_changes()
            self.rightFrame.pack_forget()
            self.kwargs['show_properties'] = False
        elif not self._propWinDetached:
            self.rightFrame.pack(side='left', expand=False, fill='both')
            self.kwargs['show_properties'] = True

    def toggle_properties_window(self, event=None):
        """Detach/dock the element properties frame."""
        if self._propWinDetached:
            self.dock_properties_frame()
        else:
            self.detach_properties_frame()

    def unlock(self, event=None):
        """Unlock the project."""
        self.isLocked = False
        self.prjFile.unlock()
        # make it persistent
        if self.prjFile.has_changed_on_disk():
            if self.ask_yes_no(_('File has changed on disk. Reload?')):
                self.open_project(self.prjFile.filePath)

    def view_chapter(self, chId):
        """Show the selected chapter's properties; move to it in the content viewer.
                
        Positional arguments:
            chId: str -- chapter ID
        """
        self._elementView.apply_changes()
        if self.novel.chapters[chId].chLevel == 0 and self.novel.chapters[chId].chType == 2:
            if not self._elementView is self._todoChapterView:
                self._elementView.hide()
                self._elementView = self._todoChapterView
                self._elementView.show()
        else:
            if not self._elementView is self._chapterView:
                self._elementView.hide()
                self._elementView = self._chapterView
                self._elementView.show()
        self._elementView.set_data(self.novel.chapters[chId])
        self.contentsViewer.see(f'ch{chId}')

    def view_character(self, crId):
        """Show the selected character's properties.
                
        Positional arguments:
            crId: str -- character ID
        """
        self._elementView.apply_changes()
        if not self._elementView is self._characterView:
            self._elementView.hide()
            self._elementView = self._characterView
            self._elementView.show()
        self._elementView.set_data(self.novel.characters[crId])

    def view_item(self, itId):
        """Show the selected item's properties.
                
        Positional arguments:
            itId: str -- item ID
        """
        self._elementView.apply_changes()
        if not self._elementView is self._worldElementView:
            self._elementView.hide()
            self._elementView = self._worldElementView
            self._elementView.show()
        self._elementView.set_data(self.novel.items[itId])

    def view_location(self, lcId):
        """Show the selected location's properties.
                
        Positional arguments:
            lcId: str -- location ID
        """
        self._elementView.apply_changes()
        if not self._elementView is self._worldElementView:
            self._elementView.hide()
            self._elementView = self._worldElementView
            self._elementView.show()
        self._elementView.set_data(self.novel.locations[lcId])

    def view_narrative(self):
        """Show the project's properties."""
        self._elementView.apply_changes()
        if not self._elementView is self._projectView:
            self._elementView.hide()
            self._elementView = self._projectView
            self._elementView.show()
        self._elementView.set_data(self.novel)

    def view_nothing(self):
        """Reset properties if nothing valid is selected."""
        if not self._elementView is self._basicView:
            self._elementView.apply_changes()
            self._elementView.hide()
            self._elementView = self._basicView
            self._elementView.show()

    def view_projectNote(self, pnId):
        """Show the selected project note.
        
        Positional arguments:
            pnId: str -- Project note ID
        """
        self._elementView.apply_changes()
        if not self._elementView is self._projectnoteView:
            self._elementView.hide()
            self._elementView = self._projectnoteView
            self._elementView.show()
        self._elementView.set_data(self.novel.projectNotes[pnId])

    def view_scene(self, scId):
        """Show the selected scene's properties; move to it in the content viewer.
                
        Positional arguments:
            scId: str -- scene ID
        """
        self._elementView.apply_changes()
        if self.novel.scenes[scId].scType == 2:
            if not self._elementView is self._todoSceneView:
                self._elementView.hide()
                self._elementView = self._todoSceneView
                self._elementView.show()
        elif self.novel.scenes[scId].scType == 1:
            if not self._elementView is self._notesSceneView:
                self._elementView.hide()
                self._elementView = self._notesSceneView
                self._elementView.show()
        else:
            if not self._elementView is self._sceneView:
                self._elementView.hide()
                self._elementView = self._sceneView
                self._elementView.show()
        self._elementView.set_data(self.novel.scenes[scId])
        self.contentsViewer.see(f'sc{scId}')

    def _build_main_menu(self):
        """Overrides the superclass template method."""
        pass

    def _initialize_properties_frame(self, parent):
        """Initialize element properties views.
        
        This method is called e.g. when detaching or docking the properties.
        """
        self._basicView = BasicView(self, parent)
        self._projectView = ProjectView(self, parent)
        self._chapterView = ChapterView(self, parent)
        self._todoChapterView = TodoChapterView(self, parent)
        self._todoSceneView = TodoSceneView(self, parent)
        self._notesSceneView = NotesSceneView(self, parent)
        self._sceneView = NormalSceneView(self, parent)
        self._characterView = CharacterView(self, parent)
        self._projectnoteView = ProjectnoteView(self, parent)
        self._worldElementView = WorldElementView(self, parent)

        self._elementView = self._basicView
        self._elementView.set_data(None)

    def _show_report(self, suffix):
        """Create HTML report for the web browser."""
        self.restore_status()
        self._elementView.apply_changes()
        self.reporter.run(self.prjFile, suffix)

