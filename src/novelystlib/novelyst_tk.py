#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from datetime import datetime
from pywriter.pywriter_globals import ERROR
from pywriter.ui.main_tk import MainTk
from pywriter.yw.yw7_file import Yw7File
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.pywriter_globals import ERROR


class NovelystTk(MainTk):
    """A tkinter GUI class for yWriter project processing.

    Show titles, descriptions, and contents in a text box.
    """

    _COLUMNS = (
        ('Words', 'wc_width'),
        ('Status', 'status_width'),
        ('Viewpoint', 'vp_width'),
        ('Tags', 'tags_width'),
        )

    def __init__(self, colTitle, **kwargs):
        """Put a text box to the GUI main window.
        
        Required keyword arguments:
            root_geometry -- str: geometry of the root window.
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
        self.kwargs = kwargs
        super().__init__(colTitle, **kwargs)
        self._root.geometry(kwargs['root_geometry'])
        rootWidth = int(kwargs['root_geometry'].split('x', maxsplit=1)[0])
        self._root.protocol("WM_DELETE_WINDOW", self._on_quit)
        self._chapterMenu = None
        self._sceneMenu = None
        self._hasChanged = False

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
        self._tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self._tree.bind('<Control-B1-Motion>', self._move_node)
        self._tree.bind('<Delete>', self._delete_node)
        self._tree.bind('<Button-3>', self._context_menu)
        self._root.bind('<Control_L>s', self._save_project)
        self._root.bind('<Control_L>r', self._reload_project)
        self._root.bind('<Control_L>o', self._open_project)
        self._root.bind('<Control_L>q', self._close_project)

        self._novelRoot = None
        self._trashNode = None

    def _build_tree(self):
        """Display the opened novel's tree."""
        self._reset_tree()

        #--- Build Parts/Chapters/scenes tree.
        self._novelRoot = self._tree.insert('', 'end', 'rootNovel', text='Novel', tags='root', open=True)
        inPart = False
        for chId in self._ywPrj.srtChapters:
            if self._ywPrj.chapters[chId].isTrash:
                self._trashNode = f'ch{chId}'
                inPart = False
            if self._ywPrj.chapters[chId].chLevel == 1:
                inPart = True
                inChapter = False
                columns, nodeTags = self._set_chapter_display(chId)
                partNode = self._tree.insert(self._novelRoot, 'end', f'pt{chId}', text=self._ywPrj.chapters[chId].title, values=columns, tags=nodeTags, open=True)
            else:
                inChapter = True
                if inPart:
                    parentNode = partNode
                else:
                    parentNode = self._novelRoot
                columns, nodeTags = self._set_chapter_display(chId)
                chapterNode = self._tree.insert(parentNode, 'end', f'ch{chId}', text=self._ywPrj.chapters[chId].title, values=columns, tags=nodeTags)
            for scId in self._ywPrj.chapters[chId].srtScenes:
                columns, nodeTags = self._set_scene_display(scId)
                if inChapter:
                    parentNode = chapterNode
                else:
                    parentNode = partNode
                self._tree.insert(parentNode, 'end', f'sc{scId}', text=self._ywPrj.scenes[scId].title, values=columns, tags=nodeTags)

        #--- Build character tree.
        self._characterRoot = self._tree.insert('', 'end', 'rootCharacters', text='Characters', tags='root', open=False)
        for crId in self._ywPrj.srtCharacters:
            columns, nodeTags = self._set_character_display(crId)
            self._tree.insert(self._characterRoot, 'end', f'cr{crId}', text=self._ywPrj.characters[crId].title, values=columns, tags=nodeTags)

        #--- Build location tree.
        self._locationRoot = self._tree.insert('', 'end', 'rootLocations', text='Locations', tags='root', open=False)
        for lcId in self._ywPrj.srtLocations:
            columns, nodeTags = self._set_location_display(lcId)
            self._tree.insert(self._locationRoot, 'end', f'lc{lcId}', text=self._ywPrj.locations[lcId].title, values=columns, tags=nodeTags)

        #--- Build item tree.
        self._itemRoot = self._tree.insert('', 'end', 'rootItems', text='Items', tags='root', open=False)
        for itId in self._ywPrj.srtItems:
            columns, nodeTags = self._set_item_display(itId)
            self._tree.insert(self._itemRoot, 'end', f'it{itId}', text=self._ywPrj.items[itId].title, values=columns, tags=nodeTags)

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
                if childNode.startswith('sc'):
                    scId = childNode[2:]
                    self._ywPrj.chapters[chId].srtScenes.append(scId)
                    columns, nodeTags = self._set_scene_display(scId)
                elif childNode.startswith('cr'):
                    crId = childNode[2:]
                    self._ywPrj.srtCharacters.append(crId)
                    columns, nodeTags = self._set_character_display(crId)
                elif childNode.startswith('lc'):
                    lcId = childNode[2:]
                    self._ywPrj.srtLocations.append(lcId)
                    columns, nodeTags = self._set_location_display(lcId)
                elif childNode.startswith('it'):
                    itId = childNode[2:]
                    self._ywPrj.srtItems.append(itId)
                    columns, nodeTags = self._set_item_display(itId)
                else:
                    chId = childNode[2:]
                    self._ywPrj.srtChapters.append(chId)
                    self._ywPrj.chapters[chId].srtScenes = []
                    update_node(childNode, chId)
                    columns, nodeTags = self._set_chapter_display(chId)
                self._tree.item(childNode, values=columns, tags=nodeTags)

        self._ywPrj.srtChapters = []
        self._ywPrj.srtCharacters = []
        self._ywPrj.srtLocations = []
        self._ywPrj.srtItems = []
        update_node(self._novelRoot, '')
        update_node(self._characterRoot, '')
        update_node(self._locationRoot, '')
        update_node(self._itemRoot, '')
        self._set_changeflag()
        self._set_status()

    def _delete_node(self, event):
        """Delete a node and its children.
        
        Move scenes to the "Trash" chapter.
        Delete parts/chapters and move their children scenes to the "Trash" chapter.
        Delete characters/locations/items and remove their scene references.
        """

        def waste_scenes(node):
            """Move all scenes under the node to the 'trash bin'."""
            if node.startswith('sc'):
                # Move scene.
                tv.move(node, self._trashNode, tv.index(self._trashNode))
                self._ywPrj.scenes[node[2:]].isUnused = True
            else:
                # Delete chapter and go one level up.
                del self._ywPrj.chapters[node[2:]]
                for childNode in self._tree.get_children(node):
                    waste_scenes(childNode)

        tv = event.widget
        selection = tv.selection()[0]
        elemId = selection[2:]
        if selection.startswith('sc'):
            candidate = f'Scene "{self._ywPrj.scenes[elemId].title}"'
        elif selection.startswith('ch'):
            candidate = f'Chapter "{self._ywPrj.chapters[elemId].title}"'
        elif selection.startswith('pt'):
            candidate = f'Part "{self._ywPrj.chapters[elemId].title}"'
        elif selection.startswith('cr'):
            candidate = f'Character "{self._ywPrj.characters[elemId].title}"'
        elif selection.startswith('lc'):
            candidate = f'Location "{self._ywPrj.locations[elemId].title}"'
        elif selection.startswith('it'):
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
            elif selection.startswith('cr'):
                # Delete a character and remove references.
                tv.delete(selection)
                del self._ywPrj.characters[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].characters.remove(elemId)
                    except:
                        pass
            elif selection.startswith('lc'):
                # Delete a location and remove references.
                tv.delete(selection)
                del self._ywPrj.locations[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].locations.remove(elemId)
                    except:
                        pass
            elif selection.startswith('it'):
                # Delete an item and remove references.
                tv.delete(selection)
                del self._ywPrj.items[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].items.remove(elemId)
                    except:
                        pass
            else:
                # Move scene(s) to the "trash bin".
                if self._trashNode is None:
                    # Create a "trash bin"; use the first free chapter ID.
                    i = 1
                    while str(i) in self._ywPrj.chapters:
                        i += 1
                    trashId = str(i)
                    self._ywPrj.chapters[trashId] = Chapter()
                    self._ywPrj.chapters[trashId].title = "Trash"
                    self._ywPrj.chapters[trashId].isTrash = True
                    self._ywPrj.chapters[trashId].isUnused = True
                    self._trashNode = f'ch{trashId}'
                    self._tree.insert(self._novelRoot, 'end', self._trashNode, text='Trash', tags='unused', open=True)
                waste_scenes(selection)
                if not selection.startswith('sc'):
                    tv.delete(selection)
            self._update_tree()

    def _set_scene_display(self, scId):
        """Configure scene formatting and columns."""
        columns = []
        nodeTags = []
        if self._ywPrj.scenes[scId].isTodoScene:
            nodeTags.append('todo')
            return columns, tuple(nodeTags)

        if self._ywPrj.scenes[scId].isNotesScene:
            nodeTags.append('notes')
            return columns, tuple(nodeTags)

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
        return columns, tuple(nodeTags)

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

        columns = []
        nodeTags = []
        wordCount = 0
        if self._ywPrj.chapters[chId].chType == 1:
            nodeTags.append('notes')
            return columns, tuple(nodeTags)

        elif self._ywPrj.chapters[chId].chType == 2:
            nodeTags.append('todo')
            return columns, tuple(nodeTags)

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
        return columns, tuple(nodeTags)

    def _set_character_display(self, crId):
        """Configure character formatting and columns."""
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
        return columns, tuple(nodeTags)

    def _set_location_display(self, lcId):
        """Configure location formatting and columns."""
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ywPrj.locations[lcId].tags))
        except:
            columns.append('')
        return columns, tuple(nodeTags)

    def _set_item_display(self, itId):
        """Configure item formatting and columns."""
        columns = ['', '', '']
        nodeTags = []
        try:
            columns.append(','.join(self._ywPrj.items[itId].tags))
        except:
            columns.append('')
        return columns, tuple(nodeTags)

    def _move_node(self, event):
        """Move parts, chapters, and scenes in the novel tree."""
        tv = event.widget
        selection = tv.selection()[0]
        targetNode = tv.identify_row(event.y)
        # tv.item(targetNode, open=True)
        if selection[:2] == targetNode[:2]:
            tv.move(selection, tv.parent(targetNode), tv.index(targetNode))
        elif selection.startswith('sc') and targetNode.startswith('ch') and not tv.get_children(targetNode):
            tv.move(selection, targetNode, 0)
        elif selection.startswith('sc') and targetNode.startswith('pt'):
            tv.move(selection, targetNode, 0)
        elif selection.startswith('ch') and targetNode.startswith('pt') and not tv.get_children(targetNode):
            tv.move(selection, targetNode, tv.index(targetNode))
        self._update_tree()

    def _on_quit(self):
        """Save windows size and position."""
        self._close_project()
        self.kwargs['root_geometry'] = self._root.winfo_geometry()
        self.kwargs['tree_frame_width'] = self._treeFrame.winfo_width()
        for i, column in enumerate(self._COLUMNS):
            self.kwargs[column[1]] = self._tree.column(i, 'width')
        super()._on_quit()
        self._root.quit()

    def _on_select_node(self, event):
        """Show info on the right level."""
        nodeId = self._tree.selection()[0]
        if nodeId.startswith('ch'):
            self._set_chapter_info(nodeId[2:])
        elif nodeId.startswith('sc'):
            self._set_scene_info(nodeId[2:])
        elif nodeId.startswith('pt'):
            self._set_chapter_info(nodeId[2:])
        elif nodeId == 'Novel':
            self._set_novel_info()
        elif nodeId.startswith('cr'):
            self._set_character_info(nodeId[2:])
        elif nodeId.startswith('lc'):
            self._set_location_info(nodeId[2:])
        elif nodeId.startswith('it'):
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

    def _extend_menu(self):
        """Add main menu entries.
        
        Overrides the superclass template method. 
        """
        self._viewMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='View', menu=self._viewMenu)
        self._mainMenu.entryconfig('View', state='disabled')
        self._viewMenu.add_command(label="Expand all", command=lambda: self._open_children(''))
        self._viewMenu.add_command(label="Collapse all", command=lambda: self._close_children(''))
        self._viewMenu.add_command(label="Expand selected", command=lambda: self._open_children(self._tree.selection()[0]))
        self._viewMenu.add_command(label="Collapse selected", command=lambda: self._close_children(self._tree.selection()[0]))
        self._chapterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Chapter', menu=self._chapterMenu)
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._sceneMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Scene', menu=self._sceneMenu)
        self._mainMenu.entryconfig('Scene', state='disabled')
        self._fileMenu.add_command(label='Reload', command=self._reload_project)
        self._fileMenu.entryconfig('Reload', state='disabled')
        self._fileMenu.add_command(label='Save', command=self._save_project)
        self._fileMenu.entryconfig('Save', state='disabled')

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('View', state='disabled')
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._mainMenu.entryconfig('Scene', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('View', state='normal')
        self._mainMenu.entryconfig('Chapter', state='normal')
        self._mainMenu.entryconfig('Scene', state='normal')

    def open_project(self, fileName=''):
        """Create a yWriter project instance and read the file.
        
        Display project title, description and status.
        Return the file name.
        Extends the superclass method.
        """
        fileName = super().open_project(fileName)
        if not fileName:
            return ''

        self._ywPrj = Yw7File(fileName)
        message = self._ywPrj.read()
        if message.startswith(ERROR):
            self._close_project()
            self._set_status(text=message)
            self._reset_changeflag()
            return ''

        current_time = datetime.now().strftime('%H:%M:%S')
        self._pathBar.config(text=f'{os.path.normpath(self._ywPrj.filePath)} opened at {current_time}')
        if self._ywPrj.title:
            titleView = self._ywPrj.title
        else:
            titleView = 'Untitled yWriter project'
        if self._ywPrj.authorName:
            authorView = self._ywPrj.authorName
        else:
            authorView = 'Unknown author'
        self._titleBar.config(text=f'{titleView} by {authorView}')
        self._enable_menu()
        self._build_tree()
        self._set_status()
        self._reset_changeflag()
        return fileName

    def _save_project(self, event=None):
        if self._hasChanged:
            if self._ywPrj.is_locked():
                self.set_info_how(f'{ERROR}yWriter seems to be open. Please close first.')
                return
            self._ywPrj.write()
            self._reset_changeflag()
            current_time = datetime.now().strftime('%H:%M:%S')
            self._pathBar.config(text=f'{os.path.normpath(self._ywPrj.filePath)} saved at {current_time}')

    def _close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        if self._hasChanged:
            if self.ask_yes_no('Save changes?'):
                self._save_project()
        self._reset_changeflag()
        self._reset_tree()
        self._reset_info()
        super()._close_project()

    def _set_changeflag(self):
        self._hasChanged = True
        self._fileMenu.entryconfig('Save', state='normal')
        self._fileMenu.entryconfig('Reload', state='normal')

    def _reset_changeflag(self):
        self._hasChanged = False
        self._fileMenu.entryconfig('Save', state='disabled')
        self._fileMenu.entryconfig('Reload', state='disabled')

    def _open_project(self, event=None):
        """Create a yWriter project instance and read the file."""
        self.open_project('')

    def _reload_project(self, event=None):
        """Reload a yWriter project."""
        if self._hasChanged:
            if self.ask_yes_no('Discard changes and reload the project?'):
                self.open_project(self._ywPrj.filePath)

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

    def _context_menu(self, event):
        try:
            self._viewMenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self._viewMenu.grab_release()

    def _set_status(self, message=None):
        """Extend the superclass method."""
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
        super()._set_status(message)
