""" Build a python script for the novelyst distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the pywriter package.

The PyWriter project (see see https://github.com/peter88213/PyWriter)
must be located on the same directory level as the novelyst project. 

For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE_GUI = 'novelyst_.pyw'
TARGET_FILE_GUI = f'{BUILD}novelyst.pyw'


def main():
    os.chdir(SRC)

    try:
        os.remove(TARGET_FILE_GUI)

    except:
        pass

    inliner.run(SOURCE_FILE_GUI,
                TARGET_FILE_GUI, 'pynovelyst', '../src/')
    inliner.run(TARGET_FILE_GUI,
                TARGET_FILE_GUI, 'pywriter', '../../PyWriter/src/')
    print('Done.')


if __name__ == '__main__':
    main()
