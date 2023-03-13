"""Provide a tkinter based novelyst tree view.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from pywriter.pywriter_globals import *
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.world_element import WorldElement
from pywriter.model.basic_element import BasicElement
from pywriter.model.id_generator import create_id


class TreeViewer(ttk.Frame):
    """Widget for novelyst tree view.
    
    Class constants:
        PART_PREFIX -- Part node ID prefix
        CHAPTER_PREFIX -- Chapter node ID prefix
        SCENE_PREFIX -- Scene node ID prefix
        CHARACTER_PREFIX -- Character node ID prefix
        LOCATION_PREFIX -- Location node ID prefix
        ITEM_PREFIX -- Item node ID prefix
        PRJ_NOTE_PREFIX -- project note node ID prefix
        NV_ROOT -- Root of the Narrative subtree
        RS_ROOT -- Root of the Research subtree
        PL_ROOT -- Root of the Research subtree
        CR_ROOT -- Root of the Characters subtree
        LC_ROOT -- Root of the Locations subtree
        IT_ROOT -- Root of the Items subtree
        PN_ROOT -- Root of the Items subtree
    
    Public methods:
        build_tree() -- Create and display the tree.
        refresh_tree() -- Display the tree nodes regarding the way they are read from the file.
        update_prj_structure() -- Iterate the tree and rebuild the sorted lists.
        reset_tree() -- Clear the displayed tree.
        next_node(thisNode, root) -- Return the next node ID of the same element type as thisNode.
        prev_node(thisNode, root) -- Return the previous node ID of the same element type as thisNode.
        add_part(**kwargs) -- Add a Part node to the tree and create an instance.
        add_chapter(**kwargs) -- Add a Chapter node to the tree and create an instance.
        add_scene(**kwargs) -- Add a Scene node to the tree and create an instance.
        add_character(**kwargs) -- Add a Character node to the tree and create an instance.
        add_location(**kwargs) -- Add a Location node to the tree and create an instance.
        add_item(**kwargs) -- Add an Item node to the tree and create an instance.
        add_project_note(**kwargs) -- Add a Project note node to the tree and create an instance.
        add_other_element() -- Add a Character/Location/Item/Project note node to the tree and create an instance.
        open_children(parent) -- Recursively show children nodes.
        close_children(parent) -- Recursively close children nodes.
        show_chapters(parent) -- Open Narrative/Part nodes and close chapter nodes.
        on_quit() -- Write column width to the applicaton's keyword arguments.
        
    Public instance variables:
        tree -- ttk.Treeview: The treeview widget to display.
        columns -- list of tuples (ID, title, width).
        scStyleMenu -- tk.Menu: Scene "Style" submenu.
        scTypeMenu -- tk.Menu: Scene "Type" submenu.
        scStatusMenu -- tk.Menu: Scene "Status" submenu.
        crStatusMenu -- tk.Menu: Character "Status" submenu.        
    """
    PART_PREFIX = 'pt'
    CHAPTER_PREFIX = 'ch'
    SCENE_PREFIX = 'sc'
    CHARACTER_PREFIX = 'cr'
    LOCATION_PREFIX = 'lc'
    ITEM_PREFIX = 'it'
    PRJ_NOTE_PREFIX = 'pn'
    NV_ROOT = 'nv'
    RS_ROOT = 'rs'
    PL_ROOT = 'pl'
    CR_ROOT = f'wr{CHARACTER_PREFIX}'
    LC_ROOT = f'wr{LOCATION_PREFIX}'
    IT_ROOT = f'wr{ITEM_PREFIX}'
    PN_ROOT = f'wr{PRJ_NOTE_PREFIX}'

    _COLUMNS = dict(
        wc=(_('Words'), 'wc_width'),
        vp=(_('Viewpoint'), 'vp_width'),
        sy=(_('Style'), 'style_width'),
        st=(_('Status'), 'status_width'),
        nt=(_('N'), 'nt_width'),
        dt=(_('Date'), 'date_width'),
        tm=(_('Time'), 'time_width'),
        dr=(_('Duration'), 'duration_width'),
        tg=(_('Tags'), 'tags_width',),
        po=(_('Position'), 'ps_width'),
        ac=(_('Arcs'), 'arcs_width'),
        ar=(_('A/R'), 'pacing_width'),
        pt=(_('Plot'), 'plot_width'),
        )
    # Key: column ID
    # Value: (column title, column width)

    _KEY_CANCEL_PART = '<Shift-Delete>'
    _KEY_DEMOTE_PART = '<Shift-Right>'
    _KEY_PROMOTE_CHAPTER = '<Shift-Left>'

    _SCN_STATUS = []
    for status in Scene.STATUS:
        if not status:
            _SCN_STATUS.append(status)
        else:
            _SCN_STATUS.append(_(status))

    def __init__(self, master, ui, kwargs, **kw):
        """Put a tkinter tree in the specified parent widget.
        
        Positional arguments:
            master -- parent widget for displaying the tree view.
            ui -- GUI class reference.
        
        Required keyword arguments:
            button_context_menu -- str: Mouse button to show the treeveiw context menu.
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
        """
        super().__init__(master, **kw)
        self._ui = ui
        self._wordsTotal = None
        self._trashNode = None

        # Create a novel tree.
        self.tree = ttk.Treeview(self, selectmode='extended')
        scrollX = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollY = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(xscrollcommand=scrollX.set)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollX.pack(side=tk.BOTTOM, fill=tk.X)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        #--- Add columns to the tree.
        self.configure_columns()

        #--- Create public submenus.

        #--- Create a scene style submenu.
        self.scStyleMenu = tk.Menu(self.tree, tearoff=0)
        self.scStyleMenu.add_command(label=_('staged'), command=lambda: self._set_scn_style(self.tree.selection(), None))
        self.scStyleMenu.add_command(label=_('explaining'), command=lambda: self._set_scn_style(self.tree.selection(), 'explaining'))
        self.scStyleMenu.add_command(label=_('descriptive'), command=lambda: self._set_scn_style(self.tree.selection(), 'descriptive'))
        self.scStyleMenu.add_command(label=_('summarizing'), command=lambda: self._set_scn_style(self.tree.selection(), 'summarizing'))

        #--- Create a scene type submenu.
        self.scTypeMenu = tk.Menu(self.tree, tearoff=0)
        self.scTypeMenu.add_command(label=_('Normal'), command=lambda: self._set_type(self.tree.selection(), 0))
        self.scTypeMenu.add_command(label=_('Notes'), command=lambda: self._set_type(self.tree.selection(), 1))
        self.scTypeMenu.add_command(label=_('Todo'), command=lambda: self._set_type(self.tree.selection(), 2))
        self.scTypeMenu.add_command(label=_('Unused'), command=lambda: self._set_type(self.tree.selection(), 3))

        #--- Create a scene scene status submenu.
        self.scStatusMenu = tk.Menu(self.tree, tearoff=0)
        self.scStatusMenu.add_command(label=_('Outline'), command=lambda: self._set_scn_status(self.tree.selection(), 1))
        self.scStatusMenu.add_command(label=_('Draft'), command=lambda: self._set_scn_status(self.tree.selection(), 2))
        self.scStatusMenu.add_command(label=_('1st Edit'), command=lambda: self._set_scn_status(self.tree.selection(), 3))
        self.scStatusMenu.add_command(label=_('2nd Edit'), command=lambda: self._set_scn_status(self.tree.selection(), 4))
        self.scStatusMenu.add_command(label=_('Done'), command=lambda: self._set_scn_status(self.tree.selection(), 5))

        #--- Create a character status submenu.
        self.crStatusMenu = tk.Menu(self.tree, tearoff=0)
        self.crStatusMenu.add_command(label=_('Major Character'), command=lambda: self._set_chr_status(True))
        self.crStatusMenu.add_command(label=_('Minor Character'), command=lambda: self._set_chr_status(False))

        #--- Create local context menus.

        #--- Create a narrative context menu.
        self._nvCtxtMenu = tk.Menu(self.tree, tearoff=0)
        self._nvCtxtMenu.add_command(label=_('Add Scene'), command=self.add_scene)
        self._nvCtxtMenu.add_command(label=_('Add Chapter'), command=self.add_chapter)
        self._nvCtxtMenu.add_command(label=_('Promote Chapter'), command=lambda: self.tree.event_generate(self._KEY_PROMOTE_CHAPTER, when='tail'))
        self._nvCtxtMenu.add_command(label=_('Add Part'), command=self.add_part)
        self._nvCtxtMenu.add_command(label=_('Demote Part'), command=lambda: self.tree.event_generate(self._KEY_DEMOTE_PART, when='tail'))
        self._nvCtxtMenu.add_command(label=_('Cancel Part'), command=lambda: self.tree.event_generate(self._KEY_CANCEL_PART, when='tail'))
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label=_('Delete'), command=lambda: self.tree.event_generate('<Delete>', when='tail'))
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_cascade(label=_('Set Type'), menu=self.scTypeMenu)
        self._nvCtxtMenu.add_cascade(label=_('Set Status'), menu=self.scStatusMenu)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_cascade(label=_('Set Style'), menu=self.scStyleMenu)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label=_('Join with previous'), command=self.join_scenes)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label=_('Chapter level'), command=lambda: self.show_chapters(self.NV_ROOT))
        self._nvCtxtMenu.add_command(label=_('Expand'), command=lambda: self.open_children(self.tree.selection()[0]))
        self._nvCtxtMenu.add_command(label=_('Collapse'), command=lambda: self.close_children(self.tree.selection()[0]))
        self._nvCtxtMenu.add_command(label=_('Expand all'), command=lambda: self.open_children(''))
        self._nvCtxtMenu.add_command(label=_('Collapse all'), command=lambda: self.close_children(''))
        self._nvCtxtMenu.add_command(label=_('Toggle "Contents" window'), command=self._ui.toggle_viewer)

        #--- Create a world element context menu.
        self._wrCtxtMenu = tk.Menu(self.tree, tearoff=0)
        self._wrCtxtMenu.add_command(label=_('Add'), command=self.add_other_element)
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_command(label=_('Delete'), command=lambda: self.tree.event_generate('<Delete>', when='tail'))
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_cascade(label=_('Set Status'), menu=self.crStatusMenu)

        #--- configure tree row display.
        fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']
        self.tree.tag_configure('root', font=('', fontSize, 'bold'))
        self.tree.tag_configure('chapter', foreground=kwargs['color_chapter'])
        self.tree.tag_configure('unused', foreground=kwargs['color_unused'])
        self.tree.tag_configure('notes', foreground=kwargs['color_notes'])
        self.tree.tag_configure('todo', foreground=kwargs['color_todo'])
        self.tree.tag_configure('todo part', font=('', fontSize, 'bold'), foreground=kwargs['color_todo'])
        self.tree.tag_configure('part', font=('', fontSize, 'bold'))
        self.tree.tag_configure('notes part', font=('', fontSize, 'bold'), foreground=kwargs['color_notes'])
        self.tree.tag_configure('major', foreground=kwargs['color_major'])
        self.tree.tag_configure('minor', foreground=kwargs['color_minor'])
        self.tree.tag_configure('Outline', foreground=kwargs['color_outline'])
        self.tree.tag_configure('Draft', foreground=kwargs['color_draft'])
        self.tree.tag_configure('1st Edit', foreground=kwargs['color_1st_edit'])
        self.tree.tag_configure('2nd Edit', foreground=kwargs['color_2nd_edit'])
        self.tree.tag_configure('Done', foreground=kwargs['color_done'])
        self.tree.tag_configure('summarizing', foreground=kwargs['color_summarizing'])
        self.tree.tag_configure('descriptive', foreground=kwargs['color_descriptive'])
        self.tree.tag_configure('explaining', foreground=kwargs['color_explaining'])

        #--- Event bindings.
        self.tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self.tree.bind('<Alt-B1-Motion>', self._move_node)
        self.tree.bind('<Delete>', self._delete_node)
        self.tree.bind(self._KEY_CANCEL_PART, self._cancel_part)
        self.tree.bind(self._KEY_DEMOTE_PART, self._demote_part)
        self.tree.bind(self._KEY_PROMOTE_CHAPTER, self._promote_chapter)
        self.tree.bind(kwargs['button_context_menu'], self._open_context_menu)

    def configure_columns(self):
        """Determine the order of the columnns.
        
        Read from the ui keyword arguments:
            column_order -- str: ordered column IDs, semicolon-separated.
        
        Write instance variables:
            _colPos -- dict: key=ID, value=index.
            columns -- list of tuples (ID, title, width).
        """
        # Column position by column ID.
        self._colPos = {}
        self.columns = []
        titles = []
        srtColumns = string_to_list(self._ui.kwargs['column_order'])

        # Check data integrity.
        for coId in self._COLUMNS:
            if not coId in srtColumns:
                srtColumns.append(coId)
        i = 0
        for coId in srtColumns:
            try:
                title, width = self._COLUMNS[coId]
            except:
                continue
            self._colPos[coId] = i
            i += 1
            self.columns.append((coId, title, width))
            titles.append(title)
        self.tree.configure(columns=tuple(titles))
        for column in self.columns:
            self.tree.heading(column[1], text=column[1], anchor='w')
            self.tree.column(column[1], width=int(self._ui.kwargs[column[2]]), minwidth=3, stretch=False)
        self.tree.column('#0', width=int(self._ui.kwargs['title_width']), stretch=False)

    def build_tree(self):
        """Create and display the tree."""
        self.reset_tree()

        #--- Build the toplevel  structure.
        self.tree.insert('', 'end', self.NV_ROOT, text=_('Narrative'), tags='root', open=True)
        self.tree.insert('', 'end', self.CR_ROOT, text=_('Characters'), tags='root', open=False)
        self.tree.insert('', 'end', self.LC_ROOT, text=_('Locations'), tags='root', open=False)
        self.tree.insert('', 'end', self.IT_ROOT, text=_('Items'), tags='root', open=False)
        self.tree.insert('', 'end', self.RS_ROOT, text=_('Research'), tags='root', open=False)
        self.tree.insert('', 'end', self.PL_ROOT, text=_('Planning'), tags='root', open=False)
        self.tree.insert('', 'end', self.PN_ROOT, text=_('Project notes'), tags='root', open=True)

        #--- Build Parts/Chapters/scenes tree.
        inPart = False
        inNotesPart = False
        inTodoPart = False
        wordCount = 0
        self._wordsTotal = self._ui.prjFile.get_counts()[0]
        for chId in self._ui.novel.srtChapters:
            if self._ui.novel.chapters[chId].isTrash:
                self._ui.novel.chapters[chId].chType = 3
                self._trashNode = f'{self.CHAPTER_PREFIX}{chId}'
                inPart = False
            if self._ui.novel.chapters[chId].chLevel == 1:
                # Part begins.
                inPart = True
                inChapter = False
                if self._ui.novel.chapters[chId].chType == 1:
                    # "Notes" part begins.
                    inTodoPart = False
                    inNotesPart = True
                    parent = self.RS_ROOT
                elif self._ui.novel.chapters[chId].chType == 2:
                    # "Todo" part begins.
                    inNotesPart = False
                    inTodoPart = True
                    parent = self.PL_ROOT
                else:
                    inNotesPart = False
                    inTodoPart = False
                    parent = self.NV_ROOT
                title, columns, nodeTags = self._set_chapter_display(chId, wordCount)
                partNode = self.tree.insert(parent, 'end', f'{self.PART_PREFIX}{chId}', text=title, values=columns, tags=nodeTags, open=True)
            else:
                # Chapter begins.
                inChapter = True
                if self._ui.novel.chapters[chId].chType != 1:
                    # Regular chapter can not be in "Notes" part.
                    if inNotesPart:
                        inNotesPart = False
                        inPart = False
                if self._ui.novel.chapters[chId].chType != 2:
                    # Regular chapter can not be in "Todo" part.
                    if inTodoPart:
                        inTodoPart = False
                        inPart = False
                if inPart:
                    parentNode = partNode
                else:
                    parentNode = self.NV_ROOT
                title, columns, nodeTags = self._set_chapter_display(chId, wordCount)
                chapterNode = self.tree.insert(parentNode, 'end', f'{self.CHAPTER_PREFIX}{chId}', text=title, values=columns, tags=nodeTags, open=True)
            for scId in self._ui.novel.chapters[chId].srtScenes:
                title, columns, nodeTags = self._set_scene_display(scId, wordCount)
                if inChapter:
                    parentNode = chapterNode
                else:
                    parentNode = partNode
                self.tree.insert(parentNode, 'end', f'{self.SCENE_PREFIX}{scId}', text=title, values=columns, tags=nodeTags)

                # add word count, if the scenen is "Normal".
                if self._ui.novel.scenes[scId].scType == 0:
                    wordCount += self._ui.novel.scenes[scId].wordCount

        #--- Build character tree.
        for crId in self._ui.novel.srtCharacters:
            title, columns, nodeTags = self._set_character_display(crId)
            self.tree.insert(self.CR_ROOT, 'end', f'{self.CHARACTER_PREFIX}{crId}', text=title, values=columns, tags=nodeTags)

        #--- Build location tree.
        for lcId in self._ui.novel.srtLocations:
            title, columns, nodeTags = self._set_location_display(lcId)
            self.tree.insert(self.LC_ROOT, 'end', f'{self.LOCATION_PREFIX}{lcId}', text=title, values=columns, tags=nodeTags)

        #--- Build item tree.
        for itId in self._ui.novel.srtItems:
            title, columns, nodeTags = self._set_item_display(itId)
            self.tree.insert(self.IT_ROOT, 'end', f'{self.ITEM_PREFIX}{itId}', text=title, values=columns, tags=nodeTags)

        #--- Build project note tree.
        for pnId in self._ui.novel.srtPrjNotes:
            title, columns, nodeTags = self._set_prjNote_display(pnId)
            self.tree.insert(self.PN_ROOT, 'end', f'{self.PRJ_NOTE_PREFIX}{pnId}', text=title, values=columns, tags=nodeTags)

        self.tree.selection_set(self.NV_ROOT)

    def refresh_tree(self):
        """Display the tree nodes regarding the way they are read from the file."""
        modifiedNodes = []
        isModified = self._ui.isModified
        if self._ui.prjFile.renumber_chapters():
            isModified = True

        # Make sure that nodes with non-"Normal" parents inherit the type.
        partType = 0
        for chId in self._ui.novel.srtChapters:
            if self._ui.novel.chapters[chId].chLevel == 1:
                partType = self._ui.novel.chapters[chId].chType
            elif partType != 0 and not self._ui.novel.chapters[chId].isTrash:
                if self._ui.novel.chapters[chId].chType != partType:
                    self._ui.novel.chapters[chId].chType = partType
                    isModified = True
            if self._ui.novel.chapters[chId].chType != 0:
                for scId in self._ui.novel.chapters[chId].srtScenes:
                    if self._ui.novel.scenes[scId].scType != self._ui.novel.chapters[chId].chType:
                        self._ui.novel.scenes[scId].scType = self._ui.novel.chapters[chId].chType
                        modifiedNodes.append(f'{self.SCENE_PREFIX}{scId}')
        self.build_tree()
        self._ui.isModified = isModified
        for node in modifiedNodes:
            self.tree.see(node)

    def update_prj_structure(self):
        """Iterate the tree and rebuild the sorted lists."""

        def serialize_tree(node, chId, scnPos=0):
            """Recursive tree walker.
            
            Positional arguments: 
                node -- str: Node ID to start from.
                chId -- str: Chapter ID where the recursion starts.
            Optional arguments:
                scnPos -- int: Word count so far.
            
            Return the incremented word count.
            """
            for childNode in self.tree.get_children(node):
                if childNode.startswith(self.SCENE_PREFIX):
                    scId = childNode[2:]
                    self._ui.novel.chapters[chId].srtScenes.append(scId)
                    title, columns, nodeTags = self._set_scene_display(scId, scnPos)
                    if self._ui.novel.scenes[scId].scType == 0:
                        scnPos += self._ui.novel.scenes[scId].wordCount
                elif childNode.startswith(self.CHARACTER_PREFIX):
                    crId = childNode[2:]
                    self._ui.novel.srtCharacters.append(crId)
                    title, columns, nodeTags = self._set_character_display(crId)
                elif childNode.startswith(self.LOCATION_PREFIX):
                    lcId = childNode[2:]
                    self._ui.novel.srtLocations.append(lcId)
                    title, columns, nodeTags = self._set_location_display(lcId)
                elif childNode.startswith(self.ITEM_PREFIX):
                    itId = childNode[2:]
                    self._ui.novel.srtItems.append(itId)
                    title, columns, nodeTags = self._set_item_display(itId)
                elif childNode.startswith(self.PRJ_NOTE_PREFIX):
                    pnId = childNode[2:]
                    self._ui.novel.srtPrjNotes.append(pnId)
                    title, columns, nodeTags = self._set_prjNote_display(pnId)
                else:
                    chId = childNode[2:]
                    self._ui.novel.srtChapters.append(chId)
                    self._ui.novel.chapters[chId].srtScenes = []
                    chpPos = scnPos
                    # save chapter start position, because the positions of the
                    # chapters scenes will now be added to scnPos.
                    scnPos = serialize_tree(childNode, chId, scnPos)
                    title, columns, nodeTags = self._set_chapter_display(chId, chpPos)
                self.tree.item(childNode, text=title, values=columns, tags=nodeTags)
            return scnPos

        self._wordsTotal = self._ui.prjFile.get_counts()[0]
        self._ui.novel.srtChapters = []
        self._ui.novel.srtCharacters = []
        self._ui.novel.srtLocations = []
        self._ui.novel.srtItems = []
        self._ui.novel.srtPrjNotes = []
        serialize_tree(self.NV_ROOT, '')
        serialize_tree(self.PL_ROOT, '')
        serialize_tree(self.RS_ROOT, '')
        serialize_tree(self.CR_ROOT, '')
        serialize_tree(self.LC_ROOT, '')
        serialize_tree(self.IT_ROOT, '')
        serialize_tree(self.PN_ROOT, '')

        # Make sure that scenes inherit the parent's type, if not normal.
        self._ui.prjFile.adjust_scene_types()

        # Check the arc related associations.
        self._ui.prjFile.check_arcs()

        self._ui.isModified = True
        self._ui.show_status()

    def reset_tree(self):
        """Clear the displayed tree."""
        for child in self.tree.get_children(''):
            self.tree.delete(child)

    def next_node(self, thisNode, root):
        """Return the next node ID  of the same element type as thisNode.
        
        Positional arguments: 
            thisNode -- str: node ID
            root -- str: root ID of the subtree to search 
        """

        def search_tree(parent, result, flag):
            """Search the tree for the node ID after thisNode."""
            for child in self.tree.get_children(parent):
                if result:
                    break
                if child.startswith(prefix):
                    if flag:
                        result = child
                        break
                    elif child == thisNode:
                        flag = True
                else:
                    result, flag = search_tree(child, result, flag)
            return result, flag

        prefix = thisNode[:2]
        nextNode, __ = search_tree(root, None, False)
        return nextNode

    def prev_node(self, thisNode, root):
        """Return the previous node ID of the same element type as thisNode.

        Positional arguments: 
            thisNode -- str: node ID
            root -- str: root ID of the subtree to search 
        """

        def search_tree(parent, result, prevNode):
            """Search the tree for the node ID before thisNode."""
            for child in self.tree.get_children(parent):
                if result:
                    break
                if child.startswith(prefix):
                    if child == thisNode:
                        result = prevNode
                        break
                    else:
                        prevNode = child
                else:
                    result, prevNode = search_tree(child, result, prevNode)
            return result, prevNode

        prefix = thisNode[:2]
        prevNode, __ = search_tree(root, None, None)
        return prevNode

    def add_part(self, **kwargs):
        """Add a Part node to the tree and create an instance.
        
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Part title. Default: Auto-generated title. 
            chType -- int: Part type. Default: 0.  
            NoNumber -- str: Do not auto-number this part. Default: None.
           
        - Place the new node at the next free position after the selection, if possible.
        - Otherwise, put the new node at the beginning of the "Narrative". 
        
        Return the chapter ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                selection = ''
        parent = self.NV_ROOT
        index = 0
        if selection.startswith(self.SCENE_PREFIX):
            selection = self.tree.parent(selection)
        if selection.startswith(self.CHAPTER_PREFIX):
            index = self.tree.index(selection) + 1
            selection = self.tree.parent(selection)
        if selection.startswith(self.PART_PREFIX):
            index = self.tree.index(selection) + 1
            parent = self.tree.parent(selection)
        elif selection.startswith(self.PL_ROOT):
            index = 0
            parent = self.PL_ROOT
        elif selection.startswith(self.RS_ROOT):
            index = 0
            parent = self.RS_ROOT
        chId = create_id(self._ui.novel.chapters)
        newNode = f'{self.PART_PREFIX}{chId}'
        self._ui.novel.chapters[chId] = Chapter()
        title = kwargs.get('title', None)
        if title:
            self._ui.novel.chapters[chId].title = title
        else:
            self._ui.novel.chapters[chId].title = f'{_("New Part")} (ID{chId})'
        self._ui.novel.chapters[chId].chLevel = 1

        # Initialize custom keyword variables.
        for fieldName in self._ui.prjFile.CHP_KWVAR:
            self._ui.novel.chapters[chId].kwVar[fieldName] = None
        self._ui.novel.chapters[chId].kwVar['Field_NoNumber'] = kwargs.get('NoNumber', None)
        if parent.startswith(self.PL_ROOT):
            self._ui.novel.chapters[chId].chType = 2
        elif parent.startswith(self.RS_ROOT):
            self._ui.novel.chapters[chId].chType = 1
        else:
            self._ui.novel.chapters[chId].chType = kwargs.get('chType', 0)
        self._ui.novel.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.refresh_tree()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return chId

    def add_chapter(self, **kwargs):
        """Add a Chapter node to the tree and create an instance.
             
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Scene title. Default: Auto-generated title. 
            chType -- int: Chapter type. Default: 0.
            NoNumber -- str: Do not auto-number this chapter. Default: None.
            
        - Place the new node at the next free position after the selection, if possible.
        - Otherwise, put the new node at the beginning of the "Narrative". 
        
        Return the chapter ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                selection = ''
        parent = self.NV_ROOT
        index = 0
        if selection.startswith(self.SCENE_PREFIX):
            parent = self.tree.parent(selection)
            selection = self.tree.parent(selection)
        if selection.startswith(self.CHAPTER_PREFIX):
            parent = self.tree.parent(selection)
            index = self.tree.index(selection) + 1
        elif selection.startswith(self.PART_PREFIX):
            parent = selection
        chId = create_id(self._ui.novel.chapters)
        newNode = f'{self.CHAPTER_PREFIX}{chId}'
        self._ui.novel.chapters[chId] = Chapter()
        title = kwargs.get('title', None)
        if title:
            self._ui.novel.chapters[chId].title = title
        else:
            self._ui.novel.chapters[chId].title = f'{_("New Chapter")} (ID{chId})'
        self._ui.novel.chapters[chId].chLevel = 0

        # Initialize custom keyword variables.
        for fieldName in self._ui.prjFile.CHP_KWVAR:
            self._ui.novel.chapters[chId].kwVar[fieldName] = None
        self._ui.novel.chapters[chId].kwVar['Field_NoNumber'] = kwargs.get('NoNumber', None)

        # Inherit part type, if "Todo" or "Notes".
        if self.tree.parent(parent).startswith(self.PL_ROOT):
            self._ui.novel.chapters[chId].chType = 2
        elif self.tree.parent(parent).startswith(self.RS_ROOT):
            self._ui.novel.chapters[chId].chType = 1
        else:
            self._ui.novel.chapters[chId].chType = kwargs.get('chType', 0)

        self._ui.novel.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.refresh_tree()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return chId

    def add_scene(self, **kwargs):
        """Add a Scene node to the tree and create an instance.
        
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Scene title. Default: Auto-generated title. 
            scType -- int: Scene type. Default: 0.
            status -- int: Scene status. Default: 1.
            appendToPrev -- boolean: Append to previous scene. Default: False.
            
        - Place the new node at the next free position after the selection, if possible.
        - Otherwise, do nothing. 
        
        Return the scene ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                return

        index = 0
        if selection.startswith(self.SCENE_PREFIX):
            parent = self.tree.parent(selection)
            index = self.tree.index(selection) + 1
        elif selection.startswith(self.CHAPTER_PREFIX):
            parent = selection
        elif selection.startswith(self.PART_PREFIX):
            parent = selection
        else:
            return

        scId = create_id(self._ui.novel.scenes)
        newNode = f'{self.SCENE_PREFIX}{scId}'
        self._ui.novel.scenes[scId] = Scene()
        title = kwargs.get('title', None)
        if title:
            self._ui.novel.scenes[scId].title = title
        else:
            self._ui.novel.scenes[scId].title = f'{_("New Scene")} (ID{scId})'
        self._ui.novel.scenes[scId].status = kwargs.get('status', 1)
        # Completion status = Outline by default
        self._ui.novel.scenes[scId].scType = kwargs.get('scType', 0)
        # Default type = Normal by default
        self._ui.novel.scenes[scId].appendToPrev = kwargs.get('appendToPrev', False)

        # Initialize custom keyword variables.
        for fieldName in self._ui.prjFile.SCN_KWVAR:
            self._ui.novel.scenes[scId].kwVar[fieldName] = None
        title, columns, nodeTags = self._set_scene_display(scId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return scId

    def add_character(self, **kwargs):
        """Add a Character node to the tree and create an instance.
        
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Element title. Default: Auto-generated title.
            isMajor -- boolean: If True, make the new character a major character. Default: False.
            
        - If the selection is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the first position.   

        Return the element's ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                selection = ''
        title = kwargs.get('title', None)
        isMajor = kwargs.get('isMajor', False)
        index = 0
        if selection.startswith(self.CHARACTER_PREFIX):
            index = self.tree.index(selection) + 1
        crId = create_id(self._ui.novel.characters)
        newNode = f'{self.CHARACTER_PREFIX}{crId}'
        self._ui.novel.characters[crId] = Character()
        if title:
            self._ui.novel.characters[crId].title = title
        else:
            self._ui.novel.characters[crId].title = f'{_("New Character")} (ID{crId})'
        self._ui.novel.characters[crId].isMajor = isMajor

        # Initialize custom keyword variables.
        for fieldName in self._ui.prjFile.CRT_KWVAR:
            self._ui.novel.characters[crId].kwVar[fieldName] = None
        title, columns, nodeTags = self._set_character_display(crId)
        self.tree.insert(self.CR_ROOT, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return crId

    def add_location(self, **kwargs):
        """Add a Location node to the tree and create an instance.
        
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Element title. Default: Auto-generated title. 
            
        - If the selection is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the first position.   

        Return the element's ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                selection = ''
        title = kwargs.get('title', None)
        index = 0
        if selection.startswith(self.LOCATION_PREFIX):
            index = self.tree.index(selection) + 1
        lcId = create_id(self._ui.novel.locations)
        newNode = f'{self.LOCATION_PREFIX}{lcId}'
        self._ui.novel.locations[lcId] = WorldElement()
        if title:
            self._ui.novel.locations[lcId].title = title
        else:
            self._ui.novel.locations[lcId].title = f'{_("New Location")} (ID{lcId})'

        # Initialize custom keyword variables.
        for fieldName in self._ui.prjFile.LOC_KWVAR:
            self._ui.novel.locations[lcId].kwVar[fieldName] = None
        title, columns, nodeTags = self._set_location_display(lcId)
        self.tree.insert(self.LC_ROOT, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return lcId

    def add_item(self, **kwargs):
        """Add a Item node to the tree and create an instance.
        
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Element title. Default: Auto-generated title. 
            
        - If the selection is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the first position.   

        Return the element's ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                selection = ''
        title = kwargs.get('title', None)
        index = 0
        if selection.startswith(self.ITEM_PREFIX):
            index = self.tree.index(selection) + 1
        itId = create_id(self._ui.novel.items)
        newNode = f'{self.ITEM_PREFIX}{itId}'
        self._ui.novel.items[itId] = WorldElement()
        if title:
            self._ui.novel.items[itId].title = title
        else:
            self._ui.novel.items[itId].title = f'{_("New Item")} (ID{itId})'

        # Initialize custom keyword variables.
        for fieldName in self._ui.prjFile.ITM_KWVAR:
            self._ui.novel.items[itId].kwVar[fieldName] = None
        title, columns, nodeTags = self._set_item_display(itId)
        self.tree.insert(self.IT_ROOT, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return itId

    def add_project_note(self, **kwargs):
        """Add a Project note node to the tree and create an instance.
        
        Keyword arguments:
            selection -- str: Tree position where to place a new node.
            title -- str: Element title. Default: Auto-generated title. 
            
        - If the selection is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the first position.   

        Return the element's ID, if successful.
        """
        if self._ui.check_lock():
            return

        selection = kwargs.get('selection', None)
        if not selection:
            try:
                selection = self.tree.selection()[0]
            except:
                selection = ''
        title = kwargs.get('title', None)
        index = 0
        if selection.startswith(self.PRJ_NOTE_PREFIX):
            index = self.tree.index(selection) + 1
        pnId = create_id(self._ui.novel.projectNotes)
        newNode = f'{self.PRJ_NOTE_PREFIX}{pnId}'
        self._ui.novel.projectNotes[pnId] = BasicElement()
        if title:
            self._ui.novel.projectNotes[pnId].title = title
        else:
            self._ui.novel.projectNotes[pnId].title = f'{_("New Note")} (ID{pnId})'

        title, columns, nodeTags = self._set_prjNote_display(pnId)
        self.tree.insert(self.PN_ROOT, index, newNode, text=title, values=columns, tags=nodeTags)
        self.update_prj_structure()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)
        return pnId

    def add_other_element(self):
        """Add a Character/Location/Item/Project note node to the tree and create an instance.
        
        This method is meant to be called by the context menu, so a node must be selected.
        """
        try:
            selection = self.tree.selection()[0]
        except:
            return

        if self.CHARACTER_PREFIX in selection:
            self.add_character()
        elif self.LOCATION_PREFIX in selection:
            self.add_location()
        elif self.ITEM_PREFIX in selection:
            self.add_item()
        elif self.PRJ_NOTE_PREFIX in selection:
            self.add_project_note()

    def join_scenes(self):
        """Join the selected scene with the previous one."""

        def join_str(prevText, thisText):
            if prevText is None:
                prevText = ''
            if thisText is None:
                thisText = ''
            if prevText or thisText:
                prevText = f'{prevText}\n{thisText}'.strip()
            return prevText

        def join_lst(prevList, thisList):
            if thisList:
                for elemId in thisList:
                    if not prevList:
                        prevList = []
                    if not elemId in prevList:
                        prevList.append(elemId)

        if self._ui.check_lock():
            return

        try:
            selection = self.tree.selection()[0]
        except:
            return

        if not selection.startswith(self.SCENE_PREFIX):
            return

        try:
            parent = self.tree.parent(selection)
            prevNode = self.prev_node(selection, parent)
            if not prevNode:
                raise Error(_('There is no previous scene in the chapter'))

            thisScId = selection[2:]
            prevScId = prevNode[2:]

            # Check type.
            if self._ui.novel.scenes[thisScId].scType != self._ui.novel.scenes[prevScId].scType:
                raise Error(_('The scenes are not of the same type'))

            # Check viewpoint.
            if self._ui.novel.scenes[thisScId].characters:
                if self._ui.novel.scenes[thisScId].characters:
                    if self._ui.novel.scenes[prevScId].characters:
                        if self._ui.novel.scenes[thisScId].characters[0] != self._ui.novel.scenes[prevScId].characters[0]:
                            raise Error(_('The scenes have different viewpoints'))

                    else:
                        self._ui.novel.scenes[prevScId].characters.append(self._ui.novel.scenes[thisScId].characters[0])

        except Error as ex:
            messagebox.showerror(_('Cannot join scenes'), str(ex))
            return

        # Join titles.
        joinedTitles = f'{self._ui.novel.scenes[prevScId].title} & {self._ui.novel.scenes[thisScId].title}'
        self._ui.novel.scenes[prevScId].title = joinedTitles

        # Join content.
        prevContent = self._ui.novel.scenes[prevScId].sceneContent
        thisContent = self._ui.novel.scenes[thisScId].sceneContent
        # this is because sceneContent is a property
        self._ui.novel.scenes[prevScId].sceneContent = join_str(prevContent, thisContent)

        # Join description, goal, conflict, outcome, notes.
        self._ui.novel.scenes[prevScId].desc = join_str(self._ui.novel.scenes[prevScId].desc, self._ui.novel.scenes[thisScId].desc)
        self._ui.novel.scenes[prevScId].goal = join_str(self._ui.novel.scenes[prevScId].goal, self._ui.novel.scenes[thisScId].goal)
        self._ui.novel.scenes[prevScId].conflict = join_str(self._ui.novel.scenes[prevScId].conflict, self._ui.novel.scenes[thisScId].conflict)
        self._ui.novel.scenes[prevScId].outcome = join_str(self._ui.novel.scenes[prevScId].outcome, self._ui.novel.scenes[thisScId].outcome)
        self._ui.novel.scenes[prevScId].notes = join_str(self._ui.novel.scenes[prevScId].notes, self._ui.novel.scenes[thisScId].notes)

        # Join characters, locations, items, tags.
        join_lst(self._ui.novel.scenes[prevScId].characters, self._ui.novel.scenes[thisScId].characters)
        join_lst(self._ui.novel.scenes[prevScId].locations, self._ui.novel.scenes[thisScId].locations)
        join_lst(self._ui.novel.scenes[prevScId].items, self._ui.novel.scenes[thisScId].items)
        join_lst(self._ui.novel.scenes[prevScId].tags, self._ui.novel.scenes[thisScId].tags)

        # Join arcs.
        arcs = string_to_list(self._ui.novel.scenes[prevScId].scnArcs)
        for arc in string_to_list(self._ui.novel.scenes[thisScId].scnArcs):
            if not arc in arcs:
                arcs.append(arc)
        self._ui.novel.scenes[prevScId].scnArcs = list_to_string(arcs)

        # Move arc point associations.
        pointIds = string_to_list(self._ui.novel.scenes[thisScId].kwVar.get('Field_SceneAssoc', None))
        for ptId in pointIds:
            self._ui.novel.scenes[ptId].kwVar['Field_SceneAssoc'] = prevScId

        # Add duration.
        try:
            thisLastsMin = int(self._ui.novel.scenes[thisScId].lastsMinutes)
        except:
            thisLastsMin = 0
        try:
            prevLastsMin = int(self._ui.novel.scenes[prevScId].lastsMinutes)
        except:
            prevLastsMin = 0
        hoursLeft, prevLastsMin = divmod((prevLastsMin + thisLastsMin), 60)
        self._ui.novel.scenes[prevScId].lastsMinutes = str(prevLastsMin)
        try:
            thisLastsHours = int(self._ui.novel.scenes[thisScId].lastsHours)
        except:
            thisLastsHours = 0
        try:
            prevLastsHours = int(self._ui.novel.scenes[prevScId].lastsHours)
        except:
            prevLastsHours = 0
        daysLeft, prevLastsHours = divmod((prevLastsHours + thisLastsHours + hoursLeft), 24)
        self._ui.novel.scenes[prevScId].lastsHours = str(prevLastsHours)
        try:
            thisLastsDays = int(self._ui.novel.scenes[thisScId].lastsDays)
        except:
            thisLastsDays = 0
        try:
            prevLastsDays = int(self._ui.novel.scenes[prevScId].lastsDays)
        except:
            prevLastsDays = 0
        prevLastsDays = prevLastsDays + thisLastsDays + daysLeft
        self._ui.novel.scenes[prevScId].lastsDays = str(prevLastsDays)

        # Remove selected scene from the chapter.
        chId = parent[2:]
        self._ui.novel.chapters[chId].srtScenes.remove(thisScId)

        # Remove selected scene from the tree.
        self.tree.delete(selection)

        # Delete selected scene instance.
        del(self._ui.novel.scenes[thisScId])
        self.update_prj_structure()
        self.tree.selection_set(prevNode)

    def open_children(self, parent):
        """Recursively show children nodes.
        
        Positional arguments:
            parent -- str: Root node of the subtree to open.
        """
        self.tree.item(parent, open=True)
        for child in self.tree.get_children(parent):
            self.open_children(child)

    def close_children(self, parent):
        """Recursively close children nodes.
        
        Positional arguments:
            parent -- str: Root node of the subtree to close.
        """
        self.tree.item(parent, open=False)
        for child in self.tree.get_children(parent):
            self.close_children(child)

    def show_chapters(self, parent):
        """Open Narrative/Part nodes and close chapter nodes.
        
        Positional arguments:
            parent -- str: Root node of the subtree to process.
        """
        if parent.startswith(self.CHAPTER_PREFIX):
            self.tree.item(parent, open=False)
        else:
            self.tree.item(parent, open=True)
            for child in self.tree.get_children(parent):
                self.show_chapters(child)

    def on_quit(self):
        """Write column width to the applicaton's keyword arguments."""
        self._ui.kwargs['title_width'] = self.tree.column('#0', 'width')
        for i, column in enumerate(self.columns):
            self._ui.kwargs[column[2]] = self.tree.column(i, 'width')

    def _set_scene_display(self, scId, position=None):
        """Configure scene formatting and columns."""
        title = self._ui.novel.scenes[scId].title
        if not title:
            title = _('Unnamed')

        # Date or day for displaying.
        if self._ui.novel.scenes[scId].date is not None and self._ui.novel.scenes[scId].date != Scene.NULL_DATE:
            dispDate = self._ui.novel.scenes[scId].date
        else:
            if self._ui.novel.scenes[scId].day is not None:
                dispDate = f'{_("Day")} {self._ui.novel.scenes[scId].day}'
            else:
                dispDate = ''

        # Time for displaying.
        if self._ui.novel.scenes[scId].time is not None:
            dispTime = self._ui.novel.scenes[scId].time.rsplit(':', 1)[0]
        else:
            dispTime = ''

        # Create arc point titles.
        points = []
        pointIds = string_to_list(self._ui.novel.scenes[scId].kwVar.get('Field_SceneAssoc', None))
        for ptId in pointIds:
            points.append(self._ui.novel.scenes[ptId].title)

        # Create a combined duration information.
        if self._ui.novel.scenes[scId].lastsDays and self._ui.novel.scenes[scId].lastsDays != '0':
            days = f'{self._ui.novel.scenes[scId].lastsDays}d '
        else:
            days = ''
        if self._ui.novel.scenes[scId].lastsHours and self._ui.novel.scenes[scId].lastsHours != '0':
            hours = f'{self._ui.novel.scenes[scId].lastsHours}h '
        else:
            hours = ''
        if self._ui.novel.scenes[scId].lastsMinutes and self._ui.novel.scenes[scId].lastsMinutes != '0':
            minutes = f'{self._ui.novel.scenes[scId].lastsMinutes}min'
        else:
            minutes = ''

        # Configure the columns depending on the scene type.
        columns = []
        for __ in self.columns:
            columns.append('')
        nodeTags = []
        if self._ui.novel.scenes[scId].scType == 2:
            #   is Todo type.
            nodeTags.append('todo')

            # Display the arc the point belongs to.
            arcs = self._ui.novel.scenes[scId].scnArcs
            if arcs is not None:
                columns[self._colPos['ac']] = arcs

            # Display associated scene(s), if any.
            columns[self._colPos['pt']] = list_to_string(points)

        elif self._ui.novel.scenes[scId].scType == 1:
            # Scene is Notes type.
            nodeTags.append('notes')
            columns[self._colPos['dt']] = dispDate
            columns[self._colPos['tm']] = dispTime
            columns[self._colPos['dr']] = f'{days}{hours}{minutes}'

        else:
            # Scene is Normal or Unused type.
            positionStr = ''
            if self._ui.novel.scenes[scId].scType == 3:
                nodeTags.append('unused')
            else:
                # Set the row color according to the color mode.
                if self._ui.kwargs['coloring_mode'] == _('status'):
                    nodeTags.append(Scene.STATUS[self._ui.novel.scenes[scId].status])
                elif self._ui.kwargs['coloring_mode'] == _('style'):
                    sceneStyle = self._ui.novel.scenes[scId].scnStyle
                    if sceneStyle:
                        nodeTags.append(sceneStyle)
                try:
                    positionStr = f'{round(100 * position / self._wordsTotal, 1)}%'
                except:
                    pass
            columns[self._colPos['po']] = positionStr
            columns[self._colPos['wc']] = self._ui.novel.scenes[scId].wordCount
            columns[self._colPos['st']] = self._SCN_STATUS[self._ui.novel.scenes[scId].status]
            sceneStyle = self._ui.novel.scenes[scId].scnStyle
            if sceneStyle:
                sceneStyle = _(sceneStyle)
            else:
                sceneStyle = _('staged')
            columns[self._colPos['sy']] = sceneStyle
            try:
                columns[self._colPos['vp']] = self._ui.novel.characters[self._ui.novel.scenes[scId].characters[0]].title
            except:
                columns[self._colPos['vp']] = _('N/A')
            if self._ui.novel.scenes[scId].kwVar.get('Field_CustomAR', None):
                columns[self._colPos['ar']] = _('C')
            elif self._ui.novel.scenes[scId].isReactionScene:
                columns[self._colPos['ar']] = _('R')
            else:
                columns[self._colPos['ar']] = _('A')

            columns[self._colPos['dt']] = dispDate
            columns[self._colPos['tm']] = dispTime
            columns[self._colPos['dr']] = f'{days}{hours}{minutes}'

            # Display arcs the scene belongs to.
            arcs = self._ui.novel.scenes[scId].scnArcs
            if arcs is not None:
                columns[self._colPos['ac']] = arcs

            # Display arc points, if any.
            columns[self._colPos['pt']] = list_to_string(points)

        # "Scene has notes" indicator.
        if self._ui.novel.scenes[scId].notes:
            columns[self._colPos['nt']] = _('N')

        # Scene tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._ui.novel.scenes[scId].tags)
        except:
            pass
        return title, columns, tuple(nodeTags)

    def _set_chapter_display(self, chId, position=None):
        """Configure chapter formatting and columns."""

        def count_words(chId):
            """Accumulate word counts of all relevant scenes in a chapter."""
            wordCount = 0
            if self._ui.novel.chapters[chId].chType in (0, 3):
                for scId in self._ui.novel.chapters[chId].srtScenes:
                    if self._ui.novel.scenes[scId].scType in (0, 3):
                        wordCount += self._ui.novel.scenes[scId].wordCount
            return wordCount

        def collect_viewpoints(chId):
            """Return a string with semicolon-separated viewpoint character names."""
            vpNames = []
            if self._ui.novel.chapters[chId].chType == 0:
                for scId in self._ui.novel.chapters[chId].srtScenes:
                    if self._ui.novel.scenes[scId].scType == 0:
                        try:
                            crId = self._ui.novel.scenes[scId].characters[0]
                            viewpoint = self._ui.novel.characters[crId].title
                            if not viewpoint in vpNames:
                                vpNames.append(viewpoint)
                        except:
                            pass
            return list_to_string(vpNames)

        def collect_tags(chId):
            """Return a string with semicolon-separated scene tags."""
            tags = []
            if self._ui.novel.chapters[chId].chType != 3:
                for scId in self._ui.novel.chapters[chId].srtScenes:
                    if self._ui.novel.scenes[scId].scType != 3:
                        if self._ui.novel.scenes[scId].tags:
                            for tag in self._ui.novel.scenes[scId].tags:
                                if not tag in tags:
                                    tags.append(tag)
            return list_to_string(tags)

        def collect_note_indicators(chId):
            """Return a string that indicates scene notes within the chapter."""
            indicator = ''
            if self._ui.novel.chapters[chId].chType != 3:
                for scId in self._ui.novel.chapters[chId].srtScenes:
                    if self._ui.novel.scenes[scId].scType != 3:
                        if self._ui.novel.scenes[scId].notes:
                            indicator = _('N')
            return indicator

        title = self._ui.novel.chapters[chId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')
        nodeTags = []
        if self._ui.novel.chapters[chId].chType == 1:
            # Chapter is Notes type.
            if self._ui.novel.chapters[chId].chLevel == 1:
                # This chapter begins a new section in ywriter.
                nodeTags.append('notes part')
            else:
                nodeTags.append('notes')
        elif self._ui.novel.chapters[chId].chType == 2:
            # Chapter is Todo type.
            if self._ui.novel.chapters[chId].chLevel == 1:
                # This chapter begins a new section in ywriter.
                nodeTags.append('todo part')
            else:
                nodeTags.append('todo')
                arc = self._ui.novel.chapters[chId].kwVar['Field_ArcDefinition']
                if arc:
                    wordCount = 0
                    for sid in self._ui.novel.scenes:
                        if self._ui.novel.scenes[sid].scType == 0:
                            if arc in string_to_list(self._ui.novel.scenes[sid].scnArcs):
                                wordCount += self._ui.novel.scenes[sid].wordCount
                    columns[self._colPos['wc']] = wordCount
        elif self._ui.novel.chapters[chId].chType == 3:
            # Chapter is Unused type.
            nodeTags.append('unused')
        else:
            # Chapter is Normal type (or other).
            nodeTags.append('chapter')
            try:
                positionStr = f'{round(100 * position / self._wordsTotal, 1)}%'
            except:
                positionStr = ''
            wordCount = count_words(chId)
            if self._ui.novel.chapters[chId].chLevel == 1:
                # This chapter begins a new section in ywriter.
                nodeTags.append('part')
                # Add all scene wordcounts until the next part.
                i = self._ui.novel.srtChapters.index(chId) + 1
                while i < len(self._ui.novel.srtChapters):
                    c = self._ui.novel.srtChapters[i]
                    if self._ui.novel.chapters[c].chLevel == 1:
                        break
                    i += 1
                    wordCount += count_words(c)
            columns[self._colPos['wc']] = wordCount
            columns[self._colPos['po']] = positionStr
            columns[self._colPos['vp']] = collect_viewpoints(chId)
        columns[self._colPos['tg']] = collect_tags(chId)
        columns[self._colPos['nt']] = collect_note_indicators(chId)
        return title, columns, tuple(nodeTags)

    def _set_character_display(self, crId):
        """Configure character formatting and columns."""
        title = self._ui.novel.characters[crId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        if self._ui.novel.characters[crId].notes:
            columns[self._colPos['nt']] = _('N')

        # Count the scenes that use this character as viewpoint.
        wordCount = 0
        for scId in self._ui.novel.scenes:
            if self._ui.novel.scenes[scId].scType == 0:
                if self._ui.novel.scenes[scId].characters:
                    if self._ui.novel.scenes[scId].characters[0] == crId:
                        wordCount += self._ui.novel.scenes[scId].wordCount
        if wordCount > 0:
            columns[self._colPos['wc']] = wordCount

            # Words percentage per viewpoint character
            try:
                percentageStr = f'{round(100 * wordCount / self._wordsTotal, 1)}%'
            except:
                percentageStr = ''
            columns[self._colPos['vp']] = percentageStr

        # Tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._ui.novel.characters[crId].tags)
        except:
            pass

        # Set color according to the character's status.
        nodeTags = []
        if self._ui.novel.characters[crId].isMajor:
            nodeTags.append('major')
        else:
            nodeTags.append('minor')
        return title, columns, tuple(nodeTags)

    def _set_location_display(self, lcId):
        """Configure location formatting and columns."""
        title = self._ui.novel.locations[lcId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        # Tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._ui.novel.locations[lcId].tags)
        except:
            pass
        nodeTags = []
        return title, columns, tuple(nodeTags)

    def _set_item_display(self, itId):
        """Configure item formatting and columns."""
        title = self._ui.novel.items[itId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        # tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._ui.novel.items[itId].tags)
        except:
            pass
        nodeTags = []
        return title, columns, tuple(nodeTags)

    def _set_prjNote_display(self, pnId):
        """Configure project note formatting and columns."""
        title = self._ui.novel.projectNotes[pnId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')
        nodeTags = []
        return title, columns, tuple(nodeTags)

    def _open_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.focus_set()
            self.tree.selection_set(row)
            prefix = row[:2]
            if prefix in (self.NV_ROOT, self.RS_ROOT, self.PL_ROOT, self.PART_PREFIX, self.CHAPTER_PREFIX, self.SCENE_PREFIX):
                # Context is within the "Narrative" or the "Research" subtree.
                if self._ui.isLocked:
                    # No changes allowed.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Style'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Scene'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Cancel Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Demote Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                elif prefix.startswith(self.NV_ROOT):
                    # Context is the "Narrative" subtree.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Set Style'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Scene'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Cancel Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Demote Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                elif prefix.startswith(self.RS_ROOT):
                    # Context is the "Research" subtree.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Style'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Scene'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Cancel Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Demote Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                elif prefix.startswith(self.PL_ROOT):
                    # Context is the "Planning" subtree.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Style'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Scene'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Cancel Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Demote Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                else:
                    # Context is a part/chapter/scene.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Set Style'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Scene'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='normal')
                    if prefix.startswith(self.PART_PREFIX):
                        # Context is a part.
                        self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                        self._nvCtxtMenu.entryconfig(_('Cancel Part'), state='normal')
                        self._nvCtxtMenu.entryconfig(_('Demote Part'), state='normal')
                    else:
                        self._nvCtxtMenu.entryconfig(_('Cancel Part'), state='disabled')
                        self._nvCtxtMenu.entryconfig(_('Demote Part'), state='disabled')
                    if prefix.startswith(self.CHAPTER_PREFIX):
                        # Context is a chapter.
                        self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                        if row != self._trashNode:
                            # Context is a regular chapter.
                            self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='normal')
                        else:
                            # Context is the "Trash" chapter.
                            self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Add Scene'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Add Part'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Set Style'), state='disabled')
                    else:
                        self._nvCtxtMenu.entryconfig(_('Promote Chapter'), state='disabled')
                    if prefix.startswith(self.SCENE_PREFIX):
                        # Context is a scene.
                        self._nvCtxtMenu.entryconfig(_('Join with previous'), state='normal')
                try:
                    self._nvCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._nvCtxtMenu.grab_release()
            elif prefix in ('wr', self.CHARACTER_PREFIX, self.LOCATION_PREFIX, self.ITEM_PREFIX, self.PRJ_NOTE_PREFIX):
                # Context is character/location/item.
                if self._ui.isLocked:
                    # No changes allowed.
                    self._wrCtxtMenu.entryconfig(_('Add'), state='disabled')
                    self._wrCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._wrCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                else:
                    self._wrCtxtMenu.entryconfig(_('Add'), state='normal')
                    if prefix.startswith('wr'):
                        # Context is the root of a world element type subtree.
                        self._wrCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    else:
                        # Context is a world element.
                        self._wrCtxtMenu.entryconfig(_('Delete'), state='normal')
                    if prefix.startswith(self.CHARACTER_PREFIX) or  row.endswith(self.CHARACTER_PREFIX):
                        # Context is a character.
                        self._wrCtxtMenu.entryconfig(_('Set Status'), state='normal')
                    else:
                        # Context is not a character.
                        self._wrCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                try:
                    self._wrCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._wrCtxtMenu.grab_release()

    def _set_type(self, nodes, newType):
        """Recursively set scene or chapter type (Normal/Notes/Todo/Unused).
        
        nodes must be an iterable.
        """
        if self._ui.check_lock():
            return

        has_changed = False
        for node in nodes:
            if node.startswith(self.SCENE_PREFIX):
                scene = self._ui.novel.scenes[node[2:]]
                if scene.scType != newType:
                    scene.scType = newType
                    has_changed = True
            elif node.startswith(self.CHAPTER_PREFIX) or node.startswith(self.PART_PREFIX):
                self.tree.item(node, open=True)
                chapter = self._ui.novel.chapters[node[2:]]
                if chapter.isTrash:
                    newType = 3
                if chapter.chType != newType:
                    chapter.chType = newType
                    has_changed = True

                # Go one level down.
                self._set_type(self.tree.get_children(node), newType)
        if has_changed:
            self.update_prj_structure()
            self.refresh_tree()

    def _set_scn_status(self, nodes, scnStatus):
        """Recursively set scene editing status (Outline/Draft..)."""
        if self._ui.check_lock():
            return

        has_changed = False
        for node in nodes:
            if node.startswith(self.SCENE_PREFIX):
                if  self._ui.novel.scenes[node[2:]].status != scnStatus:
                    self._ui.novel.scenes[node[2:]].status = scnStatus
                    has_changed = True
            elif node.startswith(self.CHAPTER_PREFIX) or node.startswith(self.PART_PREFIX) or node.startswith(self.NV_ROOT):
                self.tree.item(node, open=True)

                # Go one level down.
                self._set_scn_status(self.tree.get_children(node), scnStatus)
        if has_changed:
            self.update_prj_structure()
            self.refresh_tree()

    def _set_scn_style(self, nodes, scnStyle):
        """Set scene narrative mode (Scene/Description/summary)."""
        if self._ui.check_lock():
            return

        has_changed = False
        for node in nodes:
            if node.startswith(self.SCENE_PREFIX):
                if  self._ui.novel.scenes[node[2:]].scnStyle != scnStyle:
                    self._ui.novel.scenes[node[2:]].scnStyle = scnStyle
                    has_changed = True
            elif node.startswith(self.CHAPTER_PREFIX) or node.startswith(self.PART_PREFIX) or node.startswith(self.NV_ROOT):
                self.tree.item(node, open=True)

                # Go one level down.
                self._set_scn_style(self.tree.get_children(node), scnStyle)
        if has_changed:
            self.update_prj_structure()

    def _set_chr_status(self, chrStatus):
        """Set character status (Major/Minor)."""
        if self._ui.check_lock():
            return

        has_changed = False
        nodes = self.tree.selection()
        for node in nodes:
            if node.startswith(self.CHARACTER_PREFIX):
                if self._ui.novel.characters[node[2:]].isMajor != chrStatus:
                    self._ui.novel.characters[node[2:]].isMajor = chrStatus
                    has_changed = True
            elif node.endswith(self.CHARACTER_PREFIX):
                # Go one level down.
                for childNode in self.tree.get_children(node):
                    self._set_chr_status(childNode, chrStatus)
                has_changed = True
        if has_changed:
            self.update_prj_structure()

    def _move_node(self, event):
        """Move a selected node in the novel tree."""
        if self._ui.isLocked:
            return

        node = self.tree.selection()[0]
        if node == self._trashNode:
            return

        targetNode = self.tree.identify_row(event.y)
        # self.tree.item(targetNode, open=True)
        if node[:2] == targetNode[:2]:
            self.tree.move(node, self.tree.parent(targetNode), self.tree.index(targetNode))
        elif node.startswith(self.SCENE_PREFIX) and targetNode.startswith(self.CHAPTER_PREFIX) and not self.tree.get_children(targetNode):
            self.tree.move(node, targetNode, 0)
        elif node.startswith(self.SCENE_PREFIX) and targetNode.startswith(self.PART_PREFIX):
            self.tree.move(node, targetNode, 0)
        elif node.startswith(self.CHAPTER_PREFIX) and targetNode.startswith(self.PART_PREFIX) and not self.tree.get_children(targetNode):
            self.tree.move(node, targetNode, self.tree.index(targetNode))
        self.update_prj_structure()

    def _cancel_part(self, event):
        """Remove a part but keep its chapters."""
        if self._ui.check_lock():
            return

        selection = self.tree.selection()[0]
        if not selection.startswith(self.PART_PREFIX):
            return
        elemId = selection[2:]
        if self._ui.ask_yes_no(_('Remove part "{}" and keep the chapters?').format(self._ui.novel.chapters[elemId].title)):
            if self.tree.prev(selection):
                self.tree.selection_set(self.tree.prev(selection))
            else:
                self.tree.selection_set(self.tree.parent(selection))
            del self._ui.novel.chapters[elemId]
            self._ui.novel.srtChapters.remove(elemId)
            self.update_prj_structure()
            self.refresh_tree()

    def _promote_chapter(self, event):
        """Make a chapter a part."""
        if self._ui.check_lock():
            return

        selection = self.tree.selection()[0]
        if not selection.startswith(self.CHAPTER_PREFIX):
            return
        elemId = selection[2:]
        if self._ui.novel.chapters[elemId].isTrash:
            return

        if self._ui.ask_yes_no(_('Promote chapter "{}" to part?').format(self._ui.novel.chapters[elemId].title)):
            self._ui.novel.chapters[elemId].chLevel = 1
            self.update_prj_structure()
            self.refresh_tree()

    def _demote_part(self, event):
        """Make a part a chapter."""
        if self._ui.check_lock():
            return

        selection = self.tree.selection()[0]
        if not selection.startswith(self.PART_PREFIX):
            return
        elemId = selection[2:]
        if self._ui.ask_yes_no(_('Demote part "{}" to chapter?').format(self._ui.novel.chapters[elemId].title)):
            self._ui.novel.chapters[elemId].chLevel = 0
            self.update_prj_structure()
            self.refresh_tree()

    def _delete_node(self, event):
        """Delete a node and its children.
        
        Move scenes to the "Trash" chapter.
        Delete parts/chapters and move their children scenes to the "Trash" chapter.
        Delete characters/locations/items and remove their scene references.
        """

        def waste_scenes(node):
            """Move all scenes under the node to the 'trash bin'."""
            if node.startswith(self.SCENE_PREFIX):
                scId = node[2:]
                self._ui.novel.scenes[scId].scType = 3
                # Move scene.
                self.tree.move(node, self._trashNode, 0)
            else:
                # Delete chapter and go one level down.
                chId = node[2:]
                del self._ui.novel.chapters[chId]
                if chId in self._ui.novel.srtChapters:
                    self._ui.novel.srtChapters.remove(chId)
                for childNode in self.tree.get_children(node):
                    waste_scenes(childNode)

        if self._ui.check_lock():
            return

        for  selection in self.tree.selection():
            elemId = selection[2:]
            if selection.startswith(self.SCENE_PREFIX):
                candidate = f'{_("Scene")} "{self._ui.novel.scenes[elemId].title}"'
            elif selection.startswith(self.CHAPTER_PREFIX):
                candidate = f'{_("Chapter")} "{self._ui.novel.chapters[elemId].title}"'
            elif selection.startswith(self.PART_PREFIX):
                candidate = f'{_("Part")} "{self._ui.novel.chapters[elemId].title}"'
            elif selection.startswith(self.CHARACTER_PREFIX):
                candidate = f'{_("Character")} "{self._ui.novel.characters[elemId].title}"'
            elif selection.startswith(self.LOCATION_PREFIX):
                candidate = f'{_("Location")} "{self._ui.novel.locations[elemId].title}"'
            elif selection.startswith(self.ITEM_PREFIX):
                candidate = f'{_("Item")} "{self._ui.novel.items[elemId].title}"'
            elif selection.startswith(self.PRJ_NOTE_PREFIX):
                candidate = f'{_("Project note")} "{self._ui.novel.projectNotes[elemId].title}"'
            else:
                return

            if not self._ui.ask_yes_no(_('Delete {}?').format(candidate)):
                return

            if self.tree.prev(selection):
                self.tree.selection_set(self.tree.prev(selection))
            else:
                self.tree.selection_set(self.tree.parent(selection))
            if selection == self._trashNode:
                # Remove the "trash bin".
                self.tree.delete(selection)
                self._trashNode = None
                for scId in self._ui.novel.chapters[elemId].srtScenes:
                    del self._ui.novel.scenes[scId]
                self._ui.novel.chapters[elemId].srtScenes = []
                del self._ui.novel.chapters[elemId]
                if elemId in self._ui.novel.srtChapters:
                    self._ui.novel.srtChapters.remove(elemId)
            elif selection.startswith(self.CHARACTER_PREFIX):
                # Delete a character and remove references.
                self.tree.delete(selection)
                del self._ui.novel.characters[elemId]
                for scId in self._ui.novel.scenes:
                    try:
                        self._ui.novel.scenes[scId].characters.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self.LOCATION_PREFIX):
                # Delete a location and remove references.
                self.tree.delete(selection)
                del self._ui.novel.locations[elemId]
                for scId in self._ui.novel.scenes:
                    try:
                        self._ui.novel.scenes[scId].locations.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self.ITEM_PREFIX):
                # Delete an item and remove references.
                self.tree.delete(selection)
                del self._ui.novel.items[elemId]
                for scId in self._ui.novel.scenes:
                    try:
                        self._ui.novel.scenes[scId].items.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self.PRJ_NOTE_PREFIX):
                # Delete a project note and remove references.
                self.tree.delete(selection)
                del self._ui.novel.projectNotes[elemId]
            else:
                # Part/chapter/scene selected.
                if self._trashNode is None:
                    # Create a "trash bin"; use the first free chapter ID.
                    trashId = create_id(self._ui.novel.chapters)
                    self._ui.novel.chapters[trashId] = Chapter()
                    for fieldName in self._ui.prjFile.CHP_KWVAR:
                        self._ui.novel.chapters[trashId].kwVar[fieldName] = None
                    self._ui.novel.chapters[trashId].title = _('Trash')
                    self._ui.novel.chapters[trashId].isTrash = True
                    self._trashNode = f'{self.CHAPTER_PREFIX}{trashId}'
                    self.tree.insert(self.NV_ROOT, 'end', self._trashNode, text=_('Trash'), tags='unused', open=True)
                if selection.startswith(self.SCENE_PREFIX):
                    if self.tree.parent(selection) == self._trashNode:
                        # Remove scene, if already in trash bin.
                        self.tree.delete(selection)
                        del self._ui.novel.scenes[elemId]
                    else:
                        # Move scene to the "trash bin".
                        waste_scenes(selection)
                else:
                    # Delete part/chapter and move child scenes to the "trash bin".
                    waste_scenes(selection)
                    self.tree.delete(selection)
                # Make sure the whole "trash bin" is unused.
                self._set_type([self._trashNode], 3)
            self.update_prj_structure()

    def _on_select_node(self, event):
        try:
            nodeId = self.tree.selection()[0]
            if nodeId.startswith(self.SCENE_PREFIX):
                self._ui.view_scene(nodeId[2:])
            elif nodeId.startswith(self.CHAPTER_PREFIX):
                self._ui.view_chapter(nodeId[2:])
            elif nodeId.startswith(self.PART_PREFIX):
                self._ui.view_chapter(nodeId[2:])
            elif nodeId.startswith(self.NV_ROOT):
                self._ui.view_narrative()
            elif nodeId.startswith(self.CHARACTER_PREFIX):
                self._ui.view_character(nodeId[2:])
            elif nodeId.startswith(self.LOCATION_PREFIX):
                self._ui.view_location(nodeId[2:])
            elif nodeId.startswith(self.ITEM_PREFIX):
                self._ui.view_item(nodeId[2:])
            elif nodeId.startswith(self.PRJ_NOTE_PREFIX):
                self._ui.view_projectNote(nodeId[2:])
            else:
                self._ui.view_nothing()
        except IndexError:
            pass

