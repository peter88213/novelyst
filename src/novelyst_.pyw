#!/usr/bin/env python3
"""A novel organizer for writers. 

Version @release
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from pathlib import Path
from pywriter.pywriter_globals import *
from pywriter.config.configuration import Configuration
from novelystlib.novelyst_tk import NovelystTk

APPNAME = 'novelyst'
SETTINGS = dict(
    yw_last_open='',
    root_geometry='1200x800',
    gui_theme='',
    button_context_menu='<Button-3>',
    middle_frame_width=400,
    right_frame_width=350,
    color_chapter='green',
    color_unused='gray',
    color_notes='blue',
    color_todo='red',
    color_major='navy',
    color_minor='cornflower blue',
    color_outline='dark orchid',
    color_draft='black',
    color_1st_edit='DarkGoldenrod4',
    color_2nd_edit='DarkGoldenrod3',
    color_done='DarkGoldenrod2',
    color_staged='black',
    color_descriptive='light sea green',
    color_explaining='brown',
    color_summarizing='magenta',
    color_locked_bg='dim gray',
    color_locked_fg='light gray',
    color_modified_bg='goldenrod1',
    color_modified_fg='maroon',
    color_text_bg='white',
    color_text_fg='black',
    color_notes_bg='lemon chiffon',
    color_notes_fg='black',
    coloring_mode='',
    title_width=400,
    ps_width=50,
    wc_width=50,
    status_width=100,
    style_width=100,
    nt_width=20,
    vp_width=100,
    tags_width=100,
    pacing_width=40,
    date_width=70,
    time_width=40,
    duration_width=55,
    arcs_width=55,
    column_order='wc;vp;sy;st;nt;dt;tm;dr;tg;po;ac;ar'
)
OPTIONS = dict(
    show_contents=True,
    show_markup=False,
    show_language_settings=False,
    show_auto_numbering=False,
    show_renamings=False,
    show_writing_progress=False,
    show_action_reaction=False,
    show_relationships=False,
    show_cr_bio=True,
    show_cr_goals=True,
)


def run(sourcePath='', installDir='.', configDir='.'):

    #--- Load configuration.
    iniFile = f'{configDir}/{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = {}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    #--- Get initial project path.
    if not sourcePath or not os.path.isfile(sourcePath):
        sourcePath = kwargs['yw_last_open']

    #--- Create a directory for temporary files.
    tempDir = f'{installDir}/temp'
    os.makedirs(tempDir, exist_ok=True)

    #--- Instantiate the app object.
    app = NovelystTk('novelyst @release', tempDir, **kwargs)
    app.open_project(sourcePath)
    app.start()

    #--- Save project specific configuration
    for keyword in app.kwargs:
        if keyword in configuration.options:
            configuration.options[keyword] = app.kwargs[keyword]
        elif keyword in configuration.settings:
            configuration.settings[keyword] = app.kwargs[keyword]
    configuration.write(iniFile)

    #--- Delete the temporary files.
    # Note: Do not remove the temp directory itself,
    # because other novelyst instances might be running and using it.
    # However, temporary files of other running instances are deleted
    # if not protected e.g. by a read-only flag.
    for file in os.scandir(tempDir):
        try:
            os.remove(file)
        except:
            pass


if __name__ == '__main__':
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}'
    except:
        installDir = '.'
    os.makedirs(installDir, exist_ok=True)
    configDir = f'{installDir}/config'
    os.makedirs(configDir, exist_ok=True)
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, installDir, configDir)
