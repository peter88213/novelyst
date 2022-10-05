"""Generate a template file (pot) for message translation.

This script is for the Windows Explorer context menu
as specified by the ".reg" file to generate. 

For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
sys.path.insert(0, f'{os.getcwd()}/../../PyWriter/src')
import pgettext

APP = 'novelyst'
POT_FILE = '../i18n/reg.pot'
SETUP_SCRIPT = '../src/setup.pyw'


def make_pot(version='unknown'):

    # Generate a pot file from the script.
    if os.path.isfile(POT_FILE):
        os.replace(POT_FILE, f'{POT_FILE}.bak')
        backedUp = True
    else:
        backedUp = False
    pot = pgettext.PotFile(POT_FILE, app=APP, appVersion=version)
    pot.scan_file(SETUP_SCRIPT)
    print(f'Writing "{pot.filePath}"...\n')
    try:
        pot.write_pot()
        return True

    except:
        if backedUp:
            os.replace(f'{POT_FILE}.bak', POT_FILE)
        print('WARNING: Cannot write pot file.')
        return False


if __name__ == '__main__':
    try:
        success = make_pot(sys.argv[1])
    except:
        success = make_pot()
    if not success:
        sys.exit(1)
