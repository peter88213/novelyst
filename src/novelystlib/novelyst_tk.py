#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter tree view.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from pywriter.pywriter_globals import ERROR
from pywriter.model.id_generator import create_id
from pywriter.ui.main_tk import MainTk
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.world_element import WorldElement
from novelystlib.nv_exporter import NvExporter
from novelystlib.yw7_work_file import Yw7WorkFile


class NovelystTk(MainTk):
    """A tkinter GUI class for yWriter tree view.

    Public methods:
        open_project -- Create a yWriter project instance and read the file.
        save_project -- Save the yWriter project to disk and set 'unchanged' status.
    """

    _COLUMNS = (
        ('Words', 'wc_width'),
        ('Status', 'status_width'),
        ('Viewpoint', 'vp_width'),
        ('Tags', 'tags_width'),
        )

    _PT = 'pt'
    # Part node ID prefix
    _CH = 'ch'
    # Chapter node ID prefix
    _SC = 'sc'
    # Scene node ID prefix
    _CR = 'cr'
    # Character node ID prefix
    _LC = 'lc'
    # Location node ID prefix
    _IT = 'it'
    # Item node ID prefix
    _NV_ROOT = 'nv'
    # Root of the Narrative subtree
    _CR_ROOT = f'wr{_CR}'
    # Root of the Characters subtree
    _LC_ROOT = f'wr{_LC}'
    # Root of the Locations subtree
    _IT_ROOT = f'wr{_IT}'
    # Root of the Items subtree

    def __init__(self, colTitle, **kwargs):
        """Put a text box to the GUI main window.
        
        Required keyword arguments:
            root_geometry -- str: geometry of the root window.
            key_restore_status -- str: "Restore Status bar" key binding.
            key_open_project -- str: "Open Project" key binding.
            key_on_quit -- str: "Exit" key binding.
            key_create_project -- str: "New" key binding.
            key_lock_project -- str: "Lock" key binding.
            key_unlock_project -- str: "Unlock" key binding.
            key_reload_project -- str: "Reload Project" key binding.
            key_save_project -- str: "Save Project" key binding.
            button_context_menu -- str: Mouse button to open the treeveiw context menu.
            tree_frame_width -- int: width of the chapter frame.
            wc_width -- int: width of the wordcount column.
            status_width -- int: width of the scene status column.
            vp_width -- int: width of the scene viewpoint column.
            tags_width -- int: width of the tags column.
            color_chapter -- str: tk color name for normal parts and chapters.
            color_unused -- str: tk color name for unused chapters and scenes.
            color_notes -- str: tk color name for "Notes" chapters and scenes.
            color_todo -- str: tk color name for "To do" chapters and scenes.
            color_major -- str: tk color name for major characters.
            color_minor -- str: tk color name for minor characters.
            color_outline -- str: tk color name for "Outline" status.
            color_draft -- str: tk color name for "Draft" status.
            color_1st_edit -- str: tk color name for "First Edit" status.
            color_2nd_edit -- str: tk color name for "Second Edit" status.
            color_done -- str: tk color name for "Done" status.
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
        self._isLocked = False
        self._trashNode = None
        self._exporter = NvExporter(self)

        # Create an application window with a tree frame and a data frame.
        self._appWindow = tk.PanedWindow(self._mainWindow, sashrelief=tk.RAISED)
        self._appWindow.pack(expand=True, fill='both')
        self._treeFrame = tk.Frame(self._appWindow)
        kw = {'width':kwargs['tree_frame_width']}
        self._appWindow.add(self._treeFrame, **kw)
        self._dataFrame = tk.Frame(self._appWindow)
        self._appWindow.add(self._dataFrame)

        # Create a novel tree window.
        self._treeWindow = tk.PanedWindow(self._treeFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._treeWindow.pack(expand=True, fill='both')

        # Create a novel tree.
        self._tree = ttk.Treeview(self._treeWindow, selectmode='browse')
        scrollY = ttk.Scrollbar(self._treeWindow, orient="vertical", command=self._tree.yview)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self._tree.configure(yscrollcommand=scrollY.set)
        self._treeWindow.add(self._tree)

        # Add columns to the tree.
        columns = []
        titleWidth = int(kwargs['tree_frame_width'])
        for column in self._COLUMNS:
            titleWidth -= int(kwargs[column[1]])
            columns.append(column[0])
        self._tree['columns'] = tuple(columns)
        for column in self._COLUMNS:
            self._tree.heading(column[0], text=column[0], anchor='w')
            self._tree.column(column[0], width=int(kwargs[column[1]]))
        self._tree.column('#0', width=titleWidth)

        # Create a data window.
        self._dataWindow = tk.PanedWindow(self._dataFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._dataWindow.pack(expand=True, fill='both')

        # Place a desc window inside the data window.
        self._descWindow = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=4, width=10)
        self._dataWindow.add(self._descWindow)

        self._fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']

        #--- Event bindings.
        self._root.bind(kwargs['key_create_project'], self._create_project)
        self._root.bind(kwargs['key_lock_project'], self._lock)
        self._root.bind(kwargs['key_unlock_project'], self._unlock)
        self._root.bind(kwargs['key_reload_project'], self._reload_project)
        self._root.bind(kwargs['key_save_project'], self.save_project)

        self._tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self._tree.bind('<Shift-B1-Motion>', self._move_node)
        self._tree.bind('<Delete>', self._delete_node)
        self._tree.bind(kwargs['button_context_menu'], self._open_context_menu)

        #--- Create a scene type submenu.
        self._typeMenu = tk.Menu(self._root, tearoff=0)
        self._typeMenu.add_command(label='Normal', command=lambda: self._set_type(self._tree.selection()[0], 0))
        self._typeMenu.add_command(label='Notes', command=lambda: self._set_type(self._tree.selection()[0], 1))
        self._typeMenu.add_command(label='Todo', command=lambda: self._set_type(self._tree.selection()[0], 2))
        self._typeMenu.add_command(label='Unused', command=lambda: self._set_type(self._tree.selection()[0], 3))

        #--- Create a scene scene status submenu.
        self._scStatusMenu = tk.Menu(self._root, tearoff=0)
        self._scStatusMenu.add_command(label='Outline', command=lambda: self._set_scn_status(self._tree.selection()[0], 1))
        self._scStatusMenu.add_command(label='Draft', command=lambda: self._set_scn_status(self._tree.selection()[0], 2))
        self._scStatusMenu.add_command(label='1st Edit', command=lambda: self._set_scn_status(self._tree.selection()[0], 3))
        self._scStatusMenu.add_command(label='2nd Edit', command=lambda: self._set_scn_status(self._tree.selection()[0], 4))
        self._scStatusMenu.add_command(label='Done', command=lambda: self._set_scn_status(self._tree.selection()[0], 5))

        #--- Create a narrative context menu.
        self._nvCtxtMenu = tk.Menu(self._root, tearoff=0)
        self._nvCtxtMenu.add_command(label='Add Scene', command=self._add_scene)
        self._nvCtxtMenu.add_command(label='Add Chapter', command=self._add_chapter)
        self._nvCtxtMenu.add_command(label='Add Part', command=self._add_part)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label='Delete', command=lambda: self._tree.event_generate('<Delete>', when='tail'))
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_cascade(label='Set Type', menu=self._typeMenu)
        self._nvCtxtMenu.add_cascade(label='Set Status', menu=self._scStatusMenu)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label='Expand', command=lambda: self._open_children(self._tree.selection()[0]))
        self._nvCtxtMenu.add_command(label='Collapse', command=lambda: self._close_children(self._tree.selection()[0]))
        self._nvCtxtMenu.add_command(label='Expand all', command=lambda: self._open_children(''))
        self._nvCtxtMenu.add_command(label='Collapse all', command=lambda: self._close_children(''))

        #--- Create a character status submenu.
        self._crStatusMenu = tk.Menu(self._root, tearoff=0)
        self._crStatusMenu.add_command(label='MajorCharacter', command=lambda: self._set_chr_status(True))
        self._crStatusMenu.add_command(label='MinorCharacter', command=lambda: self._set_chr_status(False))

        #--- Create a world element context menu.
        self._wrCtxtMenu = tk.Menu(self._root, tearoff=0)
        self._wrCtxtMenu.add_command(label='Add', command=lambda: self._add_world_element())
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_command(label='Delete', command=lambda: self._tree.event_generate('<Delete>', when='tail'))
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_cascade(label='Set Status', menu=self._crStatusMenu)

    @property
    def _isModified(self):
        return self._internalModificationFlag

    @_isModified.setter
    def _isModified(self, setFlag):
        if setFlag:
            self._internalModificationFlag = True
            self._pathBar.config(bg=self.kwargs['color_modified_bg'])
            self._pathBar.config(fg=self.kwargs['color_modified_fg'])
        else:
            self._internalModificationFlag = False
            if not self._isLocked:
                self._pathBar.config(bg=self._root.cget('background'))
                self._pathBar.config(fg='black')

    @property
    def _isLocked(self):
        return self._internalLockFlag

    @_isLocked.setter
    def _isLocked(self, setFlag):
        if setFlag and not self._internalLockFlag:
            if self._isModified:
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
            self._pathBar.config(bg=self._root.cget('background'))
            self._pathBar.config(fg='black')

    def _lock(self, event=None):
        if self._ywPrj.filePath is not None:
            self._isLocked = True
            # actually, this is a setter method with conditions
            if self._isLocked:
                self._ywPrj.lock()
                # make it persistent

    def _unlock(self, event=None):
        self._isLocked = False
        self._ywPrj.unlock()
        # make it persistent
        if self._ywPrj.has_changed_on_disk():
            if self.ask_yes_no(f'File has changed on disk. Reload?'):
                self.open_project(self._ywPrj.filePath)

    def _build_main_menu(self):
        """Add main menu entries.
        
        Overrides the superclass template method. 
        """
        # Files
        self._fileMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='File', menu=self._fileMenu)
        self._fileMenu.add_command(label='New', command=self._create_project)
        self._fileMenu.add_command(label='Open...', command=lambda: self.open_project(''))
        self._fileMenu.add_command(label='Lock', command=self._lock)
        self._fileMenu.add_command(label='Unlock', command=self._unlock)
        self._fileMenu.add_command(label='Reload', command=self._reload_project)
        self._fileMenu.add_command(label='Save', command=self.save_project)
        self._fileMenu.add_command(label='Close', command=self._close_project)
        self._fileMenu.add_command(label='Exit', command=self._on_quit)

        # View
        self._viewMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='View', menu=self._viewMenu)
        self._viewMenu.add_command(label="Expand selected", command=lambda: self._open_children(self._tree.selection()[0]))
        self._viewMenu.add_command(label="Collapse selected", command=lambda: self._close_children(self._tree.selection()[0]))
        self._viewMenu.add_command(label="Expand all", command=lambda: self._open_children(''))
        self._viewMenu.add_command(label="Collapse all", command=lambda: self._close_children(''))

        # Part
        self._partMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Part', menu=self._partMenu)
        self._partMenu.add_command(label='Add', command=self._add_part)
        self._partMenu.add_separator()
        self._partMenu.add_command(label='Export part descriptions for editing', command=lambda: self._exporter.run(self._ywPrj, '_parts'))

        # Chapter
        self._chapterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Chapter', menu=self._chapterMenu)
        self._chapterMenu.add_command(label='Add', command=self._add_chapter)
        self._chapterMenu.add_separator()
        self._chapterMenu.add_command(label='Export chapter descriptions for editing', command=lambda: self._exporter.run(self._ywPrj, '_chapters'))

        # Scene
        self._sceneMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Scene', menu=self._sceneMenu)
        self._sceneMenu.add_command(label='Add', command=self._add_scene)
        self._sceneMenu.add_separator()
        self._sceneMenu.add_command(label='Export scene descriptions for editing', command=lambda: self._exporter.run(self._ywPrj, '_scenes'))
        self._sceneMenu.add_command(label='Export scene list (spreadsheet)', command=lambda: self._exporter.run(self._ywPrj, '_scenelist'))

        # Character
        self._characterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Character', menu=self._characterMenu)
        self._characterMenu.add_command(label='Add', command=lambda: self._add_world_element(self._CR_ROOT))
        self._characterMenu.add_separator()
        self._characterMenu.add_command(label='Export descriptions for editing', command=lambda: self._exporter.run(self._ywPrj, '_characters'))
        self._characterMenu.add_command(label='Export character list (spreadsheet)', command=lambda: self._exporter.run(self._ywPrj, '_charlist'))

        # Location
        self._locationMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Location', menu=self._locationMenu)
        self._locationMenu.add_command(label='Add', command=lambda: self._add_world_element(self._LC_ROOT))
        self._locationMenu.add_separator()
        self._locationMenu.add_command(label='Export descriptions for editing', command=lambda: self._exporter.run(self._ywPrj, '_locations'))
        self._locationMenu.add_command(label='Export location list (spreadsheet)', command=lambda: self._exporter.run(self._ywPrj, '_loclist'))

        # Item
        self._itemMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Item', menu=self._itemMenu)
        self._itemMenu.add_command(label='Add', command=lambda: self._add_world_element(self._IT_ROOT))
        self._itemMenu.add_separator()
        self._itemMenu.add_command(label='Export descriptions for editing', command=lambda: self._exporter.run(self._ywPrj, '_items'))
        self._itemMenu.add_command(label='Export item list (spreadsheet)', command=lambda: self._exporter.run(self._ywPrj, '_itemlist'))

        # Export
        self._exportMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Export', menu=self._exportMenu)
        self._exportMenu.add_command(label='Manuscript for editing', command=lambda: self._exporter.run(self._ywPrj, '_manuscript'))
        self._exportMenu.add_command(label='Manuscript with visible structure tags for proof reading', command=lambda: self._exporter.run(self._ywPrj, '_proof'))
        self._exportMenu.add_separator()
        self._exportMenu.add_command(label='Manuscript without tags (export only)', command=lambda: self._exporter.run(self._ywPrj, ''))
        self._exportMenu.add_command(label='Brief synopsis (export only)', command=lambda: self._exporter.run(self._ywPrj, '_brf_synopsis'))
        self._exportMenu.add_command(label='Cross references (export only)', command=lambda: self._exporter.run(self._ywPrj, '_xref'))

        self._disable_menu()

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
        self._fileMenu.entryconfig('Reload', state='disabled')
        self._fileMenu.entryconfig('Save', state='disabled')

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
        self._fileMenu.entryconfig('Reload', state='normal')
        self._fileMenu.entryconfig('Save', state='normal')

    def _open_context_menu(self, event):
        row = self._tree.identify_row(event.y)
        if row:
            self._tree.focus_set()
            self._tree.selection_set(row)
            prefix = row[:2]
            if prefix in ('nv', self._PT, self._CH, self._SC):
                # Context is narrative/part/chapter/scene.
                if self._isLocked:
                    self._nvCtxtMenu.entryconfig('Delete', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Type', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Status', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Part', state='disabled')
                elif prefix.startswith('nv'):
                    self._nvCtxtMenu.entryconfig('Delete', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Type', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Status', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Part', state='normal')
                else:
                    self._nvCtxtMenu.entryconfig('Delete', state='normal')
                    self._nvCtxtMenu.entryconfig('Set Type', state='normal')
                    self._nvCtxtMenu.entryconfig('Set Status', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Part', state='normal')
                try:
                    self._nvCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._nvCtxtMenu.grab_release()
            elif prefix in ('wr', self._CR, self._LC, self._IT):
                # Context is character/location/item.
                if self._isLocked:
                    self._wrCtxtMenu.entryconfig('Add', state='disabled')
                    self._wrCtxtMenu.entryconfig('Delete', state='disabled')
                    self._wrCtxtMenu.entryconfig('Set Status', state='disabled')
                else:
                    self._wrCtxtMenu.entryconfig('Add', state='normal')
                    if prefix.startswith('wr'):
                        self._wrCtxtMenu.entryconfig('Delete', state='disabled')
                    else:
                        self._wrCtxtMenu.entryconfig('Delete', state='normal')
                    if (prefix.startswith(self._CR) or  row.endswith(self._CR)) and not self._isLocked:
                        self._wrCtxtMenu.entryconfig('Set Status', state='normal')
                    else:
                        self._wrCtxtMenu.entryconfig('Set Status', state='disabled')
                try:
                    self._wrCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._wrCtxtMenu.grab_release()

    def _build_tree(self):
        """Display the opened narrative's tree."""
        self._reset_tree()

        #--- Build Parts/Chapters/scenes tree.
        self._tree.insert('', 'end', self._NV_ROOT, text='Narrative', tags='root', open=True)
        inPart = False
        for chId in self._ywPrj.srtChapters:
            if self._ywPrj.chapters[chId].isTrash:
                self._trashNode = f'{self._CH}{chId}'
                inPart = False
            if self._ywPrj.chapters[chId].chLevel == 1:
                inPart = True
                inChapter = False
                title, columns, nodeTags = self._set_chapter_display(chId)
                partNode = self._tree.insert(self._NV_ROOT, 'end', f'{self._PT}{chId}', text=title, values=columns, tags=nodeTags, open=True)
            else:
                inChapter = True
                if inPart:
                    parentNode = partNode
                else:
                    parentNode = self._NV_ROOT
                title, columns, nodeTags = self._set_chapter_display(chId)
                chapterNode = self._tree.insert(parentNode, 'end', f'{self._CH}{chId}', text=title, values=columns, tags=nodeTags)
            for scId in self._ywPrj.chapters[chId].srtScenes:
                title, columns, nodeTags = self._set_scene_display(scId)
                if inChapter:
                    parentNode = chapterNode
                else:
                    parentNode = partNode
                self._tree.insert(parentNode, 'end', f'{self._SC}{scId}', text=title, values=columns, tags=nodeTags)

        #--- Build character tree.
        self._tree.insert('', 'end', self._CR_ROOT, text='Characters', tags='root', open=False)
        for crId in self._ywPrj.srtCharacters:
            title, columns, nodeTags = self._set_character_display(crId)
            self._tree.insert(self._CR_ROOT, 'end', f'{self._CR}{crId}', text=title, values=columns, tags=nodeTags)

        #--- Build location tree.
        self._tree.insert('', 'end', self._LC_ROOT, text='Locations', tags='root', open=False)
        for lcId in self._ywPrj.srtLocations:
            title, columns, nodeTags = self._set_location_display(lcId)
            self._tree.insert(self._LC_ROOT, 'end', f'{self._LC}{lcId}', text=title, values=columns, tags=nodeTags)

        #--- Build item tree.
        self._tree.insert('', 'end', self._IT_ROOT, text='Items', tags='root', open=False)
        for itId in self._ywPrj.srtItems:
            title, columns, nodeTags = self._set_item_display(itId)
            self._tree.insert(self._IT_ROOT, 'end', f'{self._IT}{itId}', text=title, values=columns, tags=nodeTags)

        #--- configure row display.
        self._tree.tag_configure('root', font=('', self._fontSize, 'bold'))
        self._tree.tag_configure('chapter', foreground=self.kwargs['color_chapter'])
        self._tree.tag_configure('unused', foreground=self.kwargs['color_unused'])
        self._tree.tag_configure('notes', foreground=self.kwargs['color_notes'])
        self._tree.tag_configure('todo', foreground=self.kwargs['color_todo'])
        self._tree.tag_configure('part', font=('', self._fontSize, 'bold'))
        self._tree.tag_configure('major', foreground=self.kwargs['color_major'])
        self._tree.tag_configure('minor', foreground=self.kwargs['color_minor'])
        self._tree.tag_configure('Outline', foreground=self.kwargs['color_outline'])
        self._tree.tag_configure('Draft', foreground=self.kwargs['color_draft'])
        self._tree.tag_configure('1st Edit', foreground=self.kwargs['color_1st_edit'])
        self._tree.tag_configure('2nd Edit', foreground=self.kwargs['color_2nd_edit'])
        self._tree.tag_configure('Done', foreground=self.kwargs['color_done'])

    def _update_tree(self):
        """Rebuild the sorted lists."""

        def update_node(node, chId):
            """Recursive tree builder."""
            for childNode in self._tree.get_children(node):
                if childNode.startswith(self._SC):
                    scId = childNode[2:]
                    self._ywPrj.chapters[chId].srtScenes.append(scId)
                    title, columns, nodeTags = self._set_scene_display(scId)
                elif childNode.startswith(self._CR):
                    crId = childNode[2:]
                    self._ywPrj.srtCharacters.append(crId)
                    title, columns, nodeTags = self._set_character_display(crId)
                elif childNode.startswith(self._LC):
                    lcId = childNode[2:]
                    self._ywPrj.srtLocations.append(lcId)
                    title, columns, nodeTags = self._set_location_display(lcId)
                elif childNode.startswith(self._IT):
                    itId = childNode[2:]
                    self._ywPrj.srtItems.append(itId)
                    title, columns, nodeTags = self._set_item_display(itId)
                else:
                    chId = childNode[2:]
                    self._ywPrj.srtChapters.append(chId)
                    self._ywPrj.chapters[chId].srtScenes = []
                    update_node(childNode, chId)
                    title, columns, nodeTags = self._set_chapter_display(chId)
                self._tree.item(childNode, text=title, values=columns, tags=nodeTags)

        self._ywPrj.srtChapters = []
        self._ywPrj.srtCharacters = []
        self._ywPrj.srtLocations = []
        self._ywPrj.srtItems = []
        update_node(self._NV_ROOT, '')
        update_node(self._CR_ROOT, '')
        update_node(self._LC_ROOT, '')
        update_node(self._IT_ROOT, '')
        self._isModified = True
        self._show_status()

    def _set_scene_display(self, scId):
        """Configure scene formatting and columns."""
        title = self._ywPrj.scenes[scId].title
        columns = []
        nodeTags = []
        if self._ywPrj.scenes[scId].isTodoScene:
            nodeTags.append('todo')
            return title, columns, tuple(nodeTags)

        if self._ywPrj.scenes[scId].isNotesScene:
            nodeTags.append('notes')
            return title, columns, tuple(nodeTags)

        if self._ywPrj.scenes[scId].isUnused:
            nodeTags.append('unused')
        else:
            nodeTags.append(Scene.STATUS[self._ywPrj.scenes[scId].status])
        columns.append(self._ywPrj.scenes[scId].wordCount)
        columns.append(Scene.STATUS[self._ywPrj.scenes[scId].status])
        try:
            columns.append(self._ywPrj.characters[self._ywPrj.scenes[scId].characters[0]].title)
        except:
            columns.append('N/A')
        try:
            columns.append(','.join(self._ywPrj.scenes[scId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_chapter_display(self, chId):
        """Configure chapter formatting and columns."""

        def count_words(chId):
            """Accumulate word counts of all relevant scenes in a chapter."""
            wordCount = 0
            for scId in self._ywPrj.chapters[chId].srtScenes:
                if self._ywPrj.scenes[scId].isTodoScene:
                    continue
                if self._ywPrj.scenes[scId].isNotesScene:
                    continue
                wordCount += self._ywPrj.scenes[scId].wordCount
            return wordCount

        title = self._ywPrj.chapters[chId].title
        columns = []
        nodeTags = []
        if self._ywPrj.chapters[chId].chType == 1:
            nodeTags.append('notes')
            return title, columns, tuple(nodeTags)

        elif self._ywPrj.chapters[chId].chType == 2:
            nodeTags.append('todo')
            return title, columns, tuple(nodeTags)

        elif self._ywPrj.chapters[chId].isUnused:
            nodeTags.append('unused')
        else:
            nodeTags.append('chapter')
        wordCount = count_words(chId)
        if self._ywPrj.chapters[chId].chLevel == 1:
            # This chapter begins a new section in ywriter.
            nodeTags.append('part')
            # Add all scene wordcounts until the next part.
            i = self._ywPrj.srtChapters.index(chId) + 1
            while i < len(self._ywPrj.srtChapters):
                c = self._ywPrj.srtChapters[i]
                if self._ywPrj.chapters[c].chLevel == 1:
                    break
                i += 1
                wordCount += count_words(c)
        columns.append(wordCount)
        return title, columns, tuple(nodeTags)

    def _set_character_display(self, crId):
        """Configure character formatting and columns."""
        title = self._ywPrj.characters[crId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ywPrj.characters[crId].tags))
        except:
            columns.append('')
        if self._ywPrj.characters[crId].isMajor:
            nodeTags.append('major')
        else:
            nodeTags.append('minor')
        return title, columns, tuple(nodeTags)

    def _set_location_display(self, lcId):
        """Configure location formatting and columns."""
        title = self._ywPrj.locations[lcId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ywPrj.locations[lcId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_item_display(self, itId):
        """Configure item formatting and columns."""
        title = self._ywPrj.items[itId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ywPrj.items[itId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_type(self, node, newType):
        """Recursively set scene or chapter type (Normal/Notes/Todo/Unused)."""
        if self._isLocked:
            return
        if node.startswith(self._SC):
            scene = self._ywPrj.scenes[node[2:]]
            if newType == 3:
                scene.isUnused = True
                scene.isTodoScene = False
                scene.isNotesScene = False
            elif newType == 2:
                scene.isUnused = False
                scene.isTodoScene = True
                scene.isNotesScene = False
            elif newType == 1:
                scene.isUnused = False
                scene.isTodoScene = False
                scene.isNotesScene = True
            else:
                scene.isUnused = False
                scene.isTodoScene = False
                scene.isNotesScene = False
        elif node.startswith(self._CH) or node.startswith(self._PT):
            self._tree.item(node, open=True)
            chapter = self._ywPrj.chapters[node[2:]]
            if newType == 3:
                chapter.isUnused = True
                chapter.chType = 0
            else:
                chapter.chType = newType
                chapter.isUnused = False
            # Go one level down.
            for childNode in self._tree.get_children(node):
                self._set_type(childNode, newType)
        else:
            # Do nothing, avoid tree update.
            return

        self._update_tree()

    def _set_scn_status(self, node, scnStatus):
        """Recursively set scene editing status (Outline/Draft..)."""
        if self._isLocked:
            return
        if node.startswith(self._SC):
            self._ywPrj.scenes[node[2:]].status = scnStatus
        elif node.startswith(self._CH) or node.startswith(self._PT) or node.startswith('nv'):
            self._tree.item(node, open=True)
            # Go one level down.
            for childNode in self._tree.get_children(node):
                self._set_scn_status(childNode, scnStatus)
        else:
            # Do nothing, avoid tree update.
            return

        self._update_tree()

    def _set_chr_status(self, chrStatus):
        """Set character status (Major/Minor)."""
        if self._isLocked:
            return
        node = self._tree.selection()[0]
        if node.startswith(self._CR):
            self._ywPrj.characters[node[2:]].isMajor = chrStatus
        elif node.endswith(self._CR):
            # Go one level down.
            for childNode in self._tree.get_children(node):
                self._set_chr_status(childNode, chrStatus)
        else:
            # Do nothing, avoid tree update.
            return

        self._update_tree()

    def _move_node(self, event):
        """Move a selected node in the novel tree."""
        if self._isLocked:
            return
        tv = event.widget
        node = tv.selection()[0]
        targetNode = tv.identify_row(event.y)
        # tv.item(targetNode, open=True)
        if node[:2] == targetNode[:2]:
            tv.move(node, tv.parent(targetNode), tv.index(targetNode))
        elif node.startswith(self._SC) and targetNode.startswith(self._CH) and not tv.get_children(targetNode):
            tv.move(node, targetNode, 0)
        elif node.startswith(self._SC) and targetNode.startswith(self._PT):
            tv.move(node, targetNode, 0)
        elif node.startswith(self._CH) and targetNode.startswith(self._PT) and not tv.get_children(targetNode):
            tv.move(node, targetNode, tv.index(targetNode))
        self._update_tree()

    def _on_quit(self, event=None):
        """Save windows size and position."""
        self._close_project()
        self.kwargs['tree_frame_width'] = self._treeFrame.winfo_width()
        for i, column in enumerate(self._COLUMNS):
            self.kwargs[column[1]] = self._tree.column(i, 'width')
        super()._on_quit()

    def _on_select_node(self, event):
        """Show info on the right level."""
        nodeId = self._tree.selection()[0]
        if nodeId.startswith(self._SC):
            self._set_scene_info(nodeId[2:])
        elif nodeId.startswith(self._CH):
            self._set_chapter_info(nodeId[2:])
        elif nodeId.startswith(self._PT):
            self._set_chapter_info(nodeId[2:])
        elif nodeId.startswith(self._NV_ROOT):
            self._set_novel_info()
        elif nodeId.startswith(self._CR):
            self._set_character_info(nodeId[2:])
        elif nodeId.startswith(self._LC):
            self._set_location_info(nodeId[2:])
        elif nodeId.startswith(self._IT):
            self._set_item_info(nodeId[2:])
        else:
            self._reset_info()

    def _reset_tree(self):
        """Clear the displayed novel tree."""
        for child in self._tree.get_children(''):
            self._tree.delete(child)

    def _set_novel_info(self):
        """Show the selected novel's description."""
        if self._ywPrj.desc is not None:
            text = self._ywPrj.desc
        else:
            text = ''
        self._descWindow.delete('1.0', tk.END)
        self._descWindow.insert(tk.END, text)

    def _set_chapter_info(self, chId):
        """Show the selected chapter's description."""
        if self._ywPrj.chapters[chId].desc is not None:
            text = self._ywPrj.chapters[chId].desc
        else:
            text = ''
        self._descWindow.delete('1.0', tk.END)
        self._descWindow.insert(tk.END, text)

    def _set_scene_info(self, scId):
        """Show the selected scene's description."""
        if self._ywPrj.scenes[scId].desc is not None:
            text = self._ywPrj.scenes[scId].desc
        else:
            text = ''
        self._descWindow.delete('1.0', tk.END)
        self._descWindow.insert(tk.END, text)

    def _set_character_info(self, crId):
        """Show the selected character's description."""
        if self._ywPrj.characters[crId].desc is not None:
            text = self._ywPrj.characters[crId].desc
        else:
            text = ''
        self._descWindow.delete('1.0', tk.END)
        self._descWindow.insert(tk.END, text)

    def _set_location_info(self, lcId):
        """Show the selected location's deslciption."""
        if self._ywPrj.locations[lcId].desc is not None:
            text = self._ywPrj.locations[lcId].desc
        else:
            text = ''
        self._descWindow.delete('1.0', tk.END)
        self._descWindow.insert(tk.END, text)

    def _set_item_info(self, itId):
        """Show the selected item's desitiption."""
        if self._ywPrj.items[itId].desc is not None:
            text = self._ywPrj.items[itId].desc
        else:
            text = ''
        self._descWindow.delete('1.0', tk.END)
        self._descWindow.insert(tk.END, text)

    def _create_project(self, event=None):
        """Create a yWriter project instance."""
        if self._ywPrj is not None:
            self._close_project()
        fileName = 'New project.yw7'
        self._ywPrj = Yw7WorkFile(fileName)
        if self._ywPrj.title:
            titleView = self._ywPrj.title
        else:
            titleView = 'Untitled yWriter project'
        if self._ywPrj.authorName:
            authorView = self._ywPrj.authorName
        else:
            authorView = 'Unknown author'
        self._root.title(f'{titleView} by {authorView} - {self._title}')
        self._show_path(os.path.normpath(fileName))
        self._enable_menu()
        self._build_tree()
        self._show_status()
        self._isModified = True

    def open_project(self, fileName=''):
        """Create a yWriter project instance and read the file.
        
        Display project title, description and status.
        Return the file name.
        Extends the superclass method.
        """
        fileName = super().open_project(fileName)
        if not fileName:
            return ''

        self._ywPrj = Yw7WorkFile(fileName)
        message = self._ywPrj.read()
        if message.startswith(ERROR):
            self._close_project()
            self._show_status(text=message)
            return ''

        self._show_path(f'{os.path.normpath(self._ywPrj.filePath)} (last saved on {self._ywPrj.fileDate})')
        if self._ywPrj.title:
            titleView = self._ywPrj.title
        else:
            titleView = 'Untitled yWriter project'
        if self._ywPrj.authorName:
            authorView = self._ywPrj.authorName
        else:
            authorView = 'Unknown author'
        self._root.title(f'{titleView} by {authorView} - {self._title}')
        self._enable_menu()
        self._build_tree()
        self._show_status()
        self._isModified = False
        if self._ywPrj.has_lockfile():
            self._isLocked = True
        return fileName

    def _close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        if self._isModified:
            if self.ask_yes_no('Save changes?'):
                self.save_project()
            self._isModified = False
        self._reset_tree()
        self._reset_info()
        self._isLocked = False
        super()._close_project()

    def _reload_project(self, event=None):
        """Reload a yWriter project."""
        if self._isModified and not self.ask_yes_no('Discard changes and reload the project?'):
            return

        if self._ywPrj.has_changed_on_disk() and not self.ask_yes_no('File has changed on disk. Reload anyway?'):
            return

        self._isModified = False
        # This is to avoid another question when closing the project
        self.open_project(self._ywPrj.filePath)
        # Includes closing

    def _reset_info(self):
        self._descWindow.delete('1.0', tk.END)

    def _open_children(self, parent):
        """Recursively open children"""
        self._tree.item(parent, open=True)
        for child in self._tree.get_children(parent):
            self._open_children(child)

    def _close_children(self, parent):
        """Recursively close children"""
        self._tree.item(parent, open=False)
        for child in self._tree.get_children(parent):
            self._close_children(child)

    def _show_status(self, message=None):
        """Extends the superclass method."""
        if self._ywPrj is not None and not message:
            partCount = 0
            chapterCount = 0
            sceneCount = 0
            wordCount = 0
            for chId in self._ywPrj.srtChapters:
                if self._ywPrj.chapters[chId].isUnused or self._ywPrj.chapters[chId].isTrash:
                    continue

                if self._ywPrj.chapters[chId].chType == 0:
                    for scId in self._ywPrj.chapters[chId].srtScenes:
                        if self._ywPrj.scenes[scId].isUnused:
                            continue

                        if self._ywPrj.scenes[scId].isNotesScene:
                            continue

                        if self._ywPrj.scenes[scId].isTodoScene:
                            continue

                        sceneCount += 1
                        wordCount += self._ywPrj.scenes[scId].wordCount
                if self._ywPrj.chapters[chId].chLevel == 1:
                    partCount += 1
                else:
                    chapterCount += 1
            message = f'{partCount} parts, {chapterCount} chapters, {sceneCount} scenes, {wordCount} words'
        super()._show_status(message)

    #--- Methods that change the project

    def _delete_node(self, event):
        """Delete a node and its children.
        
        Move scenes to the "Trash" chapter.
        Delete parts/chapters and move their children scenes to the "Trash" chapter.
        Delete characters/locations/items and remove their scene references.
        """

        def waste_scenes(node):
            """Move all scenes under the node to the 'trash bin'."""
            if node.startswith(self._SC):
                # Move scene.
                tv.move(node, self._trashNode, 0)
            else:
                # Delete chapter and go one level down.
                del self._ywPrj.chapters[node[2:]]
                for childNode in self._tree.get_children(node):
                    waste_scenes(childNode)

        if self._isLocked:
            return
        tv = event.widget
        selection = tv.selection()[0]
        elemId = selection[2:]
        if selection.startswith(self._SC):
            candidate = f'Scene "{self._ywPrj.scenes[elemId].title}"'
        elif selection.startswith(self._CH):
            candidate = f'Chapter "{self._ywPrj.chapters[elemId].title}"'
        elif selection.startswith(self._PT):
            candidate = f'Part "{self._ywPrj.chapters[elemId].title}"'
        elif selection.startswith(self._CR):
            candidate = f'Character "{self._ywPrj.characters[elemId].title}"'
        elif selection.startswith(self._LC):
            candidate = f'Location "{self._ywPrj.locations[elemId].title}"'
        elif selection.startswith(self._IT):
            candidate = f'Item "{self._ywPrj.items[elemId].title}"'
        else:
            return

        if self.ask_yes_no(f'Delete {candidate}?'):
            if tv.prev(selection):
                tv.selection_set(tv.prev(selection))
            else:
                tv.selection_set(tv.parent(selection))
            if selection == self._trashNode:
                # Remove the "trash bin".
                tv.delete(selection)
                self._trashNode = None
                for scId in self._ywPrj.chapters[elemId].srtScenes:
                    del self._ywPrj.scenes[scId]
                del self._ywPrj.chapters[elemId]
            elif selection.startswith(self._CR):
                # Delete a character and remove references.
                tv.delete(selection)
                del self._ywPrj.characters[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].characters.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self._LC):
                # Delete a location and remove references.
                tv.delete(selection)
                del self._ywPrj.locations[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].locations.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self._IT):
                # Delete an item and remove references.
                tv.delete(selection)
                del self._ywPrj.items[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].items.remove(elemId)
                    except:
                        pass
            else:
                if self._trashNode is None:
                    # Create a "trash bin"; use the first free chapter ID.
                    trashId = create_id(self._ywPrj.chapters)
                    self._ywPrj.chapters[trashId] = Chapter()
                    self._ywPrj.chapters[trashId].title = "Trash"
                    self._ywPrj.chapters[trashId].isTrash = True
                    self._trashNode = f'{self._CH}{trashId}'
                    self._tree.insert(self._NV_ROOT, 'end', self._trashNode, text='Trash', tags='unused', open=True)
                if selection.startswith(self._SC):
                    # Remove scene, if already in trash bin.
                    if self._tree.parent(selection) == self._trashNode:
                        tv.delete(selection)
                        del self._ywPrj.scenes[elemId]
                else:
                    # Move scene(s) to the "trash bin".
                    waste_scenes(selection)
                    tv.delete(selection)
                    self._set_type(self._trashNode, 3)
                    # Make sure the whole "trash bin" is unused.
            self._update_tree()

    def _add_part(self):
        """Add a Part node to the tree and create an instance."""
        if self._isLocked:
            return
        try:
            selection = self._tree.selection()[0]
        except:
            selection = ''
        parent = self._NV_ROOT
        index = 0
        if selection.startswith(self._SC):
            selection = self._tree.parent(selection)
        if selection.startswith(self._CH):
            index = self._tree.index(selection) + 1
            selection = self._tree.parent(selection)
        if selection.startswith(self._PT):
            index = self._tree.index(selection) + 1
        chId = create_id(self._ywPrj.chapters)
        newNode = f'{self._PT}{chId}'
        self._ywPrj.chapters[chId] = Chapter()
        self._ywPrj.chapters[chId].title = f'New Part (ID{chId})'
        self._ywPrj.chapters[chId].chLevel = 1
        self._ywPrj.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self._tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self._tree.selection_set(newNode)
        self._tree.see(newNode)

    def _add_chapter(self):
        """Add a Chapter node to the tree and create an instance."""
        if self._isLocked:
            return
        try:
            selection = self._tree.selection()[0]
        except:
            selection = ''
        parent = self._NV_ROOT
        index = 0
        if selection.startswith(self._SC):
            parent = self._tree.parent(selection)
            selection = self._tree.parent(selection)
        if selection.startswith(self._CH):
            parent = self._tree.parent(selection)
            index = self._tree.index(selection) + 1
        elif selection.startswith(self._PT):
            parent = selection
        chId = create_id(self._ywPrj.chapters)
        newNode = f'{self._CH}{chId}'
        self._ywPrj.chapters[chId] = Chapter()
        self._ywPrj.chapters[chId].title = f'New Chapter (ID{chId})'
        self._ywPrj.chapters[chId].chLevel = 0
        self._ywPrj.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self._tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self._tree.selection_set(newNode)
        self._tree.see(newNode)

    def _add_scene(self):
        """Add a Scene node to the tree and create an instance."""
        if self._isLocked:
            return
        try:
            selection = self._tree.selection()[0]
        except:
            return

        index = 0
        if selection.startswith(self._SC):
            parent = self._tree.parent(selection)
            index = self._tree.index(selection) + 1
        elif selection.startswith(self._CH):
            parent = selection
        elif selection.startswith(self._PT):
            parent = selection
        else:
            return

        scId = create_id(self._ywPrj.scenes)
        newNode = f'{self._SC}{scId}'
        self._ywPrj.scenes[scId] = Scene()
        self._ywPrj.scenes[scId].title = f'New Scene (ID{scId})'
        self._ywPrj.scenes[scId].status = 1
        # Edit status = Outline
        title, columns, nodeTags = self._set_scene_display(scId)
        self._tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self._tree.selection_set(newNode)
        self._tree.see(newNode)

    def _add_world_element(self, selection=None):
        """Add a Character/Location/Item node to the tree and create an instance.
        
        Positional arguments:
            selection -- str: tree position where to place a new node.
            
        - The new node's type is determined by the "selection" argument.
        - If a node of the same type as the new node is selected, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the first position.   
        """
        if self._isLocked:
            return
        if selection is None:
            selection = self._tree.selection()[0]
        if self._CR in selection:
            # Add a character.
            crId = create_id(self._ywPrj.characters)
            newNode = f'{self._CR}{crId}'
            self._ywPrj.characters[crId] = Character()
            self._ywPrj.characters[crId].title = f'New Character (ID{crId})'
            title, columns, nodeTags = self._set_character_display(crId)
            root = self._CR_ROOT
            prefix = self._CR
        elif self._LC in selection:
            # Add a location.
            lcId = create_id(self._ywPrj.locations)
            newNode = f'{self._LC}{lcId}'
            self._ywPrj.locations[lcId] = WorldElement()
            self._ywPrj.locations[lcId].title = f'New Location (ID{lcId})'
            title, columns, nodeTags = self._set_location_display(lcId)
            root = self._LC_ROOT
            prefix = self._LC
        elif self._IT in selection:
            # Add an item.
            itId = create_id(self._ywPrj.items)
            newNode = f'{self._IT}{itId}'
            self._ywPrj.items[itId] = WorldElement()
            self._ywPrj.items[itId].title = f'New Item (ID{itId})'
            title, columns, nodeTags = self._set_item_display(itId)
            root = self._IT_ROOT
            prefix = self._IT
        else:
            return

        if selection.startswith(prefix):
            index = self._tree.index(selection) + 1
        else:
            index = 0
        self._tree.insert(root, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self._tree.selection_set(newNode)
        self._tree.see(newNode)

    def save_project(self, event=None):
        """Save the yWriter project to disk and set 'unchanged' status.
        
        Return True on success, otherwise return False.
        """
        if self._isLocked:
            return
        if len(self._ywPrj.srtChapters) < 1:
            self.set_info_how(f'{ERROR}Cannot save: The project must have at least one chapter or part.')
            return False

        if self._ywPrj.is_locked():
            self.set_info_how(f'{ERROR}yWriter seems to be open. Please close first.')
            return False

        if self._ywPrj.has_changed_on_disk() and not self.ask_yes_no('File has changed on disk. Save anyway?'):
            return False

        self._ywPrj.write()
        self._show_path(f'{os.path.normpath(self._ywPrj.filePath)} (last saved on {self._ywPrj.fileDate})')
        self._isModified = False
        self._restore_status(event)
        self.kwargs['yw_last_open'] = self._ywPrj.filePath
        return True

