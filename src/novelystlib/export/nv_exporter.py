"""Provide an abstract base class for exporters.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from abc import ABC, abstractmethod


class NvExporter(ABC):
    """Converter class for document export.
    
    Public methods:
        run(source, suffix, lock=False, show=False) -- Create a target object and run conversion.    
    """

    @abstractmethod
    def run(self, source, suffix, lock=False, show=False):
        """Create a target object and run conversion.

        Positional arguments: 
            source -- Yw7File instance.
            suffix: str -- Target file name suffix.
            lock: bool -- Lock the project, if True.
            show: bool -- After document creation, ask if open it with Office.
        """
        pass

