"""Provide a class for HTML project notes report file representation.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pywriter.pywriter_globals import *
from novelystlib.export.html_report import HtmlReport


class HtmlProjectNotes(HtmlReport):
    """Class for HTML project notes report file representation."""
    DESCRIPTION = 'HTML project notes report'
    EXTENSION = '.html'
    SUFFIX = '_projectnote_report'

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Project notes')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Project notes')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Title')}</td>
<td>{_('Text')}</td>
</tr>
'''

    _projectNoteTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$Desc</td>
</tr>
'''

