""""Provide a tkinter text box class for "contents" viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *
from novelystlib.widgets.rich_text_yw import RichTextYw


class ContentsViewer:
    """A tkinter text box class for yWriter file viewing.
    
    Public methods:
        view_text(taggedText) -- load tagged text into the text box.
        build_view() -- create tagged text for viewing.
        reset_view() -- clear the text box.

    Public instance variables:
        textBox -- RichTextTk: text viewer widget.
        contents -- list of tuples: Text containing chapter titles and scene contents.

    Show the novel contents in a text box.
    """

    def __init__(self, ui, viewerWindow):
        """Put a text box to the specified window.
        """
        self._ui = ui
        kwargs = self._ui.kwargs
        self.textBox = RichTextYw(viewerWindow, **kwargs)
        self.textBox.pack(expand=True, fill=tk.BOTH)
        self.showMarkup = tk.BooleanVar(viewerWindow, value=kwargs['show_markup'])
        ttk.Checkbutton(viewerWindow, text=_('Show markup'), variable=self.showMarkup).pack(anchor=tk.W)
        self.showMarkup.trace('w', self.update)
        if not kwargs['show_contents']:
            self._ui.middleFrame.pack_forget()
        self.textMarks = {}
        self.index = '1.0'

    def view_text(self):
        """Build a list of "tagged text" tuples and send it to the text box."""

        def convert_from_yw(text):
            if not self.showMarkup.get():
                text = re.sub('\[\/*[i|b|h|c|r|s|u]\d*\]', '', text)
                # Remove yw7 markup from text
            return text

        taggedText = []
        for chId in self._ui.ywPrj.srtChapters:
            chapter = self._ui.ywPrj.chapters[chId]
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
                    heading = f"[{_('Unnamed')}\n"
            taggedText.append((heading, headingTag))

            for scId in self._ui.ywPrj.chapters[chId].srtScenes:
                scene = self._ui.ywPrj.scenes[scId]
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
                    heading = f"[{_('Unnamed')}\n"
                taggedText.append((heading, headingTag))

                if scene.sceneContent:
                    taggedText.append((convert_from_yw(f'{scene.sceneContent}\n'), textTag))

        if not taggedText:
            taggedText.append(('(No text available)', RichTextYw.ITALIC_TAG))
        self.textMarks = {}
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', tk.END)
        for entry in taggedText:
            if len(entry) == 2:
                # entry is a regular (text, tag) tuple.
                text, tag = entry
                self.textBox.insert(tk.END, text, tag)
            else:
                # entry is a mark to insert.
                index = f"{self.textBox.count('1.0', tk.END, 'lines')[0]}.0"
                self.textMarks[entry] = index
        self.textBox['state'] = 'disabled'

    def reset_view(self):
        """Clear the text box."""
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', tk.END)
        self.textBox['state'] = 'disabled'

    def see(self, idStr):
        try:
            self.index = self.textMarks[idStr]
            self.textBox.see(self.index)
        except KeyError:
            pass

    def update(self, event=None, *args):
        self.reset_view()
        self.view_text()
        try:
            self.textBox.see(self.index)
        except KeyError:
            pass

