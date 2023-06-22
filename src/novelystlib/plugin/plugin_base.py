"""Provide an abstract Plugin base class.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class PluginBase(ABC):
    """Abstract Plugin base class.
    
    Public class constants:
        VERSION: str -- Version string.
        NOVELYST_API: str -- API compatibility indicator.
        DESCRIPTION: str -- Description to be diplayed in the novelyst plugin list.
        URL: str -- Plugin project homepage URL.

    Public instance variables:
        filePath: str -- Location of the installed plugin.
        isActive: Boolean -- Acceptance flag.
        isRejected: Boolean --  Rejection flag.
        
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        on_close() -- Actions to be performed when a project is closed.       
        on_quit() -- Actions to be performed when novelyst is closed.
        open_node() -- Actions on double-clicking on a node or pressing the Return key.        
    
    """
    # Class constants to be overridden by subclasses.
    VERSION = '0.0'
    NOVELYST_API = '4.31'
    DESCRIPTION = ''
    URL = ''

    def __init__(self):
        self.filePath = None
        self.isActive = None
        self.isRejected = None

    @abstractmethod
    def install(self, ui):
        """Install the plugin.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        pass

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        pass

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        pass

    def on_close(self):
        """Actions to be performed when a project is closed."""
        pass

    def on_quit(self):
        """Actions to be performed when novelyst is closed."""
        pass

    def open_node(self):
        """Actions on double-clicking on a node or pressing the Return key."""
        pass
