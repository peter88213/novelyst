"""Provide a base class for HTML report file representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pywriter.file.file_export import FileExport


class HtmlReport(FileExport):
    """Class for HTML report file representation."""
    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    SUFFIX = '_report'

    _fileHeader = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

<style type="text/css">
body {font-family: sans-serif}
p.title {font-size: larger; font-weight: bold}
td {padding: 10}
tr.heading {font-size:smaller; font-weight: bold; background-color:lightgray}
table {border-spacing: 0}
table, td {border: lightgrey solid 1px; vertical-align: top}
td.chtitle {font-weight: bold}
</style>

'''

    _fileFooter = '''</table>
</body>
</html>
'''

