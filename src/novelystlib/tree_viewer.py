""""Provide a tkinter tree view class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from pywriter.model.id_generator import create_id
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.world_element import WorldElement


class TreeViewer:
    """A tkinter class for yWriter tree view.
    
    Public methods:
        build_tree -- Create and display the tree.
        reset_tree -- Clear the displayed tree.
        open_children -- Recursively open children nodes.
        close_children -- Recursively close children nodes.
        add_part -- Add a Part node to the tree and create an instance.
        add_chapter -- Add a Chapter node to the tree and create an instance.
        add_scene -- Add a Scene node to the tree and create an instance.
        add_world_element -- Add a Character/Location/Item node to the tree and create an instance.
        on_quit -- Write column width to the applicaton's keyword arguments.
    
    Public instance variables:
        tree -- tk Treeview instance.   
    """
    _COLUMNS = (
        ('Words', 'wc_width'),
        ('Status', 'status_width'),
        ('Viewpoint', 'vp_width'),
        ('Tags', 'tags_width'),
        ('A/R', 'pacing_width'),
        ('Date', 'date_width'),
        ('Time', 'time_width'),
        ('Duration', 'duration_width'),
        ('Arcs', 'arcs_width'),
        ('', 'sizer_width'),
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
    NV_ROOT = 'nv'
    # Root of the Narrative subtree
    RS_ROOT = 'rs'
    # Root of the Research subtree
    CR_ROOT = f'wr{_CR}'
    # Root of the Characters subtree
    LC_ROOT = f'wr{_LC}'
    # Root of the Locations subtree
    IT_ROOT = f'wr{_IT}'
    # Root of the Items subtree

    _KEY_CANCEL_PART = '<Shift-Delete>'
    _KEY_DEMOTE_PART = '<Shift-Right>'
    _KEY_PROMOTE_CHAPTER = '<Shift-Left>'

    _ARCS_TITLE = 'Arcs'
    # Title of the chapter containing the arc definitions

    def __init__(self, ui, window, **kwargs):
        """Put a text box to the GUI main window.
        
        Positional arguments:
            ui -- GUI class reference.
            window -- parent window for displaying the tree view.
        
        Required keyword arguments:
            button_context_menu -- str: Mouse button to open the treeveiw context menu.
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
        self._ui = ui

        # Create a novel tree.
        self.tree = ttk.Treeview(window, selectmode='browse')
        scrollY = ttk.Scrollbar(window, orient="vertical", command=self.tree.yview)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollY.set)
        window.add(self.tree)
        self._trashNode = None

        # Add columns to the tree.
        columns = []
        for column in self._COLUMNS:
            columns.append(column[0])
        self.tree.configure(columns=tuple(columns))
        for column in self._COLUMNS:
            self.tree.heading(column[0], text=column[0], anchor='w')
            self.tree.column(column[0], width=int(kwargs[column[1]]), minwidth=40, stretch='No')

        #--- Create a scene type submenu.
        self._typeMenu = tk.Menu(self.tree, tearoff=0)
        self._typeMenu.add_command(label='Normal', command=lambda: self._set_type(self.tree.selection()[0], 0))
        self._typeMenu.add_command(label='Notes', command=lambda: self._set_type(self.tree.selection()[0], 1))
        self._typeMenu.add_command(label='Todo', command=lambda: self._set_type(self.tree.selection()[0], 2))
        self._typeMenu.add_command(label='Unused', command=lambda: self._set_type(self.tree.selection()[0], 3))

        #--- Create a scene scene status submenu.
        self._scStatusMenu = tk.Menu(self.tree, tearoff=0)
        self._scStatusMenu.add_command(label='Outline', command=lambda: self._set_scn_status(self.tree.selection()[0], 1))
        self._scStatusMenu.add_command(label='Draft', command=lambda: self._set_scn_status(self.tree.selection()[0], 2))
        self._scStatusMenu.add_command(label='1st Edit', command=lambda: self._set_scn_status(self.tree.selection()[0], 3))
        self._scStatusMenu.add_command(label='2nd Edit', command=lambda: self._set_scn_status(self.tree.selection()[0], 4))
        self._scStatusMenu.add_command(label='Done', command=lambda: self._set_scn_status(self.tree.selection()[0], 5))

        #--- Create a narrative context menu.
        self._nvCtxtMenu = tk.Menu(self.tree, tearoff=0)
        self._nvCtxtMenu.add_command(label='Add Scene', command=self.add_scene)
        self._nvCtxtMenu.add_command(label='Add Chapter', command=self.add_chapter)
        self._nvCtxtMenu.add_command(label='Promote Chapter', command=lambda: self.tree.event_generate(self._KEY_PROMOTE_CHAPTER, when='tail'))
        self._nvCtxtMenu.add_command(label='Add Part', command=self.add_part)
        self._nvCtxtMenu.add_command(label='Demote Part', command=lambda: self.tree.event_generate(self._KEY_DEMOTE_PART, when='tail'))
        self._nvCtxtMenu.add_command(label='Cancel Part', command=lambda: self.tree.event_generate(self._KEY_CANCEL_PART, when='tail'))
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label='Delete', command=lambda: self.tree.event_generate('<Delete>', when='tail'))
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_cascade(label='Set Type', menu=self._typeMenu)
        self._nvCtxtMenu.add_cascade(label='Set Status', menu=self._scStatusMenu)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label='Expand', command=lambda: self.open_children(self.tree.selection()[0]))
        self._nvCtxtMenu.add_command(label='Collapse', command=lambda: self.close_children(self.tree.selection()[0]))
        self._nvCtxtMenu.add_command(label='Expand all', command=lambda: self.open_children(''))
        self._nvCtxtMenu.add_command(label='Collapse all', command=lambda: self.close_children(''))

        #--- Create a character status submenu.
        self._crStatusMenu = tk.Menu(self.tree, tearoff=0)
        self._crStatusMenu.add_command(label='MajorCharacter', command=lambda: self._set_chr_status(True))
        self._crStatusMenu.add_command(label='MinorCharacter', command=lambda: self._set_chr_status(False))

        #--- Create a world element context menu.
        self._wrCtxtMenu = tk.Menu(self.tree, tearoff=0)
        self._wrCtxtMenu.add_command(label='Add', command=lambda: self.add_world_element())
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_command(label='Delete', command=lambda: self.tree.event_generate('<Delete>', when='tail'))
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_cascade(label='Set Status', menu=self._crStatusMenu)

        #--- configure tree row display.
        fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']
        self.tree.tag_configure('root', font=('', fontSize, 'bold'))
        self.tree.tag_configure('chapter', foreground=kwargs['color_chapter'])
        self.tree.tag_configure('unused', foreground=kwargs['color_unused'])
        self.tree.tag_configure('notes', foreground=kwargs['color_notes'])
        self.tree.tag_configure('todo', foreground=kwargs['color_todo'])
        self.tree.tag_configure('part', font=('', fontSize, 'bold'))
        self.tree.tag_configure('notes part', font=('', fontSize, 'bold'), foreground=kwargs['color_notes'])
        self.tree.tag_configure('major', foreground=kwargs['color_major'])
        self.tree.tag_configure('minor', foreground=kwargs['color_minor'])
        self.tree.tag_configure('Outline', foreground=kwargs['color_outline'])
        self.tree.tag_configure('Draft', foreground=kwargs['color_draft'])
        self.tree.tag_configure('1st Edit', foreground=kwargs['color_1st_edit'])
        self.tree.tag_configure('2nd Edit', foreground=kwargs['color_2nd_edit'])
        self.tree.tag_configure('Done', foreground=kwargs['color_done'])

        #--- Event bindings.
        self.tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self.tree.bind('<Shift-B1-Motion>', self._move_node)
        self.tree.bind('<Delete>', self._delete_node)
        self.tree.bind(self._KEY_CANCEL_PART, self._cancel_part)
        self.tree.bind(self._KEY_DEMOTE_PART, self._demote_part)
        self.tree.bind(self._KEY_PROMOTE_CHAPTER, self._promote_chapter)
        self.tree.bind(kwargs['button_context_menu'], self._open_context_menu)

    def _open_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.focus_set()
            self.tree.selection_set(row)
            prefix = row[:2]
            if prefix in (self.NV_ROOT, self.RS_ROOT, self._PT, self._CH, self._SC):
                # Context is narrative/part/chapter/scene.
                if self._ui.isLocked:
                    self._nvCtxtMenu.entryconfig('Delete', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Type', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Status', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Cancel Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Demote Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Promote Chapter', state='disabled')
                elif prefix.startswith(self.NV_ROOT):
                    self._nvCtxtMenu.entryconfig('Delete', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Type', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Status', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Part', state='normal')
                    self._nvCtxtMenu.entryconfig('Cancel Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Demote Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Promote Chapter', state='disabled')
                elif prefix.startswith(self.RS_ROOT):
                    self._nvCtxtMenu.entryconfig('Delete', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Type', state='disabled')
                    self._nvCtxtMenu.entryconfig('Set Status', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='disabled')
                    self._nvCtxtMenu.entryconfig('Add Part', state='normal')
                    self._nvCtxtMenu.entryconfig('Cancel Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Demote Part', state='disabled')
                    self._nvCtxtMenu.entryconfig('Promote Chapter', state='disabled')
                else:
                    self._nvCtxtMenu.entryconfig('Delete', state='normal')
                    self._nvCtxtMenu.entryconfig('Set Type', state='normal')
                    self._nvCtxtMenu.entryconfig('Set Status', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Scene', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Chapter', state='normal')
                    self._nvCtxtMenu.entryconfig('Add Part', state='normal')
                    if prefix.startswith(self._PT):
                        self._nvCtxtMenu.entryconfig('Cancel Part', state='normal')
                        self._nvCtxtMenu.entryconfig('Demote Part', state='normal')
                    else:
                        self._nvCtxtMenu.entryconfig('Cancel Part', state='disabled')
                        self._nvCtxtMenu.entryconfig('Demote Part', state='disabled')
                    if prefix.startswith(self._CH):
                        self._nvCtxtMenu.entryconfig('Promote Chapter', state='normal')
                    else:
                        self._nvCtxtMenu.entryconfig('Promote Chapter', state='disabled')
                try:
                    self._nvCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._nvCtxtMenu.grab_release()
            elif prefix in ('wr', self._CR, self._LC, self._IT):
                # Context is character/location/item.
                if self._ui.isLocked:
                    self._wrCtxtMenu.entryconfig('Add', state='disabled')
                    self._wrCtxtMenu.entryconfig('Delete', state='disabled')
                    self._wrCtxtMenu.entryconfig('Set Status', state='disabled')
                else:
                    self._wrCtxtMenu.entryconfig('Add', state='normal')
                    if prefix.startswith('wr'):
                        self._wrCtxtMenu.entryconfig('Delete', state='disabled')
                    else:
                        self._wrCtxtMenu.entryconfig('Delete', state='normal')
                    if (prefix.startswith(self._CR) or  row.endswith(self._CR)) and not self._ui.isLocked:
                        self._wrCtxtMenu.entryconfig('Set Status', state='normal')
                    else:
                        self._wrCtxtMenu.entryconfig('Set Status', state='disabled')
                try:
                    self._wrCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._wrCtxtMenu.grab_release()

    def refresh_tree(self):
        """Refresh the tree.
        
        Display the tree nodes regarding the way they are read from the file.
        """
        modifiedNodes = []
        isModified = self._ui.isModified
        if self._ui.ywPrj.renumber_chapters():
            isModified = True
        for chId in self._ui.ywPrj.chapters:
            chType = self._ui.ywPrj.chapters[chId].chType
            for scId in self._ui.ywPrj.chapters[chId].srtScenes:
                if chType == 1:
                    if not self._ui.ywPrj.scenes[scId].isNotesScene:
                        self._ui.ywPrj.scenes[scId].isNotesScene = True
                        isModified = True
                        modifiedNodes.append(f'{self._SC}{scId}')
                elif chType == 2:
                    if not self._ui.ywPrj.scenes[scId].isTodoScene:
                        self._ui.ywPrj.scenes[scId].isTodoScene = True
                        self._ui.ywPrj.scenes[scId].isNotesScene = False
                        isModified = True
                        modifiedNodes.append(f'{self._SC}{scId}')
        self.build_tree()
        self._ui.isModified = isModified
        for node in modifiedNodes:
            self.tree.see(node)

    def build_tree(self):
        """Create and display the tree."""
        self.reset_tree()

        #--- Build Parts/Chapters/scenes tree.
        self.tree.insert('', 'end', self.NV_ROOT, text='Narrative', tags='root', open=True)
        self.tree.insert('', 'end', self.RS_ROOT, text='Research', tags='root', open=True)
        inPart = False
        inNotesPart = False
        for chId in self._ui.ywPrj.srtChapters:
            if self._ui.ywPrj.chapters[chId].isTrash:
                self._trashNode = f'{self._CH}{chId}'
                inPart = False
            if self._ui.ywPrj.chapters[chId].chLevel == 1:
                # Part begins.
                inPart = True
                inChapter = False
                if self._ui.ywPrj.chapters[chId].chType == 1:
                    # "Notes" part begins.
                    inNotesPart = True
                    parent = self.RS_ROOT
                else:
                    inNotesPart = False
                    parent = self.NV_ROOT
                title, columns, nodeTags = self._set_chapter_display(chId)
                partNode = self.tree.insert(parent, 'end', f'{self._PT}{chId}', text=title, values=columns, tags=nodeTags, open=True)
            else:
                # Chapter begins.
                inChapter = True
                if self._ui.ywPrj.chapters[chId].chType != 1:
                    # Regular chapter can not be in "Notes" part.
                    if inNotesPart:
                        inNotesPart = False
                        inPart = False
                if inPart:
                    parentNode = partNode
                else:
                    parentNode = self.NV_ROOT
                title, columns, nodeTags = self._set_chapter_display(chId)
                chapterNode = self.tree.insert(parentNode, 'end', f'{self._CH}{chId}', text=title, values=columns, tags=nodeTags)
            for scId in self._ui.ywPrj.chapters[chId].srtScenes:
                title, columns, nodeTags = self._set_scene_display(scId)
                if inChapter:
                    parentNode = chapterNode
                else:
                    parentNode = partNode
                self.tree.insert(parentNode, 'end', f'{self._SC}{scId}', text=title, values=columns, tags=nodeTags)

        #--- Build character tree.
        self.tree.insert('', 'end', self.CR_ROOT, text='Characters', tags='root', open=False)
        for crId in self._ui.ywPrj.srtCharacters:
            title, columns, nodeTags = self._set_character_display(crId)
            self.tree.insert(self.CR_ROOT, 'end', f'{self._CR}{crId}', text=title, values=columns, tags=nodeTags)

        #--- Build location tree.
        self.tree.insert('', 'end', self.LC_ROOT, text='Locations', tags='root', open=False)
        for lcId in self._ui.ywPrj.srtLocations:
            title, columns, nodeTags = self._set_location_display(lcId)
            self.tree.insert(self.LC_ROOT, 'end', f'{self._LC}{lcId}', text=title, values=columns, tags=nodeTags)

        #--- Build item tree.
        self.tree.insert('', 'end', self.IT_ROOT, text='Items', tags='root', open=False)
        for itId in self._ui.ywPrj.srtItems:
            title, columns, nodeTags = self._set_item_display(itId)
            self.tree.insert(self.IT_ROOT, 'end', f'{self._IT}{itId}', text=title, values=columns, tags=nodeTags)

    def _update_tree(self):
        """Rebuild the sorted lists."""

        def update_node(node, chId):
            """Recursive tree builder."""
            for childNode in self.tree.get_children(node):
                if childNode.startswith(self._SC):
                    scId = childNode[2:]
                    self._ui.ywPrj.chapters[chId].srtScenes.append(scId)
                    if self._ui.ywPrj.scenes[scId].isTodoScene:
                        title, columns, nodeTags = self._set_arc_display(scId)
                    else:
                        title, columns, nodeTags = self._set_scene_display(scId)
                elif childNode.startswith(self._CR):
                    crId = childNode[2:]
                    self._ui.ywPrj.srtCharacters.append(crId)
                    title, columns, nodeTags = self._set_character_display(crId)
                elif childNode.startswith(self._LC):
                    lcId = childNode[2:]
                    self._ui.ywPrj.srtLocations.append(lcId)
                    title, columns, nodeTags = self._set_location_display(lcId)
                elif childNode.startswith(self._IT):
                    itId = childNode[2:]
                    self._ui.ywPrj.srtItems.append(itId)
                    title, columns, nodeTags = self._set_item_display(itId)
                else:
                    chId = childNode[2:]
                    self._ui.ywPrj.srtChapters.append(chId)
                    self._ui.ywPrj.chapters[chId].srtScenes = []
                    update_node(childNode, chId)
                    title, columns, nodeTags = self._set_chapter_display(chId)
                self.tree.item(childNode, text=title, values=columns, tags=nodeTags)

        self._ui.ywPrj.srtChapters = []
        self._ui.ywPrj.srtCharacters = []
        self._ui.ywPrj.srtLocations = []
        self._ui.ywPrj.srtItems = []
        update_node(self.NV_ROOT, '')
        update_node(self.RS_ROOT, '')
        update_node(self.CR_ROOT, '')
        update_node(self.LC_ROOT, '')
        update_node(self.IT_ROOT, '')
        self._ui.isModified = True
        self._ui.show_status()

    def _set_scene_display(self, scId):
        """Configure scene formatting and columns."""
        title = self._ui.ywPrj.scenes[scId].title
        columns = []
        nodeTags = []
        if self._ui.ywPrj.scenes[scId].isTodoScene:
            return self._set_arc_display(scId)

        if self._ui.ywPrj.scenes[scId].isNotesScene:
            nodeTags.append('notes')
            return title, columns, tuple(nodeTags)

        if self._ui.ywPrj.scenes[scId].isUnused:
            nodeTags.append('unused')
        else:
            nodeTags.append(Scene.STATUS[self._ui.ywPrj.scenes[scId].status])
        columns.append(self._ui.ywPrj.scenes[scId].wordCount)
        columns.append(Scene.STATUS[self._ui.ywPrj.scenes[scId].status])
        try:
            columns.append(self._ui.ywPrj.characters[self._ui.ywPrj.scenes[scId].characters[0]].title)
        except:
            columns.append('N/A')
        try:
            columns.append(';'.join(self._ui.ywPrj.scenes[scId].tags))
        except:
            columns.append('')
        if self._ui.ywPrj.scenes[scId].isReactionScene:
            columns.append('R')
        else:
            columns.append('A')

        # Create a combined scDate information.
        if self._ui.ywPrj.scenes[scId].date is not None and self._ui.ywPrj.scenes[scId].date != Scene.NULL_DATE:
            cmbDate = self._ui.ywPrj.scenes[scId].date
        else:
            if self._ui.ywPrj.scenes[scId].day is not None:
                cmbDate = f'Day {self._ui.ywPrj.scenes[scId].day}'
            else:
                cmbDate = ''
        columns.append(cmbDate)

        # Create a combined time information.
        if self._ui.ywPrj.scenes[scId].time is not None and self._ui.ywPrj.scenes[scId].date != Scene.NULL_DATE:
            cmbTime = self._ui.ywPrj.scenes[scId].time.rsplit(':', 1)[0]
        else:
            if self._ui.ywPrj.scenes[scId].hour or self._ui.ywPrj.scenes[scId].minute:
                if self._ui.ywPrj.scenes[scId].hour:
                    scHour = self._ui.ywPrj.scenes[scId].hour
                else:
                    scHour = '00'
                if self._ui.ywPrj.scenes[scId].minute:
                    scMinute = self._ui.ywPrj.scenes[scId].minute
                else:
                    scMinute = '00'
                cmbTime = f'{scHour.zfill(2)}:{scMinute.zfill(2)}'
            else:
                cmbTime = ''
        columns.append(cmbTime)

        # Create a combined duration information.
        if self._ui.ywPrj.scenes[scId].lastsDays is not None and self._ui.ywPrj.scenes[scId].lastsDays != '0':
            days = f'{self._ui.ywPrj.scenes[scId].lastsDays}d '
        else:
            days = ''
        if self._ui.ywPrj.scenes[scId].lastsHours is not None and self._ui.ywPrj.scenes[scId].lastsHours != '0':
            hours = f'{self._ui.ywPrj.scenes[scId].lastsHours}h '
        else:
            hours = ''
        if self._ui.ywPrj.scenes[scId].lastsMinutes is not None and self._ui.ywPrj.scenes[scId].lastsMinutes != '0':
            minutes = f'{self._ui.ywPrj.scenes[scId].lastsMinutes}min'
        else:
            minutes = ''
        columns.append(f'{days}{hours}{minutes}')

        # Display arcs the scene belongs to.
        arcs = self._ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs']
        if arcs is None:
            columns.append('')
        else:
            columns.append(arcs)

        return title, columns, tuple(nodeTags)

    def _set_arc_display(self, arcId):
        """Configure arc formatting and columns."""
        title = self._ui.ywPrj.scenes[arcId].title
        columns = []
        nodeTags = []
        nodeTags.append('todo')
        arc = self._ui.ywPrj.scenes[arcId].kwVar['Field_SceneArcs']
        if arc:
            wordCount = 0
            for scId in self._ui.ywPrj.scenes:
                if self._ui.ywPrj.scenes[scId].isTodoScene:
                    continue
                if self._ui.ywPrj.scenes[scId].isNotesScene:
                    continue
                if self._ui.ywPrj.scenes[scId].isUnused:
                    continue
                try:
                    if arc in self._ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs']:
                        wordCount += self._ui.ywPrj.scenes[scId].wordCount
                except TypeError:
                    pass
            columns.append(wordCount)
        return title, columns, tuple(nodeTags)

    def _set_chapter_display(self, chId):
        """Configure chapter formatting and columns."""

        def count_words(chId):
            """Accumulate word counts of all relevant scenes in a chapter."""
            wordCount = 0
            if self._ui.ywPrj.chapters[chId].chType == 0:
                for scId in self._ui.ywPrj.chapters[chId].srtScenes:
                    if self._ui.ywPrj.scenes[scId].isTodoScene:
                        continue
                    if self._ui.ywPrj.scenes[scId].isNotesScene:
                        continue
                    wordCount += self._ui.ywPrj.scenes[scId].wordCount
            return wordCount

        def collect_viewpoints(chId):
            """Return a string with semicolon-separated viewpoint character names."""
            vpNames = []
            if self._ui.ywPrj.chapters[chId].chType == 0:
                for scId in self._ui.ywPrj.chapters[chId].srtScenes:
                    if self._ui.ywPrj.scenes[scId].isTodoScene:
                        continue
                    if self._ui.ywPrj.scenes[scId].isNotesScene:
                        continue
                    try:
                        crId = self._ui.ywPrj.scenes[scId].characters[0]
                        viewpoint = self._ui.ywPrj.characters[crId].title
                        if not viewpoint in vpNames:
                            vpNames.append(viewpoint)
                    except TypeError:
                        pass
            return ';'.join(vpNames)

        title = self._ui.ywPrj.chapters[chId].title
        columns = []
        nodeTags = []
        if self._ui.ywPrj.chapters[chId].chType == 1:
            if self._ui.ywPrj.chapters[chId].chLevel == 1:
                # This chapter begins a new section in ywriter.
                nodeTags.append('notes part')
            else:
                nodeTags.append('notes')
            return title, columns, tuple(nodeTags)

        elif self._ui.ywPrj.chapters[chId].chType == 2:
            nodeTags.append('todo')
            return title, columns, tuple(nodeTags)

        elif self._ui.ywPrj.chapters[chId].isUnused:
            nodeTags.append('unused')
        else:
            nodeTags.append('chapter')
        wordCount = count_words(chId)
        if self._ui.ywPrj.chapters[chId].chLevel == 1:
            # This chapter begins a new section in ywriter.
            nodeTags.append('part')
            # Add all scene wordcounts until the next part.
            i = self._ui.ywPrj.srtChapters.index(chId) + 1
            while i < len(self._ui.ywPrj.srtChapters):
                c = self._ui.ywPrj.srtChapters[i]
                if self._ui.ywPrj.chapters[c].chLevel == 1:
                    break
                i += 1
                wordCount += count_words(c)
        columns.append(wordCount)
        columns.append('')
        # Status is empty
        columns.append(collect_viewpoints(chId))
        return title, columns, tuple(nodeTags)

    def _set_character_display(self, crId):
        """Configure character formatting and columns."""
        title = self._ui.ywPrj.characters[crId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(';'.join(self._ui.ywPrj.characters[crId].tags))
        except:
            columns.append('')
        if self._ui.ywPrj.characters[crId].isMajor:
            nodeTags.append('major')
        else:
            nodeTags.append('minor')
        return title, columns, tuple(nodeTags)

    def _set_location_display(self, lcId):
        """Configure location formatting and columns."""
        title = self._ui.ywPrj.locations[lcId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(';'.join(self._ui.ywPrj.locations[lcId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_item_display(self, itId):
        """Configure item formatting and columns."""
        title = self._ui.ywPrj.items[itId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(';'.join(self._ui.ywPrj.items[itId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_type(self, node, newType):
        """Recursively set scene or chapter type (Normal/Notes/Todo/Unused)."""
        if self._ui.isLocked:
            return
        if node.startswith(self._SC):
            scene = self._ui.ywPrj.scenes[node[2:]]
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
            self.tree.item(node, open=True)
            chapter = self._ui.ywPrj.chapters[node[2:]]
            if newType == 3:
                chapter.isUnused = True
                chapter.chType = 0
            else:
                chapter.chType = newType
                chapter.isUnused = False
            # Go one level down.
            for childNode in self.tree.get_children(node):
                self._set_type(childNode, newType)
        else:
            # Do nothing, avoid tree update.
            return

        self._update_tree()

    def _set_scn_status(self, node, scnStatus):
        """Recursively set scene editing status (Outline/Draft..)."""
        if self._ui.isLocked:
            return
        if node.startswith(self._SC):
            self._ui.ywPrj.scenes[node[2:]].status = scnStatus
        elif node.startswith(self._CH) or node.startswith(self._PT) or node.startswith(self.NV_ROOT):
            self.tree.item(node, open=True)
            # Go one level down.
            for childNode in self.tree.get_children(node):
                self._set_scn_status(childNode, scnStatus)
        else:
            # Do nothing, avoid tree update.
            return

        self._update_tree()

    def _set_chr_status(self, chrStatus):
        """Set character status (Major/Minor)."""
        if self._ui.isLocked:
            return
        node = self.tree.selection()[0]
        if node.startswith(self._CR):
            self._ui.ywPrj.characters[node[2:]].isMajor = chrStatus
        elif node.endswith(self._CR):
            # Go one level down.
            for childNode in self.tree.get_children(node):
                self._set_chr_status(childNode, chrStatus)
        else:
            # Do nothing, avoid tree update.
            return

        self._update_tree()

    def _move_node(self, event):
        """Move a selected node in the novel tree."""
        if self._ui.isLocked:
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

    def _on_select_node(self, event):
        """Show info on the right level."""
        try:
            nodeId = self.tree.selection()[0]
            if nodeId.startswith(self._SC):
                self._ui.on_scene_select(nodeId[2:])
            elif nodeId.startswith(self._CH):
                self._ui.on_chapter_select(nodeId[2:])
            elif nodeId.startswith(self._PT):
                self._ui.on_chapter_select(nodeId[2:])
            elif nodeId.startswith(self.NV_ROOT):
                self._ui.on_narrative_select()
            elif nodeId.startswith(self._CR):
                self._ui.on_character_select(nodeId[2:])
            elif nodeId.startswith(self._LC):
                self._ui.on_location_select(nodeId[2:])
            elif nodeId.startswith(self._IT):
                self._ui.on_item_select(nodeId[2:])
            else:
                self._ui.on_nothing_select()
        except IndexError:
            pass

    def reset_tree(self):
        """Clear the displayed tree."""
        for child in self.tree.get_children(''):
            self.tree.delete(child)

    def open_children(self, parent):
        """Recursively open children nodes."""
        self.tree.item(parent, open=True)
        for child in self.tree.get_children(parent):
            self.open_children(child)

    def close_children(self, parent):
        """Recursively close children nodes."""
        self.tree.item(parent, open=False)
        for child in self.tree.get_children(parent):
            self.close_children(child)

    #--- Methods that change the project

    def _cancel_part(self, event):
        """Remove a part but keep its chapters."""
        if self._ui.isLocked:
            return
        tv = event.widget
        selection = tv.selection()[0]
        if not selection.startswith(self._PT):
            return
        elemId = selection[2:]
        if self._ui.ask_yes_no(f'Remove part "{self._ui.ywPrj.chapters[elemId].title}" and keep the chapters?'):
            if tv.prev(selection):
                tv.selection_set(tv.prev(selection))
            else:
                tv.selection_set(tv.parent(selection))
            del self._ui.ywPrj.chapters[elemId]
            self._ui.ywPrj.srtChapters.remove(elemId)
            self.refresh_tree()
            self._update_tree()

    def _promote_chapter(self, event):
        """Make a chapter a part."""
        if self._ui.isLocked:
            return
        tv = event.widget
        selection = tv.selection()[0]
        if not selection.startswith(self._CH):
            return
        elemId = selection[2:]
        if self._ui.ask_yes_no(f'Promote chapter "{self._ui.ywPrj.chapters[elemId].title}" to part?'):
            self._ui.ywPrj.chapters[elemId].chLevel = 1
            self.refresh_tree()
            self._update_tree()

    def _demote_part(self, event):
        """Make a part a chapter."""
        if self._ui.isLocked:
            return
        tv = event.widget
        selection = tv.selection()[0]
        if not selection.startswith(self._PT):
            return
        elemId = selection[2:]
        if self._ui.ask_yes_no(f'Demote part "{self._ui.ywPrj.chapters[elemId].title}" to chapter?'):
            self._ui.ywPrj.chapters[elemId].chLevel = 0
            self.refresh_tree()
            self._update_tree()

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
                del self._ui.ywPrj.chapters[node[2:]]
                for childNode in self.tree.get_children(node):
                    waste_scenes(childNode)

        if self._ui.isLocked:
            return
        tv = event.widget
        selection = tv.selection()[0]
        elemId = selection[2:]
        if selection.startswith(self._SC):
            candidate = f'Scene "{self._ui.ywPrj.scenes[elemId].title}"'
        elif selection.startswith(self._CH):
            candidate = f'Chapter "{self._ui.ywPrj.chapters[elemId].title}"'
        elif selection.startswith(self._PT):
            candidate = f'Part "{self._ui.ywPrj.chapters[elemId].title}"'
        elif selection.startswith(self._CR):
            candidate = f'Character "{self._ui.ywPrj.characters[elemId].title}"'
        elif selection.startswith(self._LC):
            candidate = f'Location "{self._ui.ywPrj.locations[elemId].title}"'
        elif selection.startswith(self._IT):
            candidate = f'Item "{self._ui.ywPrj.items[elemId].title}"'
        else:
            return

        if self._ui.ask_yes_no(f'Delete {candidate}?'):
            if tv.prev(selection):
                tv.selection_set(tv.prev(selection))
            else:
                tv.selection_set(tv.parent(selection))
            if selection == self._trashNode:
                # Remove the "trash bin".
                tv.delete(selection)
                self._trashNode = None
                for scId in self._ui.ywPrj.chapters[elemId].srtScenes:
                    del self._ui.ywPrj.scenes[scId]
                del self._ui.ywPrj.chapters[elemId]
            elif selection.startswith(self._CR):
                # Delete a character and remove references.
                tv.delete(selection)
                del self._ui.ywPrj.characters[elemId]
                for scId in self._ui.ywPrj.scenes:
                    try:
                        self._ui.ywPrj.scenes[scId].characters.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self._LC):
                # Delete a location and remove references.
                tv.delete(selection)
                del self._ui.ywPrj.locations[elemId]
                for scId in self._ui.ywPrj.scenes:
                    try:
                        self._ui.ywPrj.scenes[scId].locations.remove(elemId)
                    except:
                        pass
            elif selection.startswith(self._IT):
                # Delete an item and remove references.
                tv.delete(selection)
                del self._ui.ywPrj.items[elemId]
                for scId in self._ui.ywPrj.scenes:
                    try:
                        self._ui.ywPrj.scenes[scId].items.remove(elemId)
                    except:
                        pass
            else:
                # Part/chapter/scene selected.
                if self._trashNode is None:
                    # Create a "trash bin"; use the first free chapter ID.
                    trashId = create_id(self._ui.ywPrj.chapters)
                    self._ui.ywPrj.chapters[trashId] = Chapter()
                    self._ui.ywPrj.chapters[trashId].title = "Trash"
                    self._ui.ywPrj.chapters[trashId].isTrash = True
                    self._trashNode = f'{self._CH}{trashId}'
                    self.tree.insert(self.NV_ROOT, 'end', self._trashNode, text='Trash', tags='unused', open=True)
                if selection.startswith(self._SC):
                    if self.tree.parent(selection) == self._trashNode:
                        # Remove scene, if already in trash bin.
                        tv.delete(selection)
                        del self._ui.ywPrj.scenes[elemId]
                    else:
                        # Move scene to the "trash bin".
                        waste_scenes(selection)
                else:
                    # Delete part/chapter and move child scenes to the "trash bin".
                    waste_scenes(selection)
                    tv.delete(selection)
                # Make sure the whole "trash bin" is unused.
                self._set_type(self._trashNode, 3)
            self._update_tree()

    def add_part(self):
        """Add a Part node to the tree and create an instance."""
        if self._ui.isLocked:
            return
        try:
            selection = self.tree.selection()[0]
        except:
            selection = ''
        parent = self.NV_ROOT
        index = 0
        if selection.startswith(self._SC):
            selection = self.tree.parent(selection)
        if selection.startswith(self._CH):
            index = self.tree.index(selection) + 1
            selection = self.tree.parent(selection)
        if selection.startswith(self._PT):
            index = self.tree.index(selection) + 1
            parent = self.tree.parent(selection)
        elif selection.startswith(self.RS_ROOT):
            index = 0
            parent = self.RS_ROOT
        chId = create_id(self._ui.ywPrj.chapters)
        newNode = f'{self._PT}{chId}'
        self._ui.ywPrj.chapters[chId] = Chapter()
        self._ui.ywPrj.chapters[chId].title = f'New Part (ID{chId})'
        self._ui.ywPrj.chapters[chId].chLevel = 1
        self._ui.ywPrj.chapters[chId].kwVar['Field_NoNumber'] = None
        if parent.startswith(self.RS_ROOT):
            self._ui.ywPrj.chapters[chId].chType = 1
        else:
            self._ui.ywPrj.chapters[chId].chType = 0
        self._ui.ywPrj.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self.refresh_tree()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)

    def add_chapter(self):
        """Add a Chapter node to the tree and create an instance."""
        if self._ui.isLocked:
            return
        try:
            selection = self.tree.selection()[0]
        except:
            selection = ''
        parent = self.NV_ROOT
        isNotes = False
        index = 0
        if selection.startswith(self._SC):
            parent = self.tree.parent(selection)
            selection = self.tree.parent(selection)
        if selection.startswith(self._CH):
            parent = self.tree.parent(selection)
            index = self.tree.index(selection) + 1
        elif selection.startswith(self._PT):
            parent = selection
        # Inherit part type, if "Notes"
        if self.tree.parent(parent).startswith(self.RS_ROOT):
            isNotes = True
        chId = create_id(self._ui.ywPrj.chapters)
        newNode = f'{self._CH}{chId}'
        self._ui.ywPrj.chapters[chId] = Chapter()
        self._ui.ywPrj.chapters[chId].title = f'New Chapter (ID{chId})'
        self._ui.ywPrj.chapters[chId].chLevel = 0
        self._ui.ywPrj.chapters[chId].kwVar['Field_NoNumber'] = None
        if isNotes:
            self._ui.ywPrj.chapters[chId].chType = 1
        else:
            self._ui.ywPrj.chapters[chId].chType = 0
        self._ui.ywPrj.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self.refresh_tree()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)

    def add_scene(self):
        """Add a Scene node to the tree and create an instance."""
        if self._ui.isLocked:
            return
        try:
            selection = self.tree.selection()[0]
        except:
            return

        index = 0
        if selection.startswith(self._SC):
            parent = self.tree.parent(selection)
            index = self.tree.index(selection) + 1
        elif selection.startswith(self._CH):
            parent = selection
        elif selection.startswith(self._PT):
            parent = selection
        else:
            return

        scId = create_id(self._ui.ywPrj.scenes)
        newNode = f'{self._SC}{scId}'
        self._ui.ywPrj.scenes[scId] = Scene()
        self._ui.ywPrj.scenes[scId].title = f'New Scene (ID{scId})'
        self._ui.ywPrj.scenes[scId].status = 1
        # Inherit chapter type
        parentChapter = self._ui.ywPrj.chapters[parent[2:]]
        if parentChapter.chType == 1:
            self._ui.ywPrj.scenes[scId].isNotesScene = True
        elif parentChapter.chType == 2:
            self._ui.ywPrj.scenes[scId].isTodoScene = True
        elif parentChapter.isUnused:
            self._ui.ywPrj.scenes[scId].isnused = True
        # Edit status = Outline
        self._ui.ywPrj.scenes[scId].kwVar['Field_SceneArcs'] = None
        title, columns, nodeTags = self._set_scene_display(scId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)

    def add_world_element(self, selection=None):
        """Add a Character/Location/Item node to the tree and create an instance.
        
        Positional arguments:
            selection -- str: tree position where to place a new node.
            
        - The new node's type is determined by the "selection" argument.
        - If a node of the same type as the new node is selected, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the first position.   
        """
        if self._ui.isLocked:
            return
        if selection is None:
            selection = self.tree.selection()[0]
        if self._CR in selection:
            # Add a character.
            crId = create_id(self._ui.ywPrj.characters)
            newNode = f'{self._CR}{crId}'
            self._ui.ywPrj.characters[crId] = Character()
            self._ui.ywPrj.characters[crId].title = f'New Character (ID{crId})'
            title, columns, nodeTags = self._set_character_display(crId)
            root = self.CR_ROOT
            prefix = self._CR
        elif self._LC in selection:
            # Add a location.
            lcId = create_id(self._ui.ywPrj.locations)
            newNode = f'{self._LC}{lcId}'
            self._ui.ywPrj.locations[lcId] = WorldElement()
            self._ui.ywPrj.locations[lcId].title = f'New Location (ID{lcId})'
            title, columns, nodeTags = self._set_location_display(lcId)
            root = self.LC_ROOT
            prefix = self._LC
        elif self._IT in selection:
            # Add an item.
            itId = create_id(self._ui.ywPrj.items)
            newNode = f'{self._IT}{itId}'
            self._ui.ywPrj.items[itId] = WorldElement()
            self._ui.ywPrj.items[itId].title = f'New Item (ID{itId})'
            title, columns, nodeTags = self._set_item_display(itId)
            root = self.IT_ROOT
            prefix = self._IT
        else:
            return

        if selection.startswith(prefix):
            index = self.tree.index(selection) + 1
        else:
            index = 0
        self.tree.insert(root, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
        self.tree.selection_set(newNode)
        self.tree.see(newNode)

    def on_quit(self, kwargs):
        """Write column width to the applicaton's keyword arguments.
        
        Positional arguments:
            kwargs -- reference to the ui kwargs dictionary.
        """
        for i, column in enumerate(self._COLUMNS):
            kwargs[column[1]] = self.tree.column(i, 'width')

