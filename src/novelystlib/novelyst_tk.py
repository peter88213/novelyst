#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
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

    def __init__(self, colTitle, **kwargs):
        """Put a text box to the GUI main window.
        
        Required keyword arguments:
            root_geometry -- str: geometry of the root window.
            tree_frame_width -- int: width of the chapter frame.
    
        Extends the superclass constructor.
        """
        self.kwargs = kwargs
        super().__init__(colTitle, **kwargs)
        self._root.geometry(kwargs['root_geometry'])
        rootWidth = int(kwargs['root_geometry'].split('x', maxsplit=1)[0])
        self._root.protocol("WM_DELETE_WINDOW", self._on_quit)
        self._chapterMenu = None
        self._sceneMenu = None

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

        # Create a data window.
        self._dataWindow = tk.PanedWindow(self._dataFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._dataWindow.pack(expand=True, fill='both')

        # Place a desc window inside the data window.
        self._descWindow = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=4, width=10)
        self._dataWindow.add(self._descWindow)

        self._fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']

        self._tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self._tree.bind('<Control-B1-Motion>', self._move_node)
        self._tree.bind('<Delete>', self._delete_node)

        self._novelRoot = None
        self._trashNode = None

    def _update_tree(self):
        """Rebuild the sorted lists."""

        def update_node(node, chId):
            """Recursive tree builder."""
            for childNode in self._tree.get_children(node):
                if childNode.startswith('sc'):
                    self._ywPrj.chapters[chId].srtScenes.append(childNode[2:])
                elif childNode.startswith('cr'):
                    self._ywPrj.srtCharacters.append(childNode[2:])
                elif childNode.startswith('lc'):
                    self._ywPrj.srtLocations.append(childNode[2:])
                elif childNode.startswith('it'):
                    self._ywPrj.srtItems.append(childNode[2:])
                else:
                    chId = childNode[2:]
                    self._ywPrj.srtChapters.append(chId)
                    self._ywPrj.chapters[chId].srtScenes = []
                    update_node(childNode, chId)

        self._ywPrj.srtChapters = []
        self._ywPrj.srtCharacters = []
        self._ywPrj.srtLocations = []
        self._ywPrj.srtItems = []
        update_node(self._novelRoot, '')
        update_node(self._characterRoot, '')
        update_node(self._locationRoot, '')
        update_node(self._itemRoot, '')
        self._fileMenu.entryconfig('Save', state='normal')

    def _delete_node(self, event):
        """Delete parts, chapters, and scenes in the novel tree."""

        def waste_scenes(node):
            """Move all scenes under the node to the 'trash bin'."""
            if node.startswith('sc'):
                tv.item(node, tags='unused')
                tv.move(node, self._trashNode, tv.index(self._trashNode))
            else:
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
                del self._ywPrj.characters[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].characters.remove(elemId)
                    except ValueError:
                        pass
                tv.delete(selection)
            elif selection.startswith('lc'):
                del self._ywPrj.locations[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].locations.remove(elemId)
                    except ValueError:
                        pass
                tv.delete(selection)
            elif selection.startswith('it'):
                del self._ywPrj.items[elemId]
                for scId in self._ywPrj.scenes:
                    try:
                        self._ywPrj.scenes[scId].items.remove(elemId)
                    except ValueError:
                        pass
                tv.delete(selection)
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

    def _move_node(self, event):
        """Move parts, chapters, and scenes in the novel tree."""
        tv = event.widget
        selection = tv.selection()[0]
        targetNode = tv.identify_row(event.y)
        if selection[:2] == targetNode[:2]:
            tv.move(selection, tv.parent(targetNode), tv.index(targetNode))
        elif selection.startswith('sc') and targetNode.startswith('ch') and not tv.get_children(targetNode):
            tv.move(selection, targetNode, tv.index(targetNode))
        elif selection.startswith('ch') and targetNode.startswith('pt') and not tv.get_children(targetNode):
            tv.move(selection, targetNode, tv.index(targetNode))
        self._update_tree()

    def _on_quit(self):
        """Save windows size and position."""
        self._close_project()
        self.kwargs['root_geometry'] = self._root.winfo_geometry()
        self.kwargs['tree_frame_width'] = self._treeFrame.winfo_width()
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

    def _build_tree(self):
        """Display the opened novel's tree."""
        self._reset_tree()

        #--- Build Parts/Chapters/scenes tree.
        self._novelRoot = self._tree.insert('', 'end', 'Novel', text='Novel', open=True)
        inPart = False
        for chId in self._ywPrj.srtChapters:
            nodeTags = []
            if self._ywPrj.chapters[chId].chType == 1:
                nodeTags.append('notes')
            elif self._ywPrj.chapters[chId].chType == 2:
                nodeTags.append('todo')
            elif self._ywPrj.chapters[chId].isUnused:
                nodeTags.append('unused')
            else:
                nodeTags.append('chapter')
            if self._ywPrj.chapters[chId].isTrash:
                self._trashNode = f'ch{chId}'
                inPart = False
            if self._ywPrj.chapters[chId].chLevel == 1:
                inPart = True
                inChapter = False
                nodeTags.append('part')
                partNode = self._tree.insert(self._novelRoot, 'end', f'pt{chId}', text=self._ywPrj.chapters[chId].title, tags=tuple(nodeTags), open=True)
            else:
                inChapter = True
                if inPart:
                    parentNode = partNode
                else:
                    parentNode = self._novelRoot
                chapterNode = self._tree.insert(parentNode, 'end', f'ch{chId}', text=self._ywPrj.chapters[chId].title, tags=tuple(nodeTags))
            for scId in self._ywPrj.chapters[chId].srtScenes:
                nodeTags = []
                if self._ywPrj.scenes[scId].isTodoScene:
                    nodeTags.append('todo')
                elif self._ywPrj.scenes[scId].isNotesScene:
                    nodeTags.append('notes')
                elif self._ywPrj.scenes[scId].isUnused:
                    nodeTags.append('unused')
                if inChapter:
                    parentNode = chapterNode
                else:
                    parentNode = partNode
                self._tree.insert(parentNode, 'end', f'sc{scId}', text=self._ywPrj.scenes[scId].title, tags=tuple(nodeTags))
        self._tree.tag_configure('chapter', foreground='green')
        self._tree.tag_configure('unused', foreground='grey')
        self._tree.tag_configure('notes', foreground='blue')
        self._tree.tag_configure('todo', foreground='red')
        self._tree.tag_configure('part', font=('', self._fontSize, 'bold'))

        #--- Build character tree.
        self._characterRoot = self._tree.insert('', 'end', 'Characters', text='Characters', open=False)
        for crId in self._ywPrj.srtCharacters:
            self._tree.insert(self._characterRoot, 'end', f'cr{crId}', text=self._ywPrj.characters[crId].title, open=True)

        #--- Build location tree.
        self._locationRoot = self._tree.insert('', 'end', 'Locations', text='Locations', open=False)
        for lcId in self._ywPrj.srtLocations:
            self._tree.insert(self._locationRoot, 'end', f'lc{lcId}', text=self._ywPrj.locations[lcId].title, open=True)

        #--- Build item tree.
        self._itemRoot = self._tree.insert('', 'end', 'Items', text='Items', open=False)
        for itId in self._ywPrj.srtItems:
            self._tree.insert(self._itemRoot, 'end', f'it{itId}', text=self._ywPrj.items[itId].title, open=True)

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
        self._chapterMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Chapter', menu=self._chapterMenu)
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._sceneMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Scene', menu=self._sceneMenu)
        self._mainMenu.entryconfig('Scene', state='disabled')
        self._fileMenu.add_command(label='Save', command=lambda: self._save_project())
        self._fileMenu.entryconfig('Save', state='disabled')

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('Chapter', state='disabled')
        self._mainMenu.entryconfig('Scene', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('Chapter', state='normal')
        self._mainMenu.entryconfig('Scene', state='normal')

    def open_project(self, fileName):
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
            self._statusBar.config(text=message)
            return ''

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
        return fileName

    def _save_project(self):
        if self._ywPrj.is_locked():
            self.set_info_how(f'{ERROR}yWriter seems to be open. Please close first.')
            return
        self._ywPrj.write()
        self._fileMenu.entryconfig('Save', state='disabled')
        current_time = datetime.now().strftime('%H:%M:%S')
        self._set_status(f'Project saved at {current_time}')

    def _close_project(self):
        """Clear the text box.
        
        Extends the superclass method.
        """
        if self._fileMenu.entrycget('Save', 'state') == 'normal':
            if self.ask_yes_no('Save changes?'):
                self._save_project()
        self._fileMenu.entryconfig('Save', state='disabled')
        self._reset_tree()
        self._reset_info()
        super()._close_project()

    def _reset_info(self):
        self._descWindow.delete('1.0', tk.END)

