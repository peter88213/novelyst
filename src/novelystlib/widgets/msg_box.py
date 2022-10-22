import tkinter as tk
from tkinter import ttk
from pywriter.pywriter_globals import *


def openoverwritecancel(title, message , **options):
    global result
    result = None

    def cancel():
        global result
        result = None
        win.quit()

    def overwrite():
        global result
        result = False
        win.quit()

    def open():
        global result
        result = True
        win.quit()

    win = tk.Toplevel()
    win.title(title)
    win.grab_set()
    ttk.Label(win, text=message).pack(padx=20, pady=30)
    buttons = {}
    buttons['cancel'] = ttk.Button(win, text=_('Cancel'), command=cancel)
    buttons['cancel'].pack(side=tk.RIGHT, padx=10, pady=10)
    buttons['overwrite'] = ttk.Button(win, text=_('Overwrite'), command=overwrite)
    buttons['overwrite'].pack(side=tk.RIGHT, padx=10, pady=10)
    buttons['open'] = ttk.Button(win, text=_('Open'), command=open)
    buttons['open'].pack(side=tk.RIGHT, padx=10, pady=10)
    if options:
        buttons[options['default']].focus_set()
    win.mainloop()
    win.destroy()
    return result
