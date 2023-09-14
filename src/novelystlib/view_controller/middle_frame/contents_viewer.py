"""Provide a tkinter text box class for "contents" viewing.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.view_controller.widgets.rich_text_yw import RichTextYw


class ContentsViewer(RichTextYw):
    """A tkinter text box class for novelyst file viewing.
    
    Public methods:
        reset_view() -- Clear the text box.
        see(idStr) -- Scroll the text to the position of the idStr node.
        update() -- Reload the text to view.
        view_text(taggedText) -- Build a list of "tagged text" tuples and send it to the text box.

    Public instance variables:
        showMarkup: Boolean -- If True, display yWriter raw markup; if False, hide it.

    Show the novel contents in a text box.
    """

    def __init__(self, ui, parent, **kwargs):
        """Put a text box to the specified window.
        
        Positional arguments:
            ui: NovelystTk -- The instanitating controller.
            parent: tk.Frame -- The parent window.
        
        Required keyword arguments:
            show_markup: bool 
        """
        self._ui = ui
        # ui cannot be replaced by e.g. ui.novel which is None at initialization time

        super().__init__(parent, **kwargs)
        self.pack(expand=True, fill='both')
        self.showMarkup = tk.BooleanVar(parent, value=kwargs['show_markup'])
        ttk.Checkbutton(parent, text=_('Show markup'), variable=self.showMarkup).pack(anchor='w')
        self.showMarkup.trace('w', self.update)
        self._textMarks = {}
        self._index = '1.0'

    def reset_view(self):
        """Clear the text box."""
        self.config(state='normal')
        self.delete('1.0', 'end')
        self.config(state='disabled')

    def see(self, idStr):
        """Scroll the text to the position of the idStr node.
        
        Positional arguments:
            idStr: str -- Chapter or scene node (tree selection).
        """
        try:
            self._index = self._textMarks[idStr]
            super().see(self._index)
        except KeyError:
            pass

    def update(self, event=None, *args):
        """Reload the text to view."""
        self.reset_view()
        self.view_text()
        try:
            super().see(self._index)
        except KeyError:
            pass

    def view_text(self):
        """Build a list of "tagged text" tuples and send it to the text box."""

        def convert_from_yw(text):
            if not self.showMarkup.get():
                # Remove yw7 markup from text.
                text = re.sub('\[.+?\]|^\> ', '', text)
            return text

        taggedText = []
        for chId in self._ui.novel.srtChapters:
            chapter = self._ui.novel.chapters[chId]
            taggedText.append(f'ch{chId}')
            if chapter.chLevel == 0:
                if chapter.chType == 0:
                    headingTag = RichTextYw.H2_TAG
                elif chapter.chType == 1:
                    headingTag = RichTextYw.H2_NOTES_TAG
                elif chapter.chType == 2:
                    headingTag = RichTextYw.H2_TODO_TAG
                if chapter.chType == 3:
                    headingTag = RichTextYw.H2_UNUSED_TAG
            else:
                if chapter.chType == 0:
                    headingTag = RichTextYw.H1_TAG
                elif chapter.chType == 1:
                    headingTag = RichTextYw.H1_NOTES_TAG
                elif chapter.chType == 2:
                    headingTag = RichTextYw.H1_TODO_TAG
                if chapter.chType == 3:
                    headingTag = RichTextYw.H1_UNUSED_TAG

            # Get chapter titles.
            if chapter.title:
                heading = f'{chapter.title}\n'
            else:
                    heading = f"[{_('Unnamed')}]\n"
            taggedText.append((heading, headingTag))

            for scId in self._ui.novel.chapters[chId].srtScenes:
                scene = self._ui.novel.scenes[scId]
                if scene.doNotExport:
                    continue

                taggedText.append(f'sc{scId}')
                textTag = ''
                if scene.scType == 2:
                    headingTag = RichTextYw.H3_TODO_TAG
                    textTag = RichTextYw.TODO_TAG
                elif scene.scType == 1:
                    headingTag = RichTextYw.H3_NOTES_TAG
                    textTag = RichTextYw.NOTES_TAG
                elif scene.scType == 3:
                    headingTag = RichTextYw.H3_UNUSED_TAG
                    textTag = RichTextYw.UNUSED_TAG
                else:
                    headingTag = RichTextYw.H3_TAG
                if scene.title:
                    heading = f'[{scene.title}]\n'
                else:
                    heading = f"[{_('Unnamed')}]\n"
                taggedText.append((heading, headingTag))

                if scene.sceneContent:
                    taggedText.append((convert_from_yw(f'{scene.sceneContent}\n'), textTag))

        if not taggedText:
            taggedText.append(('(No text available)', RichTextYw.ITALIC_TAG))
        self._textMarks = {}
        self.config(state='normal')
        self.delete('1.0', 'end')
        for entry in taggedText:
            if len(entry) == 2:
                # entry is a regular (text, tag) tuple.
                text, tag = entry
                self.insert('end', text, tag)
            else:
                # entry is a mark to insert.
                index = f"{self.count('1.0', 'end', 'lines')[0]}.0"
                self._textMarks[entry] = index
        self.config(state='disabled')

