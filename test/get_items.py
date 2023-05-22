"""Read items from an XML data file.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
from pywriter.model.novel import Novel
from novelystlib.data_reader.item_data_reader import ItemDataReader

filePath = sys.argv[1]
dataSet = ItemDataReader(filePath)
dataSet.novel = Novel()
dataSet.read()
for itId in dataSet.novel.items:
    print(dataSet.novel.items[itId].title)

