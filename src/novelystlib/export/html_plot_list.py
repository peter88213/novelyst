"""Provide a class for html plot list representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pywriter.pywriter_globals import *
from novelystlib.export.html_report import HtmlReport


class HtmlPlotList(HtmlReport):
    """html plot list representation.

    Public methods:
        write() -- Write instance variables to the file.

    Public instance variables:
        filePath: str -- path to the file (property with getter and setter). 

    """
    DESCRIPTION = _('HTML Plot list')
    SUFFIX = '_plotlist'

    def write(self):
        """Create a HTML table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        def to_html(cell):
            return f'<td>{cell}</td>'

        STYLE_CH_TITLE = 'font-weight: bold; color: red'
        HTML_TRUE = '●'
        HTML_FALSE = ''
        htmlText = [self._fileHeader]
        htmlText.append(f'''<title>{self.novel.title}</title>
</head>
<body>
<p class=title>{self.novel.title} - {_("Plot")}</p>
<table>''')

        # Get arcs.
        arcs = {}
        scnArcs = {}
        for chId in self.novel.srtChapters:
            arcDefinition = self.novel.chapters[chId].kwVar.get('Field_ArcDefinition', None)
            if arcDefinition is not None:
                arcs[arcDefinition] = self.novel.chapters[chId].title

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(to_html(''))
        for arc in arcs:
            htmlText.append(to_html(arcs[arc]))
        htmlText.append('</tr>')

        # Chapter/scene rows.
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chType == 2:
                if self.novel.chapters[chId].chLevel > 0:
                    # do not include the "Planning" section
                    break

                htmlText.append(f'<tr>')
                htmlText.append(f'<td style="{STYLE_CH_TITLE}">{self.novel.chapters[chId].title}</td>')
                for arc in arcs:
                    htmlText.append(to_html(''))
                htmlText.append(f'</tr>')
            for scId in self.novel.chapters[chId].srtScenes:
                htmlText.append(f'<tr>')
                if self.novel.scenes[scId].scType == 0:
                    scnArcs[scId] = string_to_list(self.novel.scenes[scId].scnArcs)
                    htmlText.append(to_html(self.novel.scenes[scId].title))
                    for i, arc in enumerate(arcs):
                        if arc in scnArcs[scId]:
                            entry = HTML_TRUE
                            # Use arc point titles instead of binary marker.
                            pointIds = string_to_list(self.novel.scenes[scId].kwVar.get('Field_SceneAssoc', None))
                            points = []
                            for ptId in pointIds:
                                if arc in self.novel.scenes[ptId].scnArcs:
                                    points.append(self.novel.scenes[ptId].title)
                            if points:
                                entry = list_to_string(points)
                        else:
                            entry = HTML_FALSE
                        htmlText.append(to_html(entry))
                htmlText.append(f'</tr>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.writelines(htmlText)
