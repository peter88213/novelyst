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

    _ADDITIONAL_STYLES = '''
  <style:style style:name="ce0" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties style:text-align-source="value-type" style:repeat-content="false"/>
   <style:paragraph-properties fo:margin-left="0cm"/>
   <style:text-properties fo:color="#ff0000" fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
  </style:style>
  <style:style style:name="ce1" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#b0c4de"/>
  </style:style>
  <style:style style:name="ce2" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#ffd700"/>
  </style:style>
  <style:style style:name="ce3" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#ff7f50"/>
  </style:style>
  <style:style style:name="ce4" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#9acd32"/>
  </style:style>
  <style:style style:name="ce5" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#48d1cc"/>
  </style:style>
  <style:style style:name="ce6" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#dda0dd"/>
  </style:style>
 </office:automatic-styles>'''

    _fileHeader = OdsWriter._CONTENT_XML_HEADER.replace(' </office:automatic-styles>', _ADDITIONAL_STYLES)
    _fileHeader = f'{_fileHeader}{DESCRIPTION}" table:style-name="ta1" table:print="false">'

    def write_content_xml(self):
        """Create the ODS table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        def create_cell(text, attr='', link=''):
            """Return the markup for a table cell with text and attributes."""
            if link:
                attr = f'{attr} table:formula="of:=HYPERLINK(&quot;file:///{self.projectPath}/{self._convert_from_yw(self.projectName)}{link}&quot;;&quot;{self._convert_from_yw(text)}&quot;)"'
                text = ''
            else:
                text = f'\n      <text:p>{self._convert_from_yw(text)}</text:p>'
            return f'     <table:table-cell {attr} office:value-type="string">{text}\n     </table:table-cell>'

        odsText = [
            self._fileHeader,
            '<table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>',
            ]

        arcColorsTotal = 6
        # total number of the background colors used in the "ce" table cell styles

        # Get arcs.
        arcs = {}
        arcIds = {}
        scnArcs = {}
        for chId in self.novel.srtChapters:
            arcDefinition = self.novel.chapters[chId].kwVar.get('Field_ArcDefinition', None)
            if arcDefinition is not None:
                arcs[arcDefinition] = self.novel.chapters[chId].title
                odsText.append('<table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>')
                arcIds[arcDefinition] = chId

        # Title row.
        odsText.append('   <table:table-row table:style-name="ro2">')
        odsText.append(create_cell(''))
        for i, arc in enumerate(arcs):
            j = (i % arcColorsTotal) + 1
            odsText.append(create_cell(arcs[arc], attr=f'table:style-name="ce{j}"', link=f'_arcs.odt#ChID{arcIds[arc]}'))
        odsText.append('    </table:table-row>')

        # Chapter/scene rows.
        for chId in self.novel.srtChapters:
            if self.novel.chapters[chId].chType == 2:
                if self.novel.chapters[chId].chLevel > 0:
                    # do not include the "Planning" section
                    break

                odsText.append('   <table:table-row table:style-name="ro2">')
                odsText.append(create_cell(self.novel.chapters[chId].title, attr='table:style-name="ce0"'))
                for arc in arcs:
                    odsText.append(create_cell(''))
                odsText.append(f'    </table:table-row>')
            for scId in self.novel.chapters[chId].srtScenes:
                if self.novel.scenes[scId].scType == 0:
                    odsText.append('   <table:table-row table:style-name="ro2">')
                    scnArcs[scId] = string_to_list(self.novel.scenes[scId].scnArcs)
                    odsText.append(create_cell(self.novel.scenes[scId].title, link=f'_manuscript.odt#ScID:{scId}%7Cregion'))
                    for i, arc in enumerate(arcs):
                        j = (i % arcColorsTotal) + 1
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
                            odsText.append(create_cell(entry, attr=f'table:style-name="ce{j}" '))
                        else:
                            odsText.append(create_cell(''))
                    odsText.append(f'    </table:table-row>')

        odsText.append(self._CONTENT_XML_FOOTER)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(odsText))
