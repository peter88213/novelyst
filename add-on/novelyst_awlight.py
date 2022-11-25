"""Custom theme plugin for novelyst.

Applies the 'awlight' theme, if available. 

Installation: 

- Copy this file into the 'plugin' subdirectory of your novelyst installation folder 
  (e.g. ~/.pywriter/novelyst).
- Download the zipped tcl-awthemes package from https://sourceforge.net/projects/tcl-awthemes/
- Unpack the awthemes<version> folder and remove the version from the folder's name.
- Make sure there's a 'themes' subdirectory in your novelyst installation folder. 
- Put the 'awthemes' folder into the 'themes' directory. 

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
APPLICATION = 'awlight theme'

THEME_PACKAGE = 'awthemes'
THEME = 'awlight'
import os
import sys


class Plugin:
    VERSION = '4.0.0'
    NOVELYST_API = '4.0'
    DESCRIPTION = 'Applies the tcl awlight theme, if available'
    URL = 'https://peter88213.github.io/novelyst'

    def install(self, ui):
        """Install and apply the 'awlight' theme.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        themePath = os.path.abspath(f'{sys.path[0]}/themes')

        # Load custom theme. Exceptions are caught by the application.
        ui.root.tk.call('lappend', 'auto_path', f'{themePath}/{THEME_PACKAGE}')
        ui.root.tk.call('package', 'require', THEME)
        ui.guiStyle.theme_use(THEME)

