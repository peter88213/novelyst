"""Provide an XML item data file reader class.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *
from pywriter.yw.yw7_file import Yw7File


class ItemDataReader(Yw7File):
    """XML item data file reader.
       
    Public methods:
        read() -- Parse the xml file and get the instance variables.   
       
    """
    DESCRIPTION = _('XML item data file')
    EXTENSION = '.xml'

    def read(self):
        """Parse the xml files and get the instance variables.
        
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """
        try:
            tree = ET.parse(self.filePath)
        except:
            raise Error(f'{_("Can not process file")}: "{norm_path(self.filePath)}".')
        else:
            root = ET.Element('ROOT')
            root.append(tree.getroot())
            self._read_items(root)

