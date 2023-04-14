"""Provide an "index card" class.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from novelystlib.widgets.text_box import TextBox


class IndexCard(tk.Frame):
    """An "index card" class.
    
    Public instance variables:
        title: tk.StringVar -- Editable title text.
        bodyBox: TextBox -- Body text editor.
    
    """

    def __init__(self, master=None, cnf={}, fg='black', bg='white', font='Courier 10', **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        # Title label.
        self.title = tk.StringVar(value='')
        titleFrame = tk.Frame(self, borderwidth=3, bg=bg)
        titleFrame.pack(fill=tk.X)
        titleEntry = tk.Entry(titleFrame,
                              bd=0,
                              textvariable=self.title,
                              relief=tk.FLAT,
                              font=font,
                              )
        titleEntry.config({'background': bg,
                           'foreground': fg,
                           'insertbackground': fg,
                           })
        titleEntry.pack(fill=tk.X, ipady=6)

        tk.Frame(self, bg='red', height=1, bd=0).pack(fill=tk.X)
        tk.Frame(self, bg=bg, height=2, bd=0).pack(fill=tk.X)

        # Description window.
        self.bodyBox = TextBox(self,
                wrap='word',
                undo=True,
                autoseparators=True,
                maxundo=-1,
                padx=5,
                pady=5,
                bg=bg,
                fg=fg,
                insertbackground=fg,
                font=font,
                )
        self.bodyBox.pack(fill=tk.BOTH, expand=True)

