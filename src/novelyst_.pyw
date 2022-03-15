#!/usr/bin/env python3
"""yWriter file viewer. 

Version @release
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pathlib import Path
from pywriter.config.configuration import Configuration
from novelystlib.novelyst_tk import NovelystTk

APPNAME = 'novelyst'
SETTINGS = dict(
    yw_last_open='',
    root_geometry='1200x800',
    tree_frame_width=500,
    color_chapter='green',
    color_unused='gray',
    color_notes='blue',
    color_todo='red',
    color_major='navy',
    color_minor='cornflower blue',
    color_outline='firebrick1',
    color_draft='firebrick4',
    color_1st_edit='DarkOrange1',
    color_2nd_edit='goldenrod2',
    color_done='DarkOliveGreen4',
    wc_width=50,
    status_width=50,
    vp_width=100,
    tags_width=100,
)
OPTIONS = {}


def run(sourcePath='', installDir='.'):

    #--- Load configuration.
    iniFile = f'{installDir}/{APPNAME}.ini'
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
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}/config'
    except:
        installDir = '.'
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
