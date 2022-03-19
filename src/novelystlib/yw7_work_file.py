"""Provide a class for yWriter 7 project editing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from datetime import datetime
from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File


class Yw7WorkFile(Yw7File):
    """yWriter 7 project file representation.

    Public methods: 
        lock() -- create a non-yWriter lockfile.
        unlock() -- delete the non-yWriter lockfile, if any.
        has_lockfile() -- return True if a non-yWriter lockfile exists.
        has_changed_on_disk() -- return True if the yw project file has changed since last opened.
        write() -- write file if not locked, and get timestamp.
        read() -- read file and get timestamp.
        
    Public properties:
        fileDate -- str: ISO formatted file date (read-only)
        
    This extends the superclass with a timestamp and a locking capability.
    """
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath -- str: path to the yw7 file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._timestamp = None

    @property
    def fileDate(self):
        if self._timestamp is not None:
            return datetime.fromtimestamp(self._timestamp).replace(microsecond=0).isoformat(sep=' ')
        else:
            return 'Never'

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail

    def lock(self):
        """Create a non-yWriter lockfile."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        if not os.path.isfile(lockfilePath):
            with open(lockfilePath, 'w') as f:
                f.write('')

    def unlock(self):
        """Delete the non-yWriter lockfile, if any."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        try:
            os.remove(lockfilePath)
        except:
            pass

    def has_lockfile(self):
        """Return True if a non-yWriter lockfile exists."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        return os.path.isfile(lockfilePath)

    def has_changed_on_disk(self):
        """Return True if the yw project file has changed since last opened."""
        try:
            if self._timestamp != os.path.getmtime(self.filePath):
                return True
            else:
                return False

        except:
            # this is for newly created projects
            return False

    def read(self):
        """Read file and get timestamp.
        
        Return a message beginning with the ERROR constant in case of error.
        Extends the superclass method.
        """
        message = super().read()
        try:
            self._timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None
        return message

    def write(self):
        """Write file if not locked, and get timestamp.
        
        Return a message beginning with the ERROR constant in case of error.
        Extends the superclass method.
        """
        if not self.has_lockfile():
            # tribute to defensive programming
            message = super().write()
            try:
                self._timestamp = os.path.getmtime(self.filePath)
            except:
                self.timestamp = None
            return message

        else:
            return f'{ERROR}The project is locked.'

