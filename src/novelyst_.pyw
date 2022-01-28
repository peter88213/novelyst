#!/usr/bin/env python3
"""yWriter file viewer. 

Version @release

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pathlib import Path

from pywriter.config.configuration import Configuration
from pynovelyst.novelyst_tk import NovelystTk

APPNAME = 'novelyst'

SETTINGS = dict(
    yw_last_open='',
)

OPTIONS = {}


def run(sourcePath='', installDir=''):

    #--- Load configuration.

    iniFile = installDir + APPNAME + '.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = {}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    #--- Get initial project path.

    if not sourcePath or not os.path.isfile(sourcePath):
        sourcePath = kwargs['yw_last_open']

    #--- Instantiate the app object.

    app = NovelystTk('novelyst @release', **kwargs)
    app.open_project(sourcePath)
    app.start()

    #--- Save project specific configuration

    for keyword in app.kwargs:

        if keyword in configuration.options:
            configuration.options[keyword] = app.kwargs[keyword]

        elif keyword in configuration.settings:
            configuration.settings[keyword] = app.kwargs[keyword]

        configuration.write(iniFile)


if __name__ == '__main__':

    try:
        installDir = '{}/.pywriter/{}/config/'.format(str(Path.home()).replace('\\', '/'), APPNAME)

    except:
        installDir = ''

    os.makedirs(installDir, exist_ok=True)

    if len(sys.argv) == 1:
        run('', installDir)

    else:
        parser = argparse.ArgumentParser(
            description='Novel metadata organizer',
            epilog='')
        parser.add_argument('sourcePath',
                            metavar='Sourcefile',
                            help='The path of the yWriter project file.')

        args = parser.parse_args()
        run(args.sourcePath, installDir)
