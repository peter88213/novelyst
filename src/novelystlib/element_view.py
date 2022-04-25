#!/usr/bin/env python3
""""Provide a class for viewing tree element properties.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ElementView:
    """A generic class for viewing tree element properties.
    """

    def close(self):
        """Close the view."""
        del self
