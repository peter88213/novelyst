"""Provide a class for HTML locations report file representation.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novelystlib.export.html_report import HtmlReport
from pywriter.pywriter_globals import *


class HtmlLocations(HtmlReport):
    """Class for HTML locations report file representation."""
    DESCRIPTION = 'HTML locations report'
    EXTENSION = '.html'
    SUFFIX = '_location_report'

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Locations')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Locations')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Name')}</td>
<td>{_('AKA')}</td>
<td>{_('Tags')}</td>
<td>{_('Description')}</td>
</tr>
'''

    _locationTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$AKA</td>
<td>$Tags</td>
<td>$Desc</td>
</tr>
'''

