"""Custom theme plugin for novelyst.

Applies the 'awdark' theme, if available. 

Installation: 

- Copy this file into the 'plugin' subdirectory of your novelyst installation folder 
  (e.g. ~/.pywriter/novelyst).
- Download the zipped tcl-awthemes package from https://sourceforge.net/projects/tcl-awthemes/
- Unpack the awthemes<version> folder and remove the version from the folder's name.
- Make sure there's a 'themes' subdirectory in your novelyst installation folder. 
- Put the 'awthemes' folder into the 'themes' directory.

The installation routine changes colors; this will take effect after a novelyst restart.
To restore the default colors after having uninstalled the plugin, close novelyst,
and delete the novelyst.ini file in the novelyst/config directory.

Compatibility: novelyst v2.0 API 
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
APPLICATION = 'awdark theme'

THEME_PACKAGE = 'awthemes'
THEME = 'awdark'
import os
import sys
from tkinter import messagebox


class Plugin():
    VERSION = '2.0.0'
    NOVELYST_API = '2.0'
    DESCRIPTION = 'Applies the tcl awdark theme, if available'
    URL = 'https://peter88213.github.io/novelyst'

    COLORS = dict(
        color_chapter='chartreuse',
        color_unused='gray',
        color_notes='RoyalBlue1',
        color_todo='tomato',
        color_major='SteelBlue1',
        color_minor='SteelBlue',
        color_outline='orchid2',
        color_draft='white',
        color_1st_edit='DarkGoldenrod2',
        color_2nd_edit='DarkGoldenrod3',
        color_done='DarkGoldenrod4',
        color_staged='white',
        color_descriptive='light sea green',
        color_explaining='peru',
        color_summarizing='violet',
        color_locked_bg='dim gray',
        color_locked_fg='light gray',
        color_modified_bg='goldenrod1',
        color_modified_fg='maroon',
        )

    def install(self, ui):
        """Install and apply the 'awdark' theme.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        themePath = os.path.abspath(f'{sys.path[0]}/themes')

        # Load custom theme. Exceptions are caught by the application.
        self._ui.root.tk.call('lappend', 'auto_path', f'{themePath}/{THEME_PACKAGE}')
        self._ui.root.tk.call('package', 'require', THEME)
        self._ui.guiStyle.theme_use(THEME)

        # Adjust the colors. This will take effect after restart.
        # Note: The changes wil be stored in the novelyst.ini file
        #       in the novelyst/config directory.
        #       To restore the default colors, you will have to close novelyst
        #       and delete novelyst.ini.
        colorsChanged = False
        for color in self.COLORS:
            if self._ui.kwargs[color] != self.COLORS[color]:
                self._ui.kwargs[color] = self.COLORS[color]
                colorsChanged = True
        if colorsChanged:
            messagebox.showinfo('Dark theme installer', 'Please restart novelyst now to apply changed colors.')

