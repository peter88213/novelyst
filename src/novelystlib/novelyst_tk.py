#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from pywriter.pywriter_globals import ERROR
from pywriter.ui.main_tk import MainTk
from pywriter.yw.yw7_file import Yw7File
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


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
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
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
        self._novelTree = ttk.Treeview(self._treeWindow, selectmode='browse')
        scrollY = ttk.Scrollbar(self._treeWindow, orient="vertical", command=self._novelTree.yview)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self._novelTree.configure(yscrollcommand=scrollY.set)
        self._treeWindow.add(self._novelTree)

        # Create a data window.
        self._dataWindow = tk.PanedWindow(self._dataFrame, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self._dataWindow.pack(expand=True, fill='both')

        # Place a desc window inside the data window.
        self._descWindow = tk.Text(wrap='word', undo=True, autoseparators=True, maxundo=-1, height=4, width=10)
        self._dataWindow.add(self._descWindow)

        self._fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']

        self._novelTree.bind('<<TreeviewSelect>>', self._on_select_node)
        self._novelTree.bind('<Control-B1-Motion>', self._move_node)
        self._novelTree.bind('<Delete>', self._delete_node)

        self._rootNode = None
        self._trashNode = None

    def _delete_node(self, event):
        """Delete parts, chapters, and scenes in the novel tree."""
        tv = event.widget
        selection = tv.selection()[0]
        elemId = selection[2:]
        if selection.startswith('sc'):
            candidate = f'Scene "{self._ywPrj.scenes[elemId].title}"'
        elif selection.startswith('ch'):
            candidate = f'Chapter "{self._ywPrj.chapters[elemId].title}"'
        elif selection.startswith('pt'):
            candidate = f'Part "{self._ywPrj.chapters[elemId].title}"'
        else:
            return

        if self.ask_yes_no(f'Delete {candidate}?'):
            if tv.prev(selection):
                tv.selection_set(tv.prev(selection))
            else:
                tv.selection_set(tv.parent(selection))
            if selection == self._trashNode:
                tv.delete(selection)
                self._trashNode = None
            else:
                if self._trashNode is None:
                    i = 1
                    while str(i) in self._ywPrj.chapters:
                        i += 1
                    trashId = str(i)
                    self._ywPrj.chapters[trashId] = Chapter()
                    self._ywPrj.chapters[trashId].title = "Trash"
                    self._ywPrj.chapters[trashId].isTrash = True
                    self._ywPrj.chapters[trashId].isUnused = True
                    self._ywPrj.srtChapters.append(trashId)
                    self._trashNode = f'pt{trashId}'
                    self._novelTree.insert(self._rootNode, 'end', self._trashNode, text='Trash', tags='unused', open=True)
                else:
                    trashId = self._trashNode[2:]
                tv.move(selection, self._trashNode, tv.index(self._trashNode))
                tv.item(selection, tags='unused')
                scId = selection[2:]
                for chId in self._ywPrj.chapters:
                    if scId in self._ywPrj.chapters[chId].srtScenes:
                        self._ywPrj.chapters[chId].srtScenes.remove(scId)
                        break
                self._ywPrj.chapters[trashId].srtScenes.append(scId)

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

    def _on_close(self):
        """Save windows size and position."""
        self.kwargs['root_geometry'] = self._root.winfo_geometry()
        self.kwargs['tree_frame_width'] = self._treeFrame.winfo_width()
        self._root.destroy()

    def _on_select_node(self, event):
        """Show info on the right level."""
        nodeId = self._novelTree.selection()[0]
        if nodeId.startswith('ch'):
            chId = self._novelTree.selection()[0].split('ch', maxsplit=1)[1]
            self._set_chapter_info(chId)
        elif nodeId.startswith('sc'):
            scId = nodeId.split('sc', maxsplit=1)[1]
            self._set_scene_info(scId)
        elif nodeId.startswith('pt'):
            chId = self._novelTree.selection()[0].split('pt', maxsplit=1)[1]
            self._set_chapter_info(chId)
        else:
            self._set_novel_info()

    def _reset_novel_tree(self):
        """Clear the displayed novel tree."""
        for child in self._novelTree.get_children(''):
            self._novelTree.delete(child)

    def _set_novel_tree(self):
        """Display the opened novel's tree."""
        self._reset_novel_tree()
        self._rootNode = self._novelTree.insert('', 'end', 'nv1', text=self._ywPrj.title, open=True)
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
            if self._ywPrj.chapters[chId].chLevel == 1:
                inPart = True
                inChapter = False
                nodeTags.append('part')
                partNode = self._novelTree.insert(self._rootNode, 'end', f'pt{chId}', text=self._ywPrj.chapters[chId].title, tags=tuple(nodeTags), open=True)
            else:
                inChapter = True
                if inPart:
                    parentNode = partNode
                else:
                    parentNode = self._rootNode
                chapterNode = self._novelTree.insert(parentNode, 'end', f'ch{chId}', text=self._ywPrj.chapters[chId].title, tags=tuple(nodeTags))
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
                self._novelTree.insert(parentNode, 'end', f'sc{scId}', text=self._ywPrj.scenes[scId].title, tags=tuple(nodeTags))

        self._novelTree.tag_configure('chapter', foreground='green')
        self._novelTree.tag_configure('unused', foreground='grey')
        self._novelTree.tag_configure('notes', foreground='blue')
        self._novelTree.tag_configure('todo', foreground='red')
        self._novelTree.tag_configure('part', font=('', self._fontSize, 'bold'))

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
        self._set_novel_tree()
        return fileName

    def _close_project(self):
        """Clear the text box.
        
        Extends the superclass method.
        """
        self._reset_novel_tree()
        self._descWindow.delete('1.0', tk.END)
        super()._close_project()

