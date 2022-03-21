#!/usr/bin/env python3
""""Provide a tkinter tree view for novelyst.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
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
    """A tkinter GUI class for yWriter tree view."""
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
    NV_ROOT = 'nv'
    # Root of the Narrative subtree
    CR_ROOT = f'wr{_CR}'
    # Root of the Characters subtree
    LC_ROOT = f'wr{_LC}'
    # Root of the Locations subtree
    IT_ROOT = f'wr{_IT}'
    # Root of the Items subtree

    def __init__(self, ui):
        """Put a text box to the GUI main window.
        
        Required keyword arguments:
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
    
        Extends the superclass constructor.
        """
        self._ui = ui

        # Create a novel tree.
        self.tree = ttk.Treeview(self._ui.treeWindow, selectmode='browse')
        scrollY = ttk.Scrollbar(self._ui.treeWindow, orient="vertical", command=self.tree.yview)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollY.set)
        self._ui.treeWindow.add(self.tree)
        self._trashNode = None

        # Add columns to the tree.
        columns = []
        titleWidth = int(self._ui.kwargs['tree_frame_width'])
        for column in self._COLUMNS:
            titleWidth -= int(self._ui.kwargs[column[1]])
            columns.append(column[0])
        self.tree['columns'] = tuple(columns)
        for column in self._COLUMNS:
            self.tree.heading(column[0], text=column[0], anchor='w')
            self.tree.column(column[0], width=int(self._ui.kwargs[column[1]]))
        self.tree.column('#0', width=titleWidth)

        #--- Create a scene type submenu.
        self._typeMenu = tk.Menu(self._ui.root, tearoff=0)
        self._typeMenu.add_command(label='Normal', command=lambda: self._set_type(self.tree.selection()[0], 0))
        self._typeMenu.add_command(label='Notes', command=lambda: self._set_type(self.tree.selection()[0], 1))
        self._typeMenu.add_command(label='Todo', command=lambda: self._set_type(self.tree.selection()[0], 2))
        self._typeMenu.add_command(label='Unused', command=lambda: self._set_type(self.tree.selection()[0], 3))

        #--- Create a scene scene status submenu.
        self._scStatusMenu = tk.Menu(self._ui.root, tearoff=0)
        self._scStatusMenu.add_command(label='Outline', command=lambda: self._set_scn_status(self.tree.selection()[0], 1))
        self._scStatusMenu.add_command(label='Draft', command=lambda: self._set_scn_status(self.tree.selection()[0], 2))
        self._scStatusMenu.add_command(label='1st Edit', command=lambda: self._set_scn_status(self.tree.selection()[0], 3))
        self._scStatusMenu.add_command(label='2nd Edit', command=lambda: self._set_scn_status(self.tree.selection()[0], 4))
        self._scStatusMenu.add_command(label='Done', command=lambda: self._set_scn_status(self.tree.selection()[0], 5))

        #--- Create a narrative context menu.
        self._nvCtxtMenu = tk.Menu(self._ui.root, tearoff=0)
        self._nvCtxtMenu.add_command(label='Add Scene', command=self.add_scene)
        self._nvCtxtMenu.add_command(label='Add Chapter', command=self.add_chapter)
        self._nvCtxtMenu.add_command(label='Add Part', command=self.add_part)
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
        self._crStatusMenu = tk.Menu(self._ui.root, tearoff=0)
        self._crStatusMenu.add_command(label='MajorCharacter', command=lambda: self._set_chr_status(True))
        self._crStatusMenu.add_command(label='MinorCharacter', command=lambda: self._set_chr_status(False))

        #--- Create a world element context menu.
        self._wrCtxtMenu = tk.Menu(self._ui.root, tearoff=0)
        self._wrCtxtMenu.add_command(label='Add', command=lambda: self.add_world_element())
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_command(label='Delete', command=lambda: self.tree.event_generate('<Delete>', when='tail'))
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_cascade(label='Set Status', menu=self._crStatusMenu)

        #--- configure tree row display.
        fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']
        self.tree.tag_configure('root', font=('', fontSize, 'bold'))
        self.tree.tag_configure('chapter', foreground=self._ui.kwargs['color_chapter'])
        self.tree.tag_configure('unused', foreground=self._ui.kwargs['color_unused'])
        self.tree.tag_configure('notes', foreground=self._ui.kwargs['color_notes'])
        self.tree.tag_configure('todo', foreground=self._ui.kwargs['color_todo'])
        self.tree.tag_configure('part', font=('', fontSize, 'bold'))
        self.tree.tag_configure('major', foreground=self._ui.kwargs['color_major'])
        self.tree.tag_configure('minor', foreground=self._ui.kwargs['color_minor'])
        self.tree.tag_configure('Outline', foreground=self._ui.kwargs['color_outline'])
        self.tree.tag_configure('Draft', foreground=self._ui.kwargs['color_draft'])
        self.tree.tag_configure('1st Edit', foreground=self._ui.kwargs['color_1st_edit'])
        self.tree.tag_configure('2nd Edit', foreground=self._ui.kwargs['color_2nd_edit'])
        self.tree.tag_configure('Done', foreground=self._ui.kwargs['color_done'])

        #--- Event bindings.
        self.tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self.tree.bind('<Shift-B1-Motion>', self._move_node)
        self.tree.bind('<Delete>', self._delete_node)
        self.tree.bind(self._ui.kwargs['button_context_menu'], self._open_context_menu)

    def _open_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.focus_set()
            self.tree.selection_set(row)
            prefix = row[:2]
            if prefix in ('nv', self._PT, self._CH, self._SC):
                # Context is narrative/part/chapter/scene.
                if self._ui.isLocked:
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

    def build_tree(self):
        """Display the opened narrative's tree."""
        self.reset_tree()

        #--- Build Parts/Chapters/scenes tree.
        self.tree.insert('', 'end', self.NV_ROOT, text='Narrative', tags='root', open=True)
        inPart = False
        for chId in self._ui.ywPrj.srtChapters:
            if self._ui.ywPrj.chapters[chId].isTrash:
                self._trashNode = f'{self._CH}{chId}'
                inPart = False
            if self._ui.ywPrj.chapters[chId].chLevel == 1:
                inPart = True
                inChapter = False
                title, columns, nodeTags = self._set_chapter_display(chId)
                partNode = self.tree.insert(self.NV_ROOT, 'end', f'{self._PT}{chId}', text=title, values=columns, tags=nodeTags, open=True)
            else:
                inChapter = True
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
            nodeTags.append('todo')
            return title, columns, tuple(nodeTags)

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
            columns.append(','.join(self._ui.ywPrj.scenes[scId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_chapter_display(self, chId):
        """Configure chapter formatting and columns."""

        def count_words(chId):
            """Accumulate word counts of all relevant scenes in a chapter."""
            wordCount = 0
            for scId in self._ui.ywPrj.chapters[chId].srtScenes:
                if self._ui.ywPrj.scenes[scId].isTodoScene:
                    continue
                if self._ui.ywPrj.scenes[scId].isNotesScene:
                    continue
                wordCount += self._ui.ywPrj.scenes[scId].wordCount
            return wordCount

        title = self._ui.ywPrj.chapters[chId].title
        columns = []
        nodeTags = []
        if self._ui.ywPrj.chapters[chId].chType == 1:
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
        return title, columns, tuple(nodeTags)

    def _set_character_display(self, crId):
        """Configure character formatting and columns."""
        title = self._ui.ywPrj.characters[crId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ui.ywPrj.characters[crId].tags))
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
            columns.append(','.join(self._ui.ywPrj.locations[lcId].tags))
        except:
            columns.append('')
        return title, columns, tuple(nodeTags)

    def _set_item_display(self, itId):
        """Configure item formatting and columns."""
        title = self._ui.ywPrj.items[itId].title
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ui.ywPrj.items[itId].tags))
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
        elif node.startswith(self._CH) or node.startswith(self._PT) or node.startswith('nv'):
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
        nodeId = self.tree.selection()[0]
        if nodeId.startswith(self._SC):
            self._ui.set_scene_info(nodeId[2:])
        elif nodeId.startswith(self._CH):
            self._ui.set_chapter_info(nodeId[2:])
        elif nodeId.startswith(self._PT):
            self._ui.set_chapter_info(nodeId[2:])
        elif nodeId.startswith(self.NV_ROOT):
            self._ui.set_novel_info()
        elif nodeId.startswith(self._CR):
            self._ui.set_character_info(nodeId[2:])
        elif nodeId.startswith(self._LC):
            self._ui.set_location_info(nodeId[2:])
        elif nodeId.startswith(self._IT):
            self._ui.set_item_info(nodeId[2:])
        else:
            self._ui.reset_info()

    def reset_tree(self):
        """Clear the displayed novel tree."""
        for child in self.tree.get_children(''):
            self.tree.delete(child)

    def open_children(self, parent):
        """Recursively open children"""
        self.tree.item(parent, open=True)
        for child in self.tree.get_children(parent):
            self.open_children(child)

    def close_children(self, parent):
        """Recursively close children"""
        self.tree.item(parent, open=False)
        for child in self.tree.get_children(parent):
            self.close_children(child)

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

        if self.ask_yes_no(f'Delete {candidate}?'):
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
                if self._trashNode is None:
                    # Create a "trash bin"; use the first free chapter ID.
                    trashId = create_id(self._ui.ywPrj.chapters)
                    self._ui.ywPrj.chapters[trashId] = Chapter()
                    self._ui.ywPrj.chapters[trashId].title = "Trash"
                    self._ui.ywPrj.chapters[trashId].isTrash = True
                    self._trashNode = f'{self._CH}{trashId}'
                    self.tree.insert(self.NV_ROOT, 'end', self._trashNode, text='Trash', tags='unused', open=True)
                if selection.startswith(self._SC):
                    # Remove scene, if already in trash bin.
                    if self.tree.parent(selection) == self._trashNode:
                        tv.delete(selection)
                        del self._ui.ywPrj.scenes[elemId]
                else:
                    # Move scene(s) to the "trash bin".
                    waste_scenes(selection)
                    tv.delete(selection)
                    self._set_type(self._trashNode, 3)
                    # Make sure the whole "trash bin" is unused.
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
        chId = create_id(self._ui.ywPrj.chapters)
        newNode = f'{self._PT}{chId}'
        self._ui.ywPrj.chapters[chId] = Chapter()
        self._ui.ywPrj.chapters[chId].title = f'New Part (ID{chId})'
        self._ui.ywPrj.chapters[chId].chLevel = 1
        self._ui.ywPrj.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
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
        index = 0
        if selection.startswith(self._SC):
            parent = self.tree.parent(selection)
            selection = self.tree.parent(selection)
        if selection.startswith(self._CH):
            parent = self.tree.parent(selection)
            index = self.tree.index(selection) + 1
        elif selection.startswith(self._PT):
            parent = selection
        chId = create_id(self._ui.ywPrj.chapters)
        newNode = f'{self._CH}{chId}'
        self._ui.ywPrj.chapters[chId] = Chapter()
        self._ui.ywPrj.chapters[chId].title = f'New Chapter (ID{chId})'
        self._ui.ywPrj.chapters[chId].chLevel = 0
        self._ui.ywPrj.srtChapters.append(chId)
        title, columns, nodeTags = self._set_chapter_display(chId)
        self.tree.insert(parent, index, newNode, text=title, values=columns, tags=nodeTags)
        self._update_tree()
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
        # Edit status = Outline
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

    def on_quit(self, event=None):
        """Save column width."""
        for i, column in enumerate(self._COLUMNS):
            self._ui.kwargs[column[1]] = self.tree.column(i, 'width')

