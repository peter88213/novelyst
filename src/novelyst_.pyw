#!/usr/bin/env python3
"""A tree view for ywriter projects. 

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
    key_restore_status='<Escape>',
    key_open_project='<Control-o>',
    key_quit_program='<Control-q>',
    key_new_project='<Control-n>',
    key_lock_project='<Control-l>',
    key_unlock_project='<Control-u>',
    key_reload_project='<Control-r>',
    key_save_project='<Control-s>',
    key_save_as='<Control-S>',
    button_context_menu='<Button-3>',
    tree_frame_width=800,
    color_chapter='green',
    color_unused='gray',
    color_notes='blue',
    color_todo='red',
    color_major='navy',
    color_minor='cornflower blue',
    color_outline='firebrick4',
    color_draft='black',
    color_1st_edit='DarkOrange3',
    color_2nd_edit='DarkOrange1',
    color_done='DarkGoldenrod2',
    color_locked_bg='dim gray',
    color_locked_fg='white',
    color_modified_bg='DarkGoldenrod2',
    color_modified_fg='brown',
    wc_width=65,
    status_width=80,
    vp_width=80,
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
