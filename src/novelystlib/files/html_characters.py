"""Provide a class for HTML charcters report file representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novelystlib.files.html_report import HtmlReport
from pywriter.pywriter_globals import *


class HtmlCharacters(HtmlReport):
    """Class for HTML characters report file representation."""
    DESCRIPTION = 'HTML charcters report'
    EXTENSION = '.html'
    SUFFIX = '_character_report'

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Characters')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Characters')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Name')}</td>
<td>{_('Full name')}</td>
<td>{_('AKA')}</td>
<td>{_('Tags')}</td>
<td>{_('Description')}</td>
<td>{_('Bio')}</td>
<td>{_('Goals')}</td>
<td>{_('Notes')}</td>
</tr>
'''

    _characterTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$FullName</td>
<td>$AKA</td>
<td>$Tags</td>
<td>$Desc</td>
<td>$Bio</td>
<td>$Goals</td>
<td>$Notes</td>
</tr>
'''

