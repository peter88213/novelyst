"""Provide a class for ods plot list representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tempfile
from pywriter.pywriter_globals import *
from pywriter.ods_w.ods_writer import OdsWriter


class OdsPlotList(OdsWriter):
    """html plot list representation.

    Public methods:
        write() -- Write instance variables to the file.

    Public instance variables:
        filePath: str -- path to the file (property with getter and setter). 

    """
    DESCRIPTION = _('ODS Plot list')
    SUFFIX = '_plotlist'

    _fileHeader = f'{OdsWriter._CONTENT_XML_HEADER}{DESCRIPTION}" table:style-name="ta1" table:print="false">'

    def write_content_xml(self):
        """Create the ODS table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        def to_ods(cell, style=''):
            return f'''     <table:table-cell {style} office:value-type="string">
      <text:p>{cell}</text:p>
     </table:table-cell>'''

        odsText = [
            self._fileHeader,
            '<table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>',
            ]

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
                odsText.append('<table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>')

        # Title row.
        odsText.append('   <table:table-row table:style-name="ro2">')
        odsText.append(to_ods(''))
        for i, arc in enumerate(arcs):
            j = i % len(arcColors)
            odsText.append(to_ods(arcs[arc], style=' table:style-name="Heading" '))
        odsText.append('    </table:table-row>')

        # Chapter/scene rows.
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chType == 2:
                if self.novel.chapters[chId].chLevel > 0:
                    # do not include the "Planning" section
                    break

                odsText.append('   <table:table-row table:style-name="ro2">')
                odsText.append(to_ods(self.novel.chapters[chId].title))
                for arc in arcs:
                    odsText.append(to_ods(''))
                odsText.append(f'    </table:table-row>')
            for scId in self.novel.chapters[chId].srtScenes:
                odsText.append('   <table:table-row table:style-name="ro2">')
                if self.novel.scenes[scId].scType == 0:
                    scnArcs[scId] = string_to_list(self.novel.scenes[scId].scnArcs)
                    odsText.append(to_ods(self.novel.scenes[scId].title))
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
                            odsText.append(to_ods(entry))
                        else:
                            odsText.append(to_ods(''))
                odsText.append(f'    </table:table-row>')

        odsText.append(self._CONTENT_XML_FOOTER)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(odsText))
