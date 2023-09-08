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

        def create_cell(cell, attr=''):
            return f'<td{attr}>{cell}</td>'

        STYLE_CH_TITLE = 'font-weight: bold; color: red'
        htmlText = [self._fileHeader]
        htmlText.append(f'''<title>{self.novel.title}</title>
</head>
<body>
<p class=title>{self.novel.title} - {_("Plot")}</p>
<table>''')
        arcColors = (
            'LightSteelBlue',
            'Gold',
            'Coral',
            'YellowGreen',
            'MediumTurquoise',
            'Plum',
            )

        # Get arcs.
        arcs = {}
        scnArcs = {}
        for chId in self.novel.srtChapters:
            arcDefinition = self.novel.chapters[chId].kwVar.get('Field_ArcDefinition', None)
            if arcDefinition is not None:
                arcs[arcDefinition] = self.novel.chapters[chId].title

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(create_cell(''))
        for i, arc in enumerate(arcs):
            j = i % len(arcColors)
            htmlText.append(create_cell(arcs[arc], attr=f' style="background: {arcColors[j]}"'))
        htmlText.append('</tr>')

        # Chapter/scene rows.
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chType == 2:
                if self.novel.chapters[chId].chLevel > 0:
                    # do not include the "Planning" section
                    break

                htmlText.append(f'<tr>')
                htmlText.append(create_cell(self.novel.chapters[chId].title, attr=f' style="{STYLE_CH_TITLE}"'))
                for arc in arcs:
                    htmlText.append(create_cell(''))
                htmlText.append(f'</tr>')
            for scId in self.novel.chapters[chId].srtScenes:
                if self.novel.scenes[scId].scType == 0:
                    htmlText.append(f'<tr>')
                    scnArcs[scId] = string_to_list(self.novel.scenes[scId].scnArcs)
                    htmlText.append(create_cell(self.novel.scenes[scId].title))
                    for i, arc in enumerate(arcs):
                        j = i % len(arcColors)
                        if arc in scnArcs[scId]:
                            entry = ''
                            # Use arc point titles instead of binary marker.
                            pointIds = string_to_list(self.novel.scenes[scId].kwVar.get('Field_SceneAssoc', None))
                            points = []
                            for ptId in pointIds:
                                if arc in self.novel.scenes[ptId].scnArcs:
                                    points.append(self.novel.scenes[ptId].title)
                            if points:
                                entry = list_to_string(points)
                            htmlText.append(create_cell(entry, attr=f' style="background: {arcColors[j]}"'))
                        else:
                            htmlText.append(create_cell(''))
                    htmlText.append(f'</tr>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))
