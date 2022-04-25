#!/usr/bin/env python3
""""Provide a class for viewing tree element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ElementView:
    """A generic class for viewing tree element properties.
    """

    def __init__(self, ui, element):
        self._element = element

    def apply_changes(self):
        """Apply changes.
        
        This is a stub to be overridden by subclasses.
        """

    def close(self):
        """Apply changes and close the view."""
        self.apply_changes()
        del self
