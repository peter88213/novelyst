"""Read locations from an XML data file.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import sys
from pywriter.model.novel import Novel
from novelystlib.data_reader.location_data_reader import LocationDataReader

filePath = sys.argv[1]
dataSet = LocationDataReader(filePath)
dataSet.novel = Novel()
dataSet.read()
for lcId in dataSet.novel.locations:
    print(dataSet.novel.locations[lcId].title)

