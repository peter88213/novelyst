"""Provide a class for ODT invisibly tagged character descriptions export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pywriter.pywriter_globals import *
from pywriter.odt.odt_characters import OdtCharacters


class OdtCharactersNv(OdtCharacters):
    """ODT character descriptions file representation.

    Export a character sheet with invisibly tagged descriptions.
    """

    _characterTemplate = f'''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$FullName$AKA</text:h>
<text:section text:style-name="Sect1" text:name="CrID:$ID">
<text:h text:style-name="Heading_20_3" text:outline-level="3">{_("Description")}</text:h>
<text:section text:style-name="Sect1" text:name="CrID_desc:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">$BioTitle</text:h>
<text:section text:style-name="Sect1" text:name="CrID_bio:$ID">
<text:p text:style-name="Text_20_body">$Bio</text:p>
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">$GoalsTitle</text:h>
<text:section text:style-name="Sect1" text:name="CrID_goals:$ID">
<text:p text:style-name="Text_20_body">$Goals</text:p>
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">{_("Notes")}</text:h>
<text:section text:style-name="Sect1" text:name="CrID_notes:$ID">
<text:p text:style-name="Text_20_body">$Notes</text:p>
</text:section>
</text:section>
'''
    _PRJ_KWVAR = (
        'Field_CustomChrBio',
        'Field_CustomChrGoals',
        )

    def _get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section.
        
        Positional arguments:
            crId -- str: character ID.
        
        Use custom titles, if any.
        Extends the superclass method.
        """
        characterMapping = super()._get_characterMapping(crId)

        if self.novel.kwVar.get('Field_CustomChrBio', None):
            characterMapping['BioTitle'] = self.novel.kwVar['Field_CustomChrBio']
        else:
            characterMapping['BioTitle'] = _('Bio')
        if self.novel.kwVar.get('Field_CustomChrGoals', None):
            characterMapping['GoalsTitle'] = self.novel.kwVar['Field_CustomChrGoals']
        else:
            characterMapping['GoalsTitle'] = _('Goals')

        return characterMapping

