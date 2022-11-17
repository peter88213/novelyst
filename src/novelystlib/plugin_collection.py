""""Provide a plugin registry class for novelyst.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
import glob
import importlib
from pywriter.pywriter_globals import *


class PluginCollection(dict):
    """A plugin registry class.
    
    Represents a dictionary with 
        key -- str: The module name.
        value -- object: The module's Plugin() instance.
    
    Public methods:
        delete_file(moduleName) -- Remove a module from the file system.
        load_file(filePath) -- Load and register a single plugin.
        load_plugins(pluginPath) -- Load and register the plugins.
        disable_menu() -- Disable menu entries when no project is open.
        enable_menu() -- Enable menu entries when a project is open.
        on_quit() -- Perform actions before a project is closed.
    """

    def __init__(self, ui):
        """Get a reference to the calling controller instance.
        
        The "ui" reference is passed as an argument to each 
        registered Plugin instance, thus giving it full access to
        the calling controller's API.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self._ui = ui

        # Get the major and minor version numbers for API compatibility check.
        # The version number is inserted on building the script.
        versionStr = '@release'
        # This is a placehoder for the build script.

        try:
            majorStr, minorStr, __ = versionStr.split('.')
            self.majorVersion = int(majorStr)
            self.minorVersion = int(minorStr)
        except ValueError:
            # Set defaults for testing.
            self.majorVersion = 3
            self.minorVersion = 0

    def delete_file(self, moduleName):
        """Remove a module from the file system.
        
        Positional arguments:
            moduleName -- str: Module name as used as registry key.
        
        Note: the plugin remains active until restart.
        Return True on success, otherwise return False. 
        """
        if moduleName in self:
            try:
                if self[moduleName].filePath:
                    if self._ui.ask_yes_no(f'{_("Delete file")} "{self[moduleName].filePath}"?'):
                        os.remove(self[moduleName].filePath)
                        self[moduleName].filePath = ''
                        return True

            except Exception as ex:
                print(str(ex))
        return False

    def load_file(self, filePath):
        """Load and register a single plugin.

        Positional arguments:
            filePath -- str: The module's location in the file system. 

        Return True on success, otherwise return False. 
        """
        try:
            moduleName = os.path.split(filePath)[1][:-3]

            # Import the module.
            module = importlib.import_module(moduleName)

            # Check API compatibility.
            pluginObject = module.Plugin()
            apiVerStr = pluginObject.NOVELYST_API
            majorStr, minorStr = apiVerStr.split('.')
            apiMajorVersion = int(majorStr)
            apiMinorVersion = int(minorStr)

            isCompatible = True
            if apiMajorVersion != self.majorVersion:
                isCompatible = False
            if apiMinorVersion > self.minorVersion:
                isCompatible = False

            if isCompatible:
                # Install the plugin by calling its constructor substitute.
                pluginObject.install(self._ui)

            # Monkey-patch flags to indicate the installation.
            pluginObject.isActive = isCompatible
            pluginObject.isRejected = False

            # Register the module.
            self[moduleName] = pluginObject

            # Locate the module.
            module.Plugin.filePath = filePath
            return True

        except Exception as ex:
            self[moduleName] = Rejected(filePath, str(ex))
            return False

    def load_plugins(self, pluginPath):
        """Load and register the plugins.
        
        Import modules from the "plugin" subdirectory 
        and instantiate their 'Plugin' classes.
        The objects are stored in the self._plugins collection.
        Return True on success, otherwise return False. 
        """
        if not os.path.isdir(pluginPath):
            print('Plugin directory not found.')
            return False

        sys.path.append(pluginPath)
        files = glob.glob(f'{pluginPath}/novelyst_*.py')
        for file in files:
            self.load_file(file)
        return True

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].disable_menu()
                except:
                    pass

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].enable_menu()
                except:
                    pass

    def on_quit(self):
        """Perform actions before a project is closed."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].on_quit()
                except:
                    pass


class Rejected:
    """Substitute for The Plugin class of a rejected module."""
    VERSION = '-'
    NOVELYST_API = '-'
    URL = ''

    def __init__(self, filePath, message):
        self.filePath = filePath
        self.isActive = False
        self.isRejected = True
        self.DESCRIPTION = message
