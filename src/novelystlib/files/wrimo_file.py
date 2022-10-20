"""Provide a class for an obfuscated text file representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw2md
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

from pywriter.pywriter_globals import *
from pywriter.file.file_export import FileExport


class WrimoFile(FileExport):
    """Obfuscated text file representation.

    Public methods:
        read() -- parse the file and get the instance variables.
    """
    DESCRIPTION = _('Obfuscated text for word count')
    EXTENSION = '.txt'
    SUFFIX = '_wrimo'

    _sceneTemplate = '$SceneContent\n\n'

    def _convert_from_yw(self, text, quick=False):
        """Return obfuscated text for an exact word count.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting.
        
        Overrides the superclass method.
        """
        if text:
            text = ADDITIONAL_WORD_LIMITS.sub(' ', text)
            text = NO_WORD_LIMITS.sub('', text)
            # at this point, all words are delimited by spaces
            text = re.sub('\S', 'x', text)
        else:
            text = ''
        return text

