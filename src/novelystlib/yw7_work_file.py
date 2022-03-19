"""Provide a class for yWriter 7 project editing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File


class Yw7WorkFile(Yw7File):
    """yWriter 7 project file representation.

    Public methods: 
        lock() -- create a non-yWriter lockfile.
        unlock() -- delete the non-yWriter lockfile, if any.
        has_lockfile() -- return True if a non-yWriter lockfile exists.
    """
    _LOCKFILE_PREFIX = '/.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    def lock(self, ui):
        """Create a non-yWriter lockfile.
        
        Positional arguments:
            ui -- reference to the calling application's user interface instance.
        """
        head, tail = os.path.split(self.filePath)
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        ui.isLocked = True
        # This is a setter method with conditions, so better check again
        if ui.isLocked:
            try:
                 with open(lockfilePath, 'w') as f:
                    f.write('')
            except:
                pass

    def unlock(self, ui):
        """Delete the non-yWriter lockfile, if any.
        
        Positional arguments:
            ui -- reference to the calling application's user interface instance.
        """
        head, tail = os.path.split(self.filePath)
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        try:
            os.remove(lockfilePath)
        finally:
            ui.isLocked = False

    def has_lockfile(self):
        """Return True if a non-yWriter lockfile exists."""
        head, tail = os.path.split(self.filePath)
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        return os.path.isfile(lockfilePath)

    def write(self):
        """Write instance variables to the yWriter xml file if not locked.
        
        This is a tribute to defensive programming.
        This method should not be called by an application, if locked. 
        Extends the superclass method.
        """
        if not self.has_lockfile():
            return super().write()
        else:
            return f'{ERROR}The project is locked.'
