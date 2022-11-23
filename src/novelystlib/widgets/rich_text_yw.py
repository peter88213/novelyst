""""Provide a tkinter Rich Text box class with novelyst-specific highlighting.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import font as tkFont
from pywriter.ui.rich_text_tk import RichTextTk


class RichTextYw(RichTextTk):
    """A text box applying novelyst formatting.
    """
    H1_NOTES_TAG = 'h1Notes'
    H1_TODO_TAG = 'h1Todo'
    H1_UNUSED_TAG = 'h1Unused'
    H2_NOTES_TAG = 'h2Notes'
    H2_TODO_TAG = 'h2Todo'
    H2_UNUSED_TAG = 'h2Unused'
    H3_NOTES_TAG = 'h3Notes'
    H3_TODO_TAG = 'h3Todo'
    H3_UNUSED_TAG = 'h3Unused'
    TODO_TAG = 'todo'
    NOTES_TAG = 'notes'
    UNUSED_TAG = 'unused'

    def __init__(self, *args, **kwargs):
        """Define some tags for novelyst-specific colors.
        
        Extends the supeclass constructor
        """
        super().__init__(*args,
                height=20,
                width=60,
                spacing1=10,
                spacing2=2,
                wrap='word',
                padx=10,
                bg=kwargs['color_text_bg'],
                fg=kwargs['color_text_fg'],
                )
        defaultFont = tkFont.nametofont(self.cget('font'))

        defaultSize = defaultFont.cget('size')
        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())
        h1Font = tkFont.Font(**defaultFont.configure())
        h2Font = tkFont.Font(**defaultFont.configure())
        h3Font = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')
        h1Font.configure(size=int(defaultSize * self.H1_SIZE),
                         weight='bold',
                         )
        h2Font.configure(size=int(defaultSize * self.H2_SIZE),
                         weight='bold',
                         )
        h3Font.configure(size=int(defaultSize * self.H3_SIZE),
                         slant='italic',
                         )
        self.tag_configure(self.H1_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_chapter'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H1_NOTES_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_notes'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H1_TODO_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_todo'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H1_UNUSED_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H2_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_chapter'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H2_NOTES_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_notes'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H2_TODO_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_todo'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H2_UNUSED_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H3_NOTES_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_notes'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )
        self.tag_configure(self.H3_TODO_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_todo'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )
        self.tag_configure(self.H3_UNUSED_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )
        self.tag_configure(self.NOTES_TAG,
                           foreground=kwargs['color_notes'],
                           )
        self.tag_configure(self.TODO_TAG,
                           foreground=kwargs['color_todo'],
                           )
        self.tag_configure(self.UNUSED_TAG,
                           foreground=kwargs['color_unused'],
                           )

